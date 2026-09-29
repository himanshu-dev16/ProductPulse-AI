# ============================================================
# PRODUCTPULSE AI
# Configuration File
# ============================================================


# ============================================================
# 1. DATA SOURCE
# ============================================================
# Available options:
# "MYSQL"
# "MONGODB"
# "EXCEL"

SOURCE = "MYSQL"


# ============================================================
# 2. DATA DESTINATION
# ============================================================
# Available options:
# "MYSQL"
# "MONGODB"
# "EXCEL"

DESTINATION = "EXCEL"


# ============================================================
# 3. MYSQL CONFIGURATION
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306

MYSQL_USER = "root"

MYSQL_PASSWORD = "Your_Password"

MYSQL_DATABASE = "productpulse"

MYSQL_TABLE = "customer_product_data"


# ============================================================
# 4. MONGODB CONFIGURATION
# ============================================================

MONGO_URI = "mongodb://localhost:27017/"

MONGO_DATABASE = "productpulse"

MONGO_COLLECTION = "customer_product_data"


# ============================================================
# 5. EXCEL CONFIGURATION
# ============================================================

EXCEL_INPUT_FILE = "productpulse_input.xlsx"

EXCEL_OUTPUT_FILE = "productpulse_cleaned.xlsx"


# ============================================================
# 6. GENERAL PROJECT SETTINGS
# ============================================================

# Number of rows to display when previewing data
PREVIEW_ROWS = 10

# Whether ingestion should print detailed information
SHOW_INGESTION_LOGS = True
