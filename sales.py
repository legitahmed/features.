# sales_features.py
import pandas as pd

def add_rolling_avg_sales_7d(df, 
                             date_col='Date', 
                             group_cols=['Store No_', 'Item No_'], 
                             value_col='Net Amount', 
                             new_col='rolling_avg_7d'):
    """
    Adds a numeric 'rolling_avg_7d' feature representing the 7-day moving average 
    of sales ('Net Amount') for each item in each store.

    Parameters:
    - df: pandas DataFrame
    - date_col: name of the datetime column to sort by
    - group_cols: list of columns to group by (typically Store and Item)
    - value_col: column to calculate the rolling average on (typically 'Net Amount')
    - new_col: name of the new feature column

    Returns:
    - DataFrame with the rolling_avg_7d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    df.sort_values(by=group_cols + [date_col], inplace=True)
    df[new_col] = (
        df.groupby(group_cols)[value_col]
        .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    )
    return df

def add_rolling_avg_sales_15d(df, 
                              date_col='Date', 
                              group_cols=['Store No_', 'Item No_'], 
                              value_col='Net Amount', 
                              new_col='rolling_avg_15d'):
    """
    Adds a numeric 'rolling_avg_15d' feature representing the 15-day moving average 
    of sales ('Net Amount') for each item in each store.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: list of columns to group by (e.g. Store, Item)
    - value_col: column to average (e.g. Net Amount)
    - new_col: name of the new feature column

    Returns:
    - DataFrame with the rolling_avg_15d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    df.sort_values(by=group_cols + [date_col], inplace=True)
    df[new_col] = (
        df.groupby(group_cols)[value_col]
        .transform(lambda x: x.rolling(window=15, min_periods=1).mean())
    )
    return df

def add_rolling_avg_sales_30d(df, 
                              date_col='Date', 
                              group_cols=['Store No_', 'Item No_'], 
                              value_col='Net Amount', 
                              new_col='rolling_avg_30d'):
    """
    Adds a numeric 'rolling_avg_30d' feature representing the 30-day moving average 
    of sales ('Net Amount') for each item in each store.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: list of columns to group by
    - value_col: column to average
    - new_col: name of the new feature column

    Returns:
    - DataFrame with the rolling_avg_30d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=group_cols + [date_col], inplace=True)

    df[new_col] = (
        df.groupby(group_cols)[value_col]
        .transform(lambda x: x.rolling(window=30, min_periods=1).mean())
    )
    return df

def add_sales_lag_1d(df,      
                     date_col='Date', 
                     group_cols=['Store No_', 'Item No_'], 
                     value_col='Net Amount', 
                     new_col='sales_lag_1d'):
    """
    Adds a numeric 'sales_lag_1d' feature representing the sales from the previous day.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: columns to group by
    - value_col: target column to lag
    - new_col: name of the new lag feature

    Returns:
    - DataFrame with the sales_lag_1d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=group_cols + [date_col], inplace=True)

    df[new_col] = df.groupby(group_cols)[value_col].shift(1)
    return df

def add_sales_lag_7d(df, 
                     date_col='Date', 
                     group_cols=['Store No_', 'Item No_'], 
                     value_col='Net Amount', 
                     new_col='sales_lag_7d'):
    """
    Adds a numeric 'sales_lag_7d' feature representing the sales from 7 days ago.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: columns to group by
    - value_col: target column to lag
    - new_col: name of the new lag feature

    Returns:
    - DataFrame with the sales_lag_7d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=group_cols + [date_col], inplace=True)

    df[new_col] = df.groupby(group_cols)[value_col].shift(7)
    return df

def add_std_dev_sales_15d(df, 
                          date_col='Date', 
                          group_cols=['Store No_', 'Item No_'], 
                          value_col='Net Amount', 
                          new_col='std_dev_sales_15d'):
    """
    Adds a numeric 'std_dev_sales_15d' feature representing the standard deviation of sales 
    over the last 15 days, a measure of volatility.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: columns to group by
    - value_col: target sales column
    - new_col: name of the volatility feature

    Returns:
    - DataFrame with the std_dev_sales_15d column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=group_cols + [date_col], inplace=True)

    df[new_col] = (
        df.groupby(group_cols)[value_col]
        .transform(lambda x: x.rolling(window=15, min_periods=1).std())
    )
    return df

def add_last_year_same_period_sales(df, 
                                    date_col='Date', 
                                    group_cols=['Store No_', 'Item No_'], 
                                    value_col='Net Amount', 
                                    new_col='last_year_same_period_sales'):
    """
    Adds a numeric 'last_year_same_period_sales' feature by lagging the sales by 365 days.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: group-by columns
    - value_col: sales column
    - new_col: output feature name

    Returns:
    - DataFrame with last_year_same_period_sales column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values(by=group_cols + [date_col], inplace=True)

    df[new_col] = df.groupby(group_cols)[value_col].shift(365)
    return df

def add_total_sales_last_ramadan(df, 
                                  date_col='Date', 
                                  group_cols=['Store No_', 'Item No_'], 
                                  value_col='Net Amount', 
                                  new_col='total_sales_last_ramadan',
                                  ramadan_ranges=None):
    """
    Adds a numeric 'total_sales_last_ramadan' feature by summing sales in the Ramadan 
    period of the previous year for each item and store.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - group_cols: columns to group by
    - value_col: sales column
    - new_col: output column name
    - ramadan_ranges: list of tuples (start_date, end_date) of Ramadan periods

    Returns:
    - DataFrame with total_sales_last_ramadan column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    if ramadan_ranges is None:
       ramadan_ranges = [
    ('2024-03-10', '2024-04-08'),   # 2024
    ('2025-02-28', '2025-03-30'),   # 2025  
    ('2026-02-18', '2026-03-19'),   # 2026
    ('2027-02-07', '2027-03-08'),   # 2027
    ('2028-01-27', '2028-02-25'),   # 2028
    ('2029-01-15', '2029-02-13'),   # 2029
    ('2030-01-05', '2030-02-03'),   # 2030
    ('2031-12-26', '2032-01-24'),   # 2031 (spans into 2032)
    ('2032-12-14', '2033-01-12'),   # 2032 (spans into 2033)
    ('2033-12-04', '2034-01-02'),   # 2033 (spans into 2034)
    ('2034-11-23', '2034-12-22'),   # 2034
    ('2035-11-12', '2035-12-11')    # 2035 
       ]
    ramadan_df = pd.DataFrame()
    for start, end in ramadan_ranges:
        mask = (df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))
        period_df = df.loc[mask].copy()
        period_df['ramadan_year'] = pd.to_datetime(start).year
        ramadan_df = pd.concat([ramadan_df, period_df], axis=0)

    # Sum sales in previous Ramadan for each item-store combo
    ramadan_sum = (
        ramadan_df.groupby(group_cols + ['ramadan_year'])[value_col]
        .sum()
        .reset_index()
        .rename(columns={value_col: new_col})
    )

    # Add year column to original df for mapping
    df['year'] = df[date_col].dt.year
    df = df.merge(ramadan_sum, left_on=group_cols + ['year'], 
                  right_on=group_cols + ['ramadan_year'], how='left')
    
    df.drop(columns=['year', 'ramadan_year'], inplace=True, errors='ignore')
    return df


