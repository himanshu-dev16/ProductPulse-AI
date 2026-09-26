import os
import sys
import pandas as pd

from config import (
    SOURCE,

    # MySQL
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_DATABASE,
    MYSQL_TABLE,

    # MongoDB
    MONGO_URI,
    MONGO_DATABASE,
    MONGO_COLLECTION,

    # Excel
    EXCEL_INPUT_FILE,

    # General
    PREVIEW_ROWS,
    SHOW_INGESTION_LOGS
)


def log(message):
    """
    Prints ingestion messages when logging is enabled.
    """

    if SHOW_INGESTION_LOGS:
        print(message)


def load_from_mysql():
    """
    Loads ProductPulse data from MySQL into a Pandas DataFrame.
    """

    log("\n" + "=" * 65)
    log("MYSQL DATA INGESTION")
    log("=" * 65)

    try:
        import mysql.connector

        log(f"Connecting to MySQL server: {MYSQL_HOST}:{MYSQL_PORT}")
        log(f"Database: {MYSQL_DATABASE}")
        log(f"Table: {MYSQL_TABLE}")

        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        if connection.is_connected():
            log("MySQL connection successful.")

        query = f"""
        SELECT *
        FROM `{MYSQL_TABLE}`
        """

        dataframe = pd.read_sql(query, connection)

        connection.close()

        log("MySQL connection closed.")
        log(f"Rows loaded: {len(dataframe)}")
        log(f"Columns loaded: {len(dataframe.columns)}")

        return dataframe

    except ImportError:
        print("\nERROR: mysql-connector-python is not installed.")
        print("Install it using:")
        print("pip install mysql-connector-python")
        sys.exit(1)

    except Exception as error:
        print("\nMYSQL INGESTION ERROR")
        print("-" * 65)
        print(error)
        sys.exit(1)



def load_from_mongodb():
    """
    Loads ProductPulse documents from MongoDB
    into a Pandas DataFrame.
    """

    log("\n" + "=" * 65)
    log("MONGODB DATA INGESTION")
    log("=" * 65)

    try:
        from pymongo import MongoClient

        log(f"Connecting to MongoDB: {MONGO_URI}")
        log(f"Database: {MONGO_DATABASE}")
        log(f"Collection: {MONGO_COLLECTION}")

        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verify server connectivity
        client.server_info()

        database = client[MONGO_DATABASE]
        collection = database[MONGO_COLLECTION]

        documents = list(
            collection.find(
                {},
                {"_id": 0}
            )
        )

        client.close()

        dataframe = pd.DataFrame(documents)

        log("MongoDB connection closed.")
        log(f"Documents loaded: {len(dataframe)}")
        log(f"Columns loaded: {len(dataframe.columns)}")

        return dataframe

    except ImportError:
        print("\nERROR: pymongo is not installed.")
        print("Install it using:")
        print("pip install pymongo")
        sys.exit(1)

    except Exception as error:
        print("\nMONGODB INGESTION ERROR")
        print("-" * 65)
        print(error)
        sys.exit(1)


def load_from_excel():
    """
    Loads ProductPulse data from an Excel file
    into a Pandas DataFrame.
    """

    log("\n" + "=" * 65)
    log("EXCEL DATA INGESTION")
    log("=" * 65)

    try:

        file_path = EXCEL_INPUT_FILE

        log(f"Excel file: {file_path}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Excel file not found: {file_path}"
            )

        dataframe = pd.read_excel(file_path)

        log("Excel file loaded successfully.")
        log(f"Rows loaded: {len(dataframe)}")
        log(f"Columns loaded: {len(dataframe.columns)}")

        return dataframe

    except ImportError:
        print("\nERROR: openpyxl is not installed.")
        print("Install it using:")
        print("pip install openpyxl")
        sys.exit(1)

    except Exception as error:
        print("\nEXCEL INGESTION ERROR")
        print("-" * 65)
        print(error)
        sys.exit(1)



