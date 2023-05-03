"""Data processing module"""

from pathlib import Path

import pandas as pd


def load_air_quality(file_path: Path) -> pd.DataFrame:
    """
    Load and process air quality data set.

    Source: https://archive.ics.uci.edu/ml/datasets/Air+Quality

    The dataset was collected between January 2004 and March 2005.
    It consists of hourly measurements of the different air pollutants, NO2, NOX, CO, C6H6, O3 and NMHC. The measurements are accompanied by local temperature and humidity values, also recorded hourly.
    In the data collection experiments, scientists were testing new pollutant sensors. The values from the new sensors are stored in the variables called _sensors.
    For comparison, data for the pollutants was also gathered from fixed stations, that regularly measure the concentration of these gases. Those values are stored in the variables called _true.

    :param file_path: Path to the data file
    :return: Processed data frame
    """

    # Load and parse original csv file
    df = pd.read_csv(file_path, sep=";", parse_dates=[["Date", "Time"]]).iloc[:, :-2]
    df = df.dropna()

    # Rename columns
    date_col = "date_time"
    column_mapping = {
        "Date_Time": date_col,
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

    # Process datetimes
    df[df[date_col].apply(lambda x: len(x)) > 19]
    df[date_col] = df[date_col].str.replace(".", ":", regex=True)
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col).sort_index()

    # Reduce data span (poor data quality outside these dates)
    return df.loc["2004-04-04":"2005-04-04"]
