"""
this file creaters the featuers of the time-calendar image founded in the whatsapp group 

feature_name         | type        | description
---------------------|-------------|------------------------------------------------------------
day_of_week          | category    | Day of the week (Monday to Sunday), captures weekly patterns.
week_of_year         | numeric     | Week number (1-52), useful for seasonal trend detection.
month                | numeric     | Month number (1-12), captures monthly seasonality.
is_weekend           | boolean     | True if day is Friday or Saturday (weekend in Egypt).
is_start_of_month    | boolean     | True if day = 1; reflects salary/payment-driven behavior.
is_end_of_month      | boolean     | True if day is last day of month; budget constraints effect.
is_ramadan           | boolean     | True during the Islamic month of Ramadan; major retail shifts.
is_eid_fitr          | boolean     | True on Eid al-Fitr; significant gifting and food demand spike.
is_eid_adha          | boolean     | True on Eid al-Adha; demand for meat and family gatherings.
is_great_lent        | boolean     | True during 55 days before Coptic Easter; fasting affects consumption.
is_advent_fast       | boolean     | True during 43 days before Coptic Christmas (Jan 7); fasting period.
is_exam_period       | boolean     | True during exam months (typically Jan and May/June); affects spending.
is_national_holiday  | boolean     | True on Egyptian national holidays (Jan 25, Apr 25, Jul 23, Oct 6).
season               | category    | Meteorological season: one of ['winter', 'spring', 'summer', 'autumn'].
retail_event         | category    | Major retail campaigns: one active per date from 
                     |             | ['none', 'christmas_dec', 'coptic_christmas', 'valentines', 'mothers_day', 'black_friday', 'back_to_school'].
"""
from datetime import datetime
import pandas as pd

def add_day_of_week_feature(df, date_col='Date', new_col='day_of_week'):
    """
    Adds a 'day_of_week' categorical feature to the DataFrame based on a datetime column.

    Parameters:
    - df: pandas DataFrame containing the data
    - date_col: name of the datetime column to extract the day from (default 'Date')
    - new_col: name of the new feature column to create (default 'day_of_week')

    Returns:
    - DataFrame with the new categorical day_of_week column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = df[date_col].dt.day_name().astype('category')
    return df

def add_week_of_year_feature(df, date_col= 'Date', new_col = "week_of_year" ):
   """  Adds a 'week_of_year' numerical feature to the DataFrame based on a datetime column 
   Parameters:
    - df: pandas DataFrame containing the data
    - date_col: name of the datetime column to extract the day from (default 'Date')
    - new_col: name of the new feature column to create (default 'day_of_week')

    Returns:
    - DataFrame with the numerical  week_of_year column added
    """
   
   df = df.copy()
   df[date_col] = pd.to_datetime(df[date_col])
   df[new_col] = df[date_col].dt.isocalendar().week.astype(int)
   return df

def add_month_feature(df, date_col='Date', new_col='month'):   

    """
    Adds a numeric 'month' feature (1-12) to the DataFrame based on a datetime column.

    Parameters:
    - df: pandas DataFrame containing the data
    - date_col: name of the datetime column to extract the month from (default 'Date')
    - new_col: name of the new feature column to create (default 'month')

    Returns:
    - DataFrame with the numeric month column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = df[date_col].dt.month.astype(int)
    return df
   
def add_is_weekend_feature(df, date_col='Date', new_col='is_weekend'):
    """
    Adds a boolean 'is_weekend' feature to the DataFrame based on the datetime column.
    Marks True if the day is Friday or Saturday (Egypt weekend).

    Parameters:
    - df: pandas DataFrame containing the data
    - date_col: name of the datetime column to check (default 'Date')
    - new_col: name of the new boolean feature column (default 'is_weekend')

    Returns:
    - DataFrame with the boolean is_weekend column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    # dt.weekday: Monday=0 ... Sunday=6
    df[new_col] = df[date_col].dt.weekday.isin([4, 5])  # Friday=4, Saturday=5
    return df

def add_is_start_of_month_feature(df, date_col='Date', new_col='is_start_of_month'):
    """
    Adds a boolean 'is_start_of_month' feature: True if day == 1.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column name
    - new_col: new boolean column name

    Returns:
    - DataFrame with the new feature
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = df[date_col].dt.day == 1
    return df

