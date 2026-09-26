# ProductPulse AI

ProductPulse AI is a multi-source product intelligence and customer analytics platform designed for data analysis, machine learning, and business intelligence workflows.

The project can load customer and product data from MySQL, MongoDB, or Excel, perform data cleaning and analysis, apply machine learning models, generate AI-based business insights, and export the final enriched dataset to MySQL, MongoDB, or Excel.

The exported dataset can then be connected to Power BI for interactive business dashboards and reporting.

## Project Flow

MySQL / MongoDB / Excel

↓

Data Ingestion

↓

Data Cleaning

↓

Business Analysis

↓

Machine Learning

↓

AI Business Insights

↓

Clean + Enriched Dataset

↓

MySQL / MongoDB / Excel

↓

Power BI

## Main Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- MySQL
- MongoDB
- Excel
- Power BI
- Machine Learning
- AI-based Business Insights

## Project Structure

ProductPulseAI/

├── 01_ingestion.py
├── 02_cleaning.py
├── 03_analysis.py
├── 04_ml.py
├── 05_ai.py
├── 06_export.py
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── productpulse_input.xlsx

## File Responsibilities

### 01_ingestion.py

Loads the dataset from the selected source.

Supported sources:

- MySQL
- MongoDB
- Excel

The source is selected through `config.py`.

The module also performs initial dataset inspection and validation.

### 02_cleaning.py

Cleans and prepares the raw dataset.

Operations include:

- Column standardization
- Text cleaning
- Date conversion
- Numeric conversion
- Missing value handling
- Duplicate removal
- Data validation
- Sentiment normalization

### 03_analysis.py

Performs business-oriented exploratory analysis.

The module calculates:

- Customer KPIs
- Revenue metrics
- Order metrics
- Churn metrics
- Plan-wise analysis
- Country-wise analysis
- Product category analysis
- Sentiment analysis
- Customer value analysis
- At-risk customer analysis
- Correlations

### 04_ml.py

Applies machine learning techniques to customer data.

The module performs:

- Churn prediction
- Logistic Regression
- Random Forest classification
- Model evaluation
- Churn probability calculation
- Churn risk classification
- Feature importance analysis
- Customer segmentation
- K-Means clustering
- Silhouette score calculation

### 05_ai.py

Generates business-oriented AI insights from the analyzed and enriched dataset.

The module produces:

- Business metrics
- Plan insights
- Country insights
- Product insights
- Sentiment insights
- Customer recommended actions
- Business insights
- Power BI-ready enriched data

### 06_export.py

Exports the final enriched dataset.

Supported destinations:

- MySQL
- MongoDB
- Excel

The destination is selected through `config.py`.

### main.py

Acts as the main controller of the ProductPulse AI pipeline.

It connects all project modules and executes them in the correct order:

- Data Ingestion
- Data Cleaning
- Business Analysis
- Machine Learning
- AI Business Insights
- Data Export

The complete pipeline can be started by running:

```bash
python main.py

config.py

Contains the main project configuration.

The source can be changed using:

SOURCE

Supported values:

MYSQL

MONGODB

EXCEL

The destination can be changed using:

DESTINATION

Supported values:

MYSQL

MONGODB

EXCEL

Dataset

The project uses customer and product-related information including:

Customer ID
Customer Name
Country
Signup Date
Plan
Monthly Spend
Total Orders
Total Spend
Last Purchase Date
Support Tickets
Average Session Minutes
Feature Usage Count
Churn Status
Product Category
Rating
Sentiment
Feedback
Machine Learning

ProductPulse AI uses supervised and unsupervised machine learning.

Churn Prediction

The churn prediction pipeline uses:

Logistic Regression
Random Forest

The model predicts whether a customer is likely to churn and calculates a churn probability.

Customers are categorized into:

Low Risk
Medium Risk
High Risk
Customer Segmentation

K-Means clustering is used to identify groups of customers based on behavioral and business attributes.

Segmentation uses features such as:

Total Orders
Total Spend
Support Tickets
Average Session Minutes
Feature Usage Count
AI Business Intelligence

The AI module converts analytical results into business-oriented insights.

Examples include:

Churn monitoring
Customer retention opportunities
Product experience observations
High-risk customer identification
Customer engagement recommendations
Revenue-related insights
Power BI

Power BI is used as the visualization and dashboard layer.

The Python pipeline prepares a clean and enriched dataset containing analytical and machine learning outputs.

Power BI can use fields such as:

Total Spend
Total Orders
Churn Rate
Churn Probability
Churn Risk
Customer Segment
Product Category
Plan
Country
Sentiment
Customer Lifetime Days
Average Order Value
Recommended Action
Installation

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt
Database Setup

The project can work with local MySQL and MongoDB installations.

The MySQL database should contain:

productpulse

The main table is:

customer_product_data

MongoDB uses:

Database:

productpulse

Collection:

customer_product_data

Configuration

Open:

config.py

Set the required source:

SOURCE = "MYSQL"

or:

SOURCE = "MONGODB"

or:

SOURCE = "EXCEL"

Set the destination:

DESTINATION = "EXCEL"

or:

DESTINATION = "MYSQL"

or:

DESTINATION = "MONGODB"
MySQL Configuration

Update the MySQL password in config.py:

MYSQL_PASSWORD = "YOUR_MYSQL_PASSWORD"

Use the password of your local MySQL installation.

Do not upload your real database password to GitHub.

Running the Project

The modules are designed as a data pipeline.

The general execution order is:

01_ingestion.py
        ↓
02_cleaning.py
        ↓
03_analysis.py
        ↓
04_ml.py
        ↓
05_ai.py
        ↓
06_export.py

The complete pipeline is controlled by main.py.

Run the complete project using:

python main.py

Each stage processes the output of the previous stage.

Data Source Switching

To use MySQL:

SOURCE = "MYSQL"

To use MongoDB:

SOURCE = "MONGODB"

To use Excel:

SOURCE = "EXCEL"

Only the selected source should be active in the ingestion pipeline.

Data Destination Switching

To export to Excel:

DESTINATION = "EXCEL"

To export to MySQL:

DESTINATION = "MYSQL"

To export to MongoDB:

DESTINATION = "MONGODB"

Only the selected destination is used by the export pipeline.

Business Use Cases

ProductPulse AI can support business teams with:

Customer churn analysis
Customer segmentation
Revenue analysis
Product performance analysis
Customer feedback analysis
Retention analysis
Customer value analysis
Support issue analysis
Business KPI monitoring
Power BI reporting
Skills Demonstrated

This project demonstrates practical experience with:

Python programming
Data ingestion
Data cleaning
Exploratory data analysis
SQL
MySQL
MongoDB
Excel
Pandas
NumPy
Machine Learning
Classification
Clustering
Customer segmentation
Churn prediction
Business analytics
AI-assisted insights
Data export pipelines
Power BI data preparation
Final Output

The final output is a clean and enriched customer dataset containing original business data together with analytical, machine learning, and business intelligence fields.

This dataset can be directly used as the data source for a Power BI dashboard.

Author

Himanshu Gupta