def load_data():
    """
    Selects the correct data source according to
    SOURCE defined in config.py.
    """

    source = SOURCE.upper().strip()

    log("\n" + "=" * 65)
    log("PRODUCTPULSE AI - DATA INGESTION ENGINE")
    log("=" * 65)

    log(f"Selected source: {source}")

    if source == "MYSQL":

        # ====================================================
        # ACTIVE SOURCE: MYSQL
        # ====================================================

        dataframe = load_from_mysql()

        # ====================================================
        # OTHER SOURCES
        # Keep commented when MySQL is selected.
        # ====================================================

        # dataframe = load_from_mongodb()
        # dataframe = load_from_excel()

    elif source == "MONGODB":

        # ====================================================
        # ACTIVE SOURCE: MONGODB
        # ====================================================

        dataframe = load_from_mongodb()

        # ====================================================
        # OTHER SOURCES
        # Keep commented when MongoDB is selected.
        # ====================================================

        # dataframe = load_from_mysql()
        # dataframe = load_from_excel()

    elif source == "EXCEL":

        # ====================================================
        # ACTIVE SOURCE: EXCEL
        # ====================================================

        dataframe = load_from_excel()

        

        # dataframe = load_from_mysql()
        # dataframe = load_from_mongodb()

    else:

        print("\nINVALID DATA SOURCE")
        print("-" * 65)
        print("SOURCE must be one of:")
        print("MYSQL")
        print("MONGODB")
        print("EXCEL")
        sys.exit(1)

    return dataframe



def display_dataset_information(dataframe):
    """
    Displays basic information about the loaded dataset.
    """

    print("\n" + "=" * 65)
    print("DATASET INFORMATION")
    print("=" * 65)

    print(f"Total rows    : {dataframe.shape[0]}")
    print(f"Total columns : {dataframe.shape[1]}")

    print("\nColumn names:")
    print("-" * 65)

    for number, column in enumerate(dataframe.columns, start=1):
        print(f"{number:02d}. {column}")

    print("\nData types:")
    print("-" * 65)

    print(dataframe.dtypes)

    print("\nMissing values:")
    print("-" * 65)

    missing_values = dataframe.isnull().sum()

    for column, count in missing_values.items():
        print(f"{column}: {count}")



def display_preview(dataframe):
    """
    Displays the first few records of the dataset.
    """

    print("\n" + "=" * 65)
    print(f"DATA PREVIEW - FIRST {PREVIEW_ROWS} ROWS")
    print("=" * 65)

    print(
        dataframe.head(PREVIEW_ROWS).to_string(index=False)
    )



def display_numeric_summary(dataframe):
    """
    Displays a basic numerical summary.
    """

    numeric_columns = dataframe.select_dtypes(
        include=["number"]
    ).columns

    if len(numeric_columns) == 0:

        print("\nNo numerical columns detected.")

        return

    print("\n" + "=" * 65)
    print("NUMERICAL SUMMARY")
    print("=" * 65)

    print(
        dataframe[numeric_columns]
        .describe()
        .round(2)
        .to_string()
    )


def validate_loaded_data(dataframe):
    """
    Performs basic validation after ingestion.
    """

    print("\n" + "=" * 65)
    print("INGESTION VALIDATION")
    print("=" * 65)

    if dataframe.empty:

        print("ERROR: Dataset is empty.")
        return False

    print("Dataset status : VALID")
    print(f"Rows received  : {len(dataframe)}")
    print(f"Columns received: {len(dataframe.columns)}")

    duplicate_count = dataframe.duplicated().sum()

    print(f"Duplicate rows  : {duplicate_count}")

    return True



def main():

    try:

        dataframe = load_data()

        if not validate_loaded_data(dataframe):
            sys.exit(1)

        display_dataset_information(dataframe)

        display_preview(dataframe)

        display_numeric_summary(dataframe)

        print("\n" + "=" * 65)
        print("DATA INGESTION COMPLETED SUCCESSFULLY")
        print("=" * 65)

        print(
            f"Source: {SOURCE.upper()} | "
            f"Rows: {len(dataframe)} | "
            f"Columns: {len(dataframe.columns)}"
        )

        return dataframe

    except KeyboardInterrupt:

        print("\n\nProcess interrupted by user.")
        sys.exit(0)

    except Exception as error:

        print("\nUNEXPECTED INGESTION ERROR")
        print("-" * 65)
        print(error)
        sys.exit(1)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()