def add_is_end_of_month_feature(df, date_col='Date', new_col='is_end_of_month'):


    """
    Adds a boolean 'is_end_of_month' feature: True if day is last day of month.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column name
    - new_col: new boolean column name

    Returns:
    - DataFrame with the new feature
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = df[date_col].dt.is_month_end
    return df  

def add_is_ramadan_feature(df, date_col='Date', new_col='is_ramadan'):
    """
    Adds a boolean 'is_ramadan' feature to the DataFrame.
    Returns True if the date falls within the Ramadan period (Gregorian calendar, hardcoded for 2020–2035).

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column to evaluate
    - new_col: name of the new boolean feature column

    Returns:
    - DataFrame with the is_ramadan column added
    """
    # Ramadan ranges in Gregorian calendar: (start_date, end_date)
    ramadan_ranges = [
        ("2020-04-24", "2020-05-23"),
        ("2021-04-13", "2021-05-12"),
        ("2022-04-02", "2022-05-01"),
        ("2023-03-23", "2023-04-21"),
        ("2024-03-10", "2024-04-09"),
        ("2025-02-28", "2025-03-29"),
        ("2026-02-17", "2026-03-18"),
        ("2027-02-07", "2027-03-08"),
        ("2028-01-27", "2028-02-25"),
        ("2029-01-15", "2029-02-13"),
        ("2030-01-05", "2030-02-03"),
        ("2030-12-26", "2031-01-24"),
        ("2031-12-15", "2032-01-13"),
        ("2032-12-03", "2033-01-01"),
        ("2033-11-23", "2033-12-22"),
        ("2034-11-11", "2034-12-10"),
        ("2035-11-01", "2035-11-30"),
    ]
    
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = False
    
    for start, end in ramadan_ranges:
        mask = (df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))
        df.loc[mask, new_col] = True

    return df

def add_is_eid_fitr_feature(df, date_col='Date', new_col='is_eid_fitr'):
    """
    Adds a boolean 'is_eid_fitr' feature to the DataFrame.
    Returns True if the date falls within Eid al-Fitr (3-day period after Ramadan) from 2020–2035.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column to evaluate
    - new_col: name of the new boolean feature column

    Returns:
    - DataFrame with the is_eid_fitr column added
    """
    # Eid al-Fitr periods: 3 days after each Ramadan ends
    eid_fitr_ranges = [
        ("2020-05-24", "2020-05-26"),
        ("2021-05-13", "2021-05-15"),
        ("2022-05-02", "2022-05-04"),
        ("2023-04-21", "2023-04-23"),
        ("2024-04-10", "2024-04-12"),
        ("2025-03-30", "2025-04-01"),
        ("2026-03-19", "2026-03-21"),
        ("2027-03-09", "2027-03-11"),
        ("2028-02-26", "2028-02-28"),
        ("2029-02-14", "2029-02-16"),
        ("2030-02-04", "2030-02-06"),
        ("2031-01-25", "2031-01-27"),
        ("2032-01-14", "2032-01-16"),
        ("2033-01-02", "2033-01-04"),
        ("2033-12-23", "2033-12-25"),
        ("2034-12-11", "2034-12-13"),
        ("2035-12-01", "2035-12-03"),
    ]
    
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = False

    for start, end in eid_fitr_ranges:
        mask = (df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))
        df.loc[mask, new_col] = True

    return df

def add_is_eid_adha_feature(df, date_col='Date', new_col='is_eid_adha'):
    """
    Adds a boolean 'is_eid_adha' feature to the DataFrame.
    Returns True if the date falls within Eid al-Adha (4-day period) from 2020–2035.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column to evaluate
    - new_col: name of the new boolean feature column

    Returns:
    - DataFrame with the is_eid_adha column added
    """
    # Eid al-Adha periods: typically 4 days starting 10th of Dhul-Hijjah
    eid_adha_ranges = [
        ("2020-07-31", "2020-08-03"),
        ("2021-07-20", "2021-07-23"),
        ("2022-07-09", "2022-07-12"),
        ("2023-06-28", "2023-07-01"),
        ("2024-06-16", "2024-06-19"),
        ("2025-06-06", "2025-06-09"),
        ("2026-05-27", "2026-05-30"),
        ("2027-05-17", "2027-05-20"),
        ("2028-05-05", "2028-05-08"),
        ("2029-04-24", "2029-04-27"),
        ("2030-04-14", "2030-04-17"),
        ("2031-04-04", "2031-04-07"),
        ("2032-03-23", "2032-03-26"),
        ("2033-03-12", "2033-03-15"),
        ("2034-03-01", "2034-03-04"),
        ("2035-02-18", "2035-02-21"),
    ]

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = False

    for start, end in eid_adha_ranges:
        mask = (df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))
        df.loc[mask, new_col] = True

    return df

def add_is_great_lent_feature(df, date_col='Date', new_col='is_great_lent'):
    """
    Adds a boolean 'is_great_lent' feature indicating whether the date falls within
    the Coptic Orthodox Great Lent (55-day fast before Easter) for years 2020–2035.

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column
    - new_col: name of the new boolean feature column

    Returns:
    - DataFrame with the is_great_lent column added
    """
    lent_periods = [
        ("2020-02-24", "2020-04-18"),
        ("2021-03-08", "2021-05-01"),
        ("2022-02-28", "2022-04-23"),
        ("2023-03-06", "2023-04-15"),
        ("2024-03-18", "2024-05-11"),
        ("2025-03-03", "2025-04-26"),
        ("2026-02-16", "2026-04-11"),
        ("2027-03-08", "2027-05-01"),
        ("2028-02-21", "2028-04-15"),
        ("2029-03-05", "2029-04-28"),
        ("2030-02-18", "2030-04-13"),
        ("2031-03-10", "2031-05-03"),
        ("2032-02-23", "2032-04-17"),
        ("2033-03-07", "2033-04-30"),
        ("2034-02-20", "2034-04-15"),
        ("2035-03-05", "2035-04-28"),
    ]

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df[new_col] = False

    for start, end in lent_periods:
        mask = (df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))
        df.loc[mask, new_col] = True

    return df
    

def is_national_holiday(df, date_col="Date", new_col="is_national_holiday"):
    """
    Adds a boolean column indicating if the date is an Egyptian national holiday.
    
    Parameters:
    - df: pandas DataFrame containing the data
    - date_col: name of the datetime column to extract the date from
    - new_col: name of the new feature column to create
    
    Returns:
    - DataFrame with the boolean national holiday column added
    """
    df = df.copy()
    # Ensure the column is in datetime format
    df[date_col] = pd.to_datetime(df[date_col])

    # Fixed-date national holidays
    fixed_holidays = [
        (1, 7),   # Coptic Christmas
        (1, 25),  # Revolution/Police Day
        (4, 25),  # Sinai Liberation Day
        (5, 1),   # Labor Day
        (6, 30),  # June 30 Revolution
        (7, 23),  # 1952 Revolution Day
        (10, 6),  # Armed Forces Day
    ]

    df[new_col] = df[date_col].apply(lambda x: (x.month, x.day) in fixed_holidays)

    return df

def add_season_feature(df, date_col='Date', new_col='season'):
    """
    Adds a categorical 'season' feature based on meteorological seasons:
    Winter (Dec-Feb), Spring (Mar-May), Summer (Jun-Aug), Autumn (Sep-Nov).

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column name
    - new_col: name of the new categorical column to create

    Returns:
    - DataFrame with the season column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    def get_season(month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'autumn'

    df[new_col] = df[date_col].dt.month.apply(get_season).astype('category')

    return df

def add_retail_event_feature(df, date_col='Date', new_col='retail_event'):
    """
    Adds a categorical 'retail_event' feature indicating major retail campaigns.
    Only one event active per date. Defaults to 'none'.

    Events:
    - christmas_dec: December 1–31
    - coptic_christmas: January 7
    - valentines: February 14
    - mothers_day: March 21 (Egypt)
    - black_friday: Last Friday of November
    - back_to_school: August 15–31

    Parameters:
    - df: pandas DataFrame
    - date_col: datetime column name
    - new_col: new categorical feature name

    Returns:
    - DataFrame with the retail_event column added
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    def get_retail_event(date):
        month = date.month
        day = date.day
        weekday = date.weekday()  # Monday=0 ... Sunday=6

        # Christmas Dec
        if month == 12:
            return 'christmas_dec'

        # Coptic Christmas
        if month == 1 and day == 7:
            return 'coptic_christmas'

        # Valentines
        if month == 2 and day == 14:
            return 'valentines'

        # Mothers Day Egypt (March 21)
        if month == 3 and day == 21:
            return 'mothers_day'

        # Black Friday (last Friday of November)
        if month == 11 and weekday == 4:  # Friday
            # Check if this Friday is the last Friday of November
            next_week = date + pd.Timedelta(days=7)
            if next_week.month != 11:
                return 'black_friday'

        # Back to school (Aug 15 - Aug 31)
        if month == 8 and 15 <= day <= 31:
            return 'back_to_school'

        return 'none'

    df[new_col] = df[date_col].apply(get_retail_event).astype('category')
    return df





