import pandas as pd

def add_current_stock_qty(df_metrics, df_stock, date_col='Date', item_col='Item No_', store_col='Store No_', new_col='current_stock_qty'):
    """
    Adds the current stock quantity feature to df_metrics by merging stock data.

    Parameters:
    - df_metrics: pandas DataFrame with metrics data
    - df_stock: pandas DataFrame with stock data (Location Code, Item No_, Date, Stock)
    - date_col: datetime column in df_metrics (default 'Date')
    - item_col: item identifier column in df_metrics (default 'Item No_')
    - store_col: store/location column in df_metrics (default 'Store No_')
    - new_col: name of the new feature column to create (default 'current_stock_qty')

    Returns:
    - DataFrame with current_stock_qty column added (numeric), NaN if no matching stock found
    """
    df_metrics = df_metrics.copy()
    df_stock = df_stock.copy()

    # Normalize column names for merging
    df_stock.rename(columns={'Location Code': store_col}, inplace=True)

    # Ensure datetime format
    df_metrics[date_col] = pd.to_datetime(df_metrics[date_col])
    df_stock['Date'] = pd.to_datetime(df_stock['Date'])

    # Merge on Store, Item, Date (exact date match)
    df_merged = pd.merge(df_metrics, 
                         df_stock[[store_col, item_col, 'Date', 'Stock']],
                         how='left',
                         left_on=[store_col, item_col, date_col],
                         right_on=[store_col, item_col, 'Date'])
    df_merged[new_col] = df_merged['Stock']

    # Drop duplicate 'Date' column from stock table
    df_merged.drop(columns=['Date_y'], inplace=True)
    df_merged.rename(columns={date_col: 'Date'}, inplace=True)

    return df_merged

def add_stock_cover_days(df, stock_col='current_stock_qty', avg_sales_col='rolling_avg_7d', new_col='stock_cover_days'):
    """
    Adds the stock cover days feature: current stock divided by average daily sales.

    Parameters:
    - df: pandas DataFrame with stock and sales columns
    - stock_col: column with current stock quantity (default 'current_stock_qty')
    - avg_sales_col: column with average daily sales (default 'rolling_avg_7d')
    - new_col: name of new feature column (default 'stock_cover_days')

    Returns:
    - DataFrame with stock_cover_days column added (float), NaN if avg_sales_col is zero or missing
    """
    df = df.copy()
    # Avoid division by zero or missing values
    df[new_col] = df[stock_col] / df[avg_sales_col].replace(0, pd.NA)
    return df

def add_safety_stock_threshold(df, avg_sales_col= 'rolling_avg_15d', safety_factor= ( 15/100 ), new_col='safety_stock_threshold'):
    """
    Adds a safety stock threshold feature using business rule:
    safety_stock_threshold = safety_factor * avg sales over 15 days.

    Parameters:
    - df: pandas DataFrame with rolling average sales
    - avg_sales_col: column with 15-day avg sales (default 'rolling_avg_15d')
    - safety_factor: multiplier for safety stock (default 1.5)
    - new_col: name of the new feature column (default 'safety_stock_threshold')

    Returns:
    - DataFrame with safety_stock_threshold column added (float)
    """
    df = df.copy()
    df[new_col] = df[avg_sales_col] * safety_factor
    return df