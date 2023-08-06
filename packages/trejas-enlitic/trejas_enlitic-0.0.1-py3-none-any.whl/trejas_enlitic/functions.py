from dateutil.parser import parse
import pandas as pd
import datetime


def parse_timestamp_string_to_unix_time(date_time_str):
    return parse(date_time_str)


def transform_line(line: str) -> tuple:
    """ Transforms a data line from the log format presented.
    Args:
        line: line of data from the log.
    Returns:
        tuple of timestamp, severity, code, user from the log line.
    """
    data_elements = line.split("-")
    timestamp = parse_timestamp_string_to_unix_time(data_elements[0])
    data_elements = data_elements[1].split(" ")
    code = data_elements[0]
    if len(data_elements) > 1:
        user = data_elements[1]
    else:
        user = None
    codes = code.split(":")
    severity = codes[0]
    code = codes[1]
    return timestamp, severity, code, user


def ingest_logs(data: list) -> pd.DataFrame:
    """ Ingests logs from a list of log lines.
    Args:
        data: list of data lines.
    Returns:
        pd.DataFrame
    """
    return pd.DataFrame(
        [*[transform_line(line) for line in data]],
        columns=["timestamp", "severity", "code", "user"],
    )


def filter_by_timestamp_window(
    df: pd.DataFrame, query_timestamp: str, delta: int
) -> pd.DataFrame:
    """ Creates a filtered dataframe using an input timestamp and a delta.
    Args:
        df: Pandas dataframe to filter
        query_timestamp: timestamp string to use for the logs query.
        delta: the delta to use for timestamp filter
    Returns:
        pd.DataFrame
    """
    return (
        df.loc[
            (
                df["timestamp"]
                >= parse_timestamp_string_to_unix_time(query_timestamp)
                - datetime.timedelta(seconds=int(delta))
            )
            & (df["timestamp"] <= parse_timestamp_string_to_unix_time(query_timestamp))
        ]
        .groupby(["severity", "code", "user"], dropna=False)
        .count()
    )


def display_stats_for_timestamp(
    log_array: list, query_timestamp: str, splits: list = [5, 10, 15]
) -> pd.DataFrame:
    """ Generates a dataframe that contains the reported stats for a list of time splits

    Args:
        query_timestamp: timestamp string to use for the logs query.
        splits: List of ints, these are the times, in seconds to use to split the logs.
    
    Returns:
        pd.DataFrame
    """
    report_df = pd.DataFrame({"severity": [], "code": [], "timestamp": [], "user": []})
    for split in splits:
        temp_df = filter_by_timestamp_window(log_array, query_timestamp, split)
        temp_df = temp_df.rename(columns={"timestamp": f"{split}s"})
        if report_df.empty:
            report_df = temp_df
        else:
            report_df = report_df.merge(temp_df, on=["severity", "code", "user"])
    return report_df
