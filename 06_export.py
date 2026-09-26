import pandas as pd
import numpy as np

from config import (
    DESTINATION,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
    MYSQL_TABLE,
    MONGO_URI,
    MONGO_DATABASE,
    MONGO_COLLECTION,
    EXCEL_OUTPUT_FILE
)

import mysql.connector
from pymongo import MongoClient


def export_log(message):
    print(message)


def prepare_export_data(dataframe):
    data = dataframe.copy()

    data = data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    for column in data.select_dtypes(
        include=["datetime64[ns]"]
    ).columns:
        data[column] = data[column].dt.strftime(
            "%Y-%m-%d"
        )

    data = data.fillna("")

    return data


def validate_export_data(dataframe):
    if dataframe is None:
        raise ValueError(
            "Export DataFrame cannot be None."
        )

    if dataframe.empty:
        raise ValueError(
            "Export DataFrame is empty."
        )

    if len(dataframe.columns) == 0:
        raise ValueError(
            "Export DataFrame has no columns."
        )

    return True


def export_to_excel(dataframe):
    export_log(
        "\nStarting Excel export..."
    )

    data = prepare_export_data(
        dataframe
    )

    data.to_excel(
        EXCEL_OUTPUT_FILE,
        index=False,
        engine="openpyxl"
    )

    export_log(
        f"Excel file created: "
        f"{EXCEL_OUTPUT_FILE}"
    )

    export_log(
        f"Rows exported: {len(data)}"
    )

    export_log(
        f"Columns exported: {len(data.columns)}"
    )

    return EXCEL_OUTPUT_FILE


def create_mysql_table(connection):
    cursor = connection.cursor()

    columns = [
        "customer_id VARCHAR(50)",
        "customer_name VARCHAR(255)",
        "country VARCHAR(100)",
        "signup_date DATE",
        "plan VARCHAR(100)",
        "monthly_spend DOUBLE",
        "total_orders INT",
        "total_spend DOUBLE",
        "last_purchase_date DATE",
        "support_tickets INT",
        "avg_session_minutes DOUBLE",
        "feature_usage_count INT",
        "churned INT",
        "product_category VARCHAR(150)",
        "rating DOUBLE",
        "sentiment VARCHAR(50)",
        "feedback TEXT",
        "predicted_churn INT",
        "churn_probability DOUBLE",
        "churn_risk VARCHAR(50)",
        "customer_segment INT",
        "recommended_action TEXT",
        "customer_lifetime_days INT",
        "average_order_value DOUBLE"
    ]

    query = f"""
    CREATE TABLE IF NOT EXISTS `{MYSQL_TABLE}` (
        {", ".join(columns)}
    )
    """

    cursor.execute(query)

    connection.commit()

    cursor.close()


def export_to_mysql(dataframe):
    export_log(
        "\nStarting MySQL export..."
    )

    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

    create_mysql_table(
        connection
    )

    cursor = connection.cursor()

    columns = [
        "customer_id",
        "customer_name",
        "country",
        "signup_date",
        "plan",
        "monthly_spend",
        "total_orders",
        "total_spend",
        "last_purchase_date",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count",
        "churned",
        "product_category",
        "rating",
        "sentiment",
        "feedback",
        "predicted_churn",
        "churn_probability",
        "churn_risk",
        "customer_segment",
        "recommended_action",
        "customer_lifetime_days",
        "average_order_value"
    ]

    available_columns = [
        column
        for column in columns
        if column in dataframe.columns
    ]

    data = dataframe[
        available_columns
    ].copy()

    for column in data.columns:
        if pd.api.types.is_datetime64_any_dtype(
            data[column]
        ):
            data[column] = data[column].dt.date

    column_names = ", ".join(
        f"`{column}`"
        for column in available_columns
    )

    placeholders = ", ".join(
        ["%s"] * len(available_columns)
    )

    query = f"""
    INSERT INTO `{MYSQL_TABLE}`
    ({column_names})
    VALUES ({placeholders})
    """

    rows = []

    for _, row in data.iterrows():

        values = []

        for column in available_columns:

            value = row[column]

            if pd.isna(value):
                value = None

            values.append(value)

        rows.append(
            tuple(values)
        )

    cursor.executemany(
        query,
        rows
    )

    connection.commit()

    cursor.close()
    connection.close()

    export_log(
        f"MySQL rows exported: {len(rows)}"
    )

    return len(rows)


def prepare_mongodb_document(row):
    document = {}

    for column, value in row.items():

        if pd.isna(value):
            document[column] = None

        elif isinstance(
            value,
            np.integer
        ):
            document[column] = int(value)

        elif isinstance(
            value,
            np.floating
        ):
            document[column] = float(value)

        elif isinstance(
            value,
            np.bool_
        ):
            document[column] = bool(value)

        elif isinstance(
            value,
            pd.Timestamp
        ):
            document[column] = value.to_pydatetime()

        else:
            document[column] = value

    return document


def export_to_mongodb(dataframe):
    export_log(
        "\nStarting MongoDB export..."
    )

    client = MongoClient(
        MONGO_URI
    )

    database = client[
        MONGO_DATABASE
    ]

    collection = database[
        MONGO_COLLECTION
    ]

    documents = []

    for _, row in dataframe.iterrows():

        document = prepare_mongodb_document(
            row
        )

        documents.append(
            document
        )

    if documents:

        collection.delete_many({})

        result = collection.insert_many(
            documents
        )

        exported_count = len(
            result.inserted_ids
        )

    else:
        exported_count = 0

    client.close()

    export_log(
        f"MongoDB documents exported: "
        f"{exported_count}"
    )

    return exported_count


def create_export_summary(
    dataframe,
    destination,
    output_reference
):
    summary = {
        "destination": destination,
        "rows_exported": int(
            len(dataframe)
        ),
        "columns_exported": int(
            len(dataframe.columns)
        ),
        "columns": list(
            dataframe.columns
        ),
        "output": str(
            output_reference
        )
    }

    return summary


def display_export_summary(summary):
    print("\n" + "=" * 65)
    print(
        "PRODUCTPULSE AI - EXPORT SUMMARY"
    )
    print("=" * 65)

    print(
        f"Destination       : "
        f"{summary['destination']}"
    )

    print(
        f"Rows Exported     : "
        f"{summary['rows_exported']}"
    )

    print(
        f"Columns Exported  : "
        f"{summary['columns_exported']}"
    )

    print(
        f"Output Reference  : "
        f"{summary['output']}"
    )

    print(
        "\nExport completed successfully."
    )


def run_export_pipeline(dataframe):
    validate_export_data(
        dataframe
    )

    print("\n" + "=" * 65)
    print(
        "PRODUCTPULSE AI - DATA EXPORT ENGINE"
    )
    print("=" * 65)

    if DESTINATION == "EXCEL":

        output = export_to_excel(
            dataframe
        )

    elif DESTINATION == "MYSQL":

        output = export_to_mysql(
            dataframe
        )

    elif DESTINATION == "MONGODB":

        output = export_to_mongodb(
            dataframe
        )

    else:

        raise ValueError(
            "Invalid DESTINATION. "
            "Use EXCEL, MYSQL or MONGODB."
        )

    summary = create_export_summary(
        dataframe,
        DESTINATION,
        output
    )

    display_export_summary(
        summary
    )

    return summary


if __name__ == "__main__":

    print(
        "\n06_export.py is ready."
    )

    print(
        "This module exports the final "
        "enriched dataset."
    )

    print(
        "Destination is controlled through "
        "config.py."
    )