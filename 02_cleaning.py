import pandas as pd
import numpy as np



def cleaning_log(message):
    """
    Prints a formatted cleaning message.
    """

    print(message)


def get_dataset_snapshot(dataframe):
    """
    Returns basic dataset quality information.
    """

    snapshot = {
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "missing_values": int(dataframe.isnull().sum().sum()),
        "duplicate_rows": int(dataframe.duplicated().sum())
    }

    return snapshot


def remove_duplicates(dataframe):
    """
    Removes completely duplicated rows.
    """

    before = len(dataframe)

    dataframe = dataframe.drop_duplicates().copy()

    after = len(dataframe)

    removed = before - after

    cleaning_log(
        f"Duplicate rows removed : {removed}"
    )

    return dataframe



def clean_text_columns(dataframe):
    """
    Cleans unnecessary spaces from text columns.
    """

    text_columns = dataframe.select_dtypes(
        include=["object"]
    ).columns

    for column in text_columns:

        dataframe[column] = (
            dataframe[column]
            .astype("string")
            .str.strip()
        )

        dataframe[column] = (
            dataframe[column]
            .replace({
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
                "NULL": pd.NA
            })
        )

    cleaning_log(
        f"Text columns cleaned      : {len(text_columns)}"
    )

    return dataframe


def standardize_column_names(dataframe):
    """
    Makes column names consistent and analysis-friendly.
    """

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    cleaning_log(
        "Column names standardized  : YES"
    )

    return dataframe



def convert_date_columns(dataframe):
    """
    Converts known date columns into datetime format.
    """

    date_columns = [
        "signup_date",
        "last_purchase_date"
    ]

    converted = 0

    for column in date_columns:

        if column in dataframe.columns:

            dataframe[column] = pd.to_datetime(
                dataframe[column],
                errors="coerce"
            )

            converted += 1

    cleaning_log(
        f"Date columns converted    : {converted}"
    )

    return dataframe



def convert_numeric_columns(dataframe):
    """
    Converts known numeric columns into numeric types.
    """

    numeric_columns = [
        "monthly_spend",
        "total_orders",
        "total_spend",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count",
        "churned",
        "rating"
    ]

    converted = 0

    for column in numeric_columns:

        if column in dataframe.columns:

            dataframe[column] = pd.to_numeric(
                dataframe[column],
                errors="coerce"
            )

            converted += 1

    cleaning_log(
        f"Numeric columns converted : {converted}"
    )

    return dataframe



def handle_missing_values(dataframe):
    """
    Handles missing values according to column type.

    Numeric columns:
        Median imputation

    Text columns:
        'Unknown'

    Date columns:
        Forward fill followed by backward fill
    """

    missing_before = int(
        dataframe.isnull().sum().sum()
    )

    numeric_columns = dataframe.select_dtypes(
        include=["number"]
    ).columns

    text_columns = dataframe.select_dtypes(
        include=["object", "string"]
    ).columns

    date_columns = dataframe.select_dtypes(
        include=["datetime64[ns]"]
    ).columns


    for column in numeric_columns:

        if dataframe[column].isnull().any():

            median_value = dataframe[column].median()

            dataframe[column] = dataframe[column].fillna(
                median_value
            )

    for column in text_columns:

        if dataframe[column].isnull().any():

            dataframe[column] = dataframe[column].fillna(
                "Unknown"
            )

    for column in date_columns:

        if dataframe[column].isnull().any():

            dataframe[column] = (
                dataframe[column]
                .ffill()
                .bfill()
            )

    missing_after = int(
        dataframe.isnull().sum().sum()
    )

    cleaning_log(
        f"Missing values            : "
        f"{missing_before} → {missing_after}"
    )

    return dataframe



def validate_business_values(dataframe):
    """
    Checks important ProductPulse business fields
    for invalid values.
    """

    corrections = 0


    if "rating" in dataframe.columns:

        invalid_rating = ~dataframe["rating"].between(
            1,
            5
        )

        corrections += int(invalid_rating.sum())

        dataframe.loc[
            invalid_rating,
            "rating"
        ] = np.nan

        if invalid_rating.any():

            dataframe["rating"] = dataframe["rating"].fillna(
                dataframe["rating"].median()
            )


    if "churned" in dataframe.columns:

        invalid_churn = ~dataframe["churned"].isin(
            [0, 1]
        )

        corrections += int(invalid_churn.sum())

        dataframe.loc[
            invalid_churn,
            "churned"
        ] = 0

    # --------------------------------------------------------
    # Numeric business values cannot be negative
    # --------------------------------------------------------

    non_negative_columns = [
        "monthly_spend",
        "total_orders",
        "total_spend",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count"
    ]

    for column in non_negative_columns:

        if column in dataframe.columns:

            invalid_values = dataframe[column] < 0

            corrections += int(
                invalid_values.sum()
            )

            dataframe.loc[
                invalid_values,
                column
            ] = 0

    cleaning_log(
        f"Business-value corrections: {corrections}"
    )

    return dataframe


