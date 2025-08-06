import pandas as pd 

def add_fx_rate(df, fx_df, date_col='Date', fx_date_col='Date', fx_col='fx_rate', new_col='fx_rate'):
    """
    Adds FX rate data (USD/EGP) to the DataFrame by merging on date.

    Parameters:
    - df: pandas DataFrame with transaction data, must contain a datetime column `date_col`
    - fx_df: pandas DataFrame with FX rate data, must contain columns `fx_date_col` and `fx_col`
    - date_col: name of the datetime column in df (default 'Date')
    - fx_date_col: name of the datetime column in fx_df (default 'Date')
    - fx_col: name of the FX rate column in fx_df (default 'fx_rate')
    - new_col: name for the new FX rate column in the result (default 'fx_rate')

    Returns:
    - A copy of df with a new column `new_col` containing the FX rate for each date.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    fx_df = fx_df.copy()
    fx_df[fx_date_col] = pd.to_datetime(fx_df[fx_date_col])

    # Merge on date, left join to keep all original rows
    merged = pd.merge(df, fx_df[[fx_date_col, fx_col]], how='left',
                      left_on=date_col, right_on=fx_date_col)
    merged.rename(columns={fx_col: new_col}, inplace=True)
    merged.drop(columns=[fx_date_col], inplace=True)

    # Optionally fill missing FX values (e.g., forward fill)
    merged[new_col] = merged[new_col].fillna(method='ffill')

    return merged

def add_inflation_index(df, inflation_df, date_col='Date', inflation_date_col='Date', inflation_col='inflation_index', new_col='inflation_index'):

    """
    Adds monthly consumer inflation index to the DataFrame by matching on year and month.

    Parameters:
    - df: pandas DataFrame with daily transaction data
    - inflation_df: pandas DataFrame with monthly inflation data (columns inflation_date_col, inflation_col)
    - date_col: name of the datetime column in df (default 'Date')
    - inflation_date_col: name of the datetime column in inflation_df (default 'Date')
    - inflation_col: name of the inflation index column in inflation_df (default 'inflation_index')
    - new_col: name for the new inflation index column in the result (default 'inflation_index')

    Returns:
    - A copy of df with a new column `new_col` containing the inflation index for each transaction’s month.
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    inflation_df = inflation_df.copy()
    inflation_df[inflation_date_col] = pd.to_datetime(inflation_df[inflation_date_col])

    # Create year-month columns for merging
    df['year_month'] = df[date_col].dt.to_period('M')
    inflation_df['year_month'] = inflation_df[inflation_date_col].dt.to_period('M')

    merged = pd.merge(df, inflation_df[['year_month', inflation_col]], how='left', on='year_month')
    merged.rename(columns={inflation_col: new_col}, inplace=True)
    merged.drop(columns=['year_month'], inplace=True)

    # Handle missing inflation index, if any (e.g., fill forward)
    merged[new_col] = merged[new_col].fillna(method='ffill')

    return merged