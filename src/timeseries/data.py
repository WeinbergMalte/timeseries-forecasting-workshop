"""Data processing module"""

from pathlib import Path

import pandas as pd


def load_airline(file_path: Path) -> pd.DataFrame:
    """
    Load airline passengers time series data set.
    Source: Unknown

    :param file_path: Path to the data file
    :return: Processed data frame
    """
    df = pd.read_csv(file_path, parse_dates=["month"]).set_index("month")
    df.index.freq = pd.infer_freq(df.index)
    return df


def load_sunspots(file_path: Path) -> pd.DataFrame:
    """
    Load sunsplots time series data set.
    Source: https://www.ngdc.noaa.gov/stp/solar/ssndata.html

    :param file_path: Path to the data file
    :return: Processed data frame
    """
    df = pd.read_csv(file_path, parse_dates=["date"])
    df["date"] = df["date"].dt.to_period("M")
    return df.set_index("date")


def load_retail(file_path: Path) -> pd.DataFrame:
    """
    Load univariate online retail data set.
    Source: "https://raw.githubusercontent.com/facebook/prophet/master/examples/example_retail_sales.csv"

    :param file_path: Path to the data file
    :return: Processed data frame
    """
    return pd.read_csv(file_path, parse_dates=["month"]).set_index("month").sort_index()


def load_air_quality(file_path: Path) -> pd.DataFrame:
    """
    Load and process air quality data set.

    Source: https://archive.ics.uci.edu/ml/datasets/Air+Quality

    The dataset was collected between January 2004 and March 2005.
    It consists of hourly measurements of the different air pollutants, NO2, NOX, CO, C6H6, O3 and NMHC.
    The measurements are accompanied by local temperature and humidity values, also recorded hourly.
    In the data collection experiments, scientists were testing new pollutant sensors.
    The values from the new sensors are stored in the variables called _sensors.
    For comparison, data for the pollutants was also gathered from fixed stations, that regularly measure the concentration of these gases.
    Those values are stored in the variables called _true.

    :param file_path: Path to the data file
    :return: Processed data frame
    """
    DATE_COL = "date_time"

    # Load and parse original csv file
    df = pd.read_csv(file_path, sep=";").iloc[:, :-2]
    df[DATE_COL] = pd.to_datetime(
        df["Date"] + " " + df["Time"], format="%d/%m/%Y %H.%M.%S"
    )
    df = df.drop(columns=["Date", "Time"])
    df = df.set_index(DATE_COL).sort_index()
    df = df.dropna()

    # Rename columns
    column_mapping = {
        "CO(GT)": "co_true",
        "PT08.S1(CO)": "co_sensor",
        "NMHC(GT)": "nmhc_true",
        "C6H6(GT)": "c6h6_true",
        "PT08.S2(NMHC)": "nmhc_sensor",
        "NOx(GT)": "nox_true",
        "PT08.S3(NOx)": "nox_sensor",
        "NO2(GT)": "no2_true",
        "PT08.S4(NO2)": "no2_sensor",
        "PT08.S5(O3)": "o3_sensor",
        "T": "t",
        "RH": "humidity",
        "AH": "ah",
    }
    df = df.rename(columns=column_mapping)

    # Process predictor columns
    predictors = df.columns[1:]
    for var in predictors:
        if df[var].dtype != "O":
            continue
        df[var] = df[var].str.replace(",", ".")
        df[var] = pd.to_numeric(df[var])

    # Reduce data span (poor data quality outside these dates)
    df = df[df.index >= "2004-04-04"]
    df = df[df.index <= "2005-04-04"]

    return df