def normalize_sentiment(dataframe):
    """
    Standardizes sentiment values.
    """

    if "sentiment" not in dataframe.columns:

        return dataframe

    dataframe["sentiment"] = (
        dataframe["sentiment"]
        .astype("string")
        .str.strip()
        .str.title()
    )

    valid_sentiments = [
        "Positive",
        "Negative",
        "Neutral"
    ]

    invalid_sentiment = ~dataframe[
        "sentiment"
    ].isin(valid_sentiments)

    dataframe.loc[
        invalid_sentiment,
        "sentiment"
    ] = "Unknown"

    cleaning_log(
        "Sentiment values normalized: YES"
    )

    return dataframe



def check_data_types(dataframe):
    """
    Displays final data types after cleaning.
    """

    print("\n" + "=" * 65)
    print("FINAL DATA TYPES")
    print("=" * 65)

    print(
        dataframe.dtypes.to_string()
    )



def display_cleaning_summary(
    before_snapshot,
    after_snapshot
):
    """
    Displays before/after cleaning metrics.
    """

    print("\n" + "=" * 65)
    print("DATA CLEANING SUMMARY")
    print("=" * 65)

    print(
        f"Rows              : "
        f"{before_snapshot['rows']} → "
        f"{after_snapshot['rows']}"
    )

    print(
        f"Columns           : "
        f"{before_snapshot['columns']} → "
        f"{after_snapshot['columns']}"
    )

    print(
        f"Missing values    : "
        f"{before_snapshot['missing_values']} → "
        f"{after_snapshot['missing_values']}"
    )

    print(
        f"Duplicate rows    : "
        f"{before_snapshot['duplicate_rows']} → "
        f"{after_snapshot['duplicate_rows']}"
    )


def clean_data(dataframe):
    """
    Complete ProductPulse data-cleaning pipeline.

    Returns:
        Cleaned Pandas DataFrame
    """

    if dataframe is None:

        raise ValueError(
            "Input DataFrame cannot be None."
        )

    if dataframe.empty:

        raise ValueError(
            "Input DataFrame is empty."
        )

    print("\n" + "=" * 65)
    print("PRODUCTPULSE AI - DATA CLEANING ENGINE")
    print("=" * 65)


    before_snapshot = get_dataset_snapshot(
        dataframe
    )

    print("\nBEFORE CLEANING")
    print("-" * 65)

    print(
        f"Rows           : "
        f"{before_snapshot['rows']}"
    )

    print(
        f"Columns        : "
        f"{before_snapshot['columns']}"
    )

    print(
        f"Missing values : "
        f"{before_snapshot['missing_values']}"
    )

    print(
        f"Duplicates     : "
        f"{before_snapshot['duplicate_rows']}"
    )


    dataframe = standardize_column_names(
        dataframe
    )

    dataframe = clean_text_columns(
        dataframe
    )

    dataframe = convert_date_columns(
        dataframe
    )

    dataframe = convert_numeric_columns(
        dataframe
    )

    dataframe = remove_duplicates(
        dataframe
    )

    dataframe = handle_missing_values(
        dataframe
    )

    dataframe = validate_business_values(
        dataframe
    )

    dataframe = normalize_sentiment(
        dataframe
    )


    after_snapshot = get_dataset_snapshot(
        dataframe
    )

    display_cleaning_summary(
        before_snapshot,
        after_snapshot
    )

    check_data_types(
        dataframe
    )

    print("\n" + "=" * 65)
    print("DATA CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 65)

    return dataframe



if __name__ == "__main__":

    print(
        "\n02_cleaning.py is ready."
    )

    print(
        "This module receives a Pandas DataFrame "
        "from 01_ingestion.py."
    )

    print(
        "Run the complete pipeline after all modules "
        "are connected."
    )