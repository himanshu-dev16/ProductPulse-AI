import pandas as pd
import numpy as np


def analysis_log(message):
    """
    Prints analysis information.
    """

    print(message)


def calculate_basic_metrics(dataframe):
    """
    Calculates high-level ProductPulse business metrics.
    """

    metrics = {}

    metrics["total_customers"] = len(dataframe)

    if "total_spend" in dataframe.columns:
        metrics["total_spend"] = round(
            dataframe["total_spend"].sum(),
            2
        )

        metrics["average_spend"] = round(
            dataframe["total_spend"].mean(),
            2
        )

    else:
        metrics["total_spend"] = 0
        metrics["average_spend"] = 0

    if "total_orders" in dataframe.columns:
        metrics["total_orders"] = int(
            dataframe["total_orders"].sum()
        )

        metrics["average_orders"] = round(
            dataframe["total_orders"].mean(),
            2
        )

    else:
        metrics["total_orders"] = 0
        metrics["average_orders"] = 0

    if "churned" in dataframe.columns:

        metrics["churned_customers"] = int(
            dataframe["churned"].sum()
        )

        metrics["churn_rate"] = round(
            dataframe["churned"].mean() * 100,
            2
        )

    else:

        metrics["churned_customers"] = 0
        metrics["churn_rate"] = 0

    if "rating" in dataframe.columns:

        metrics["average_rating"] = round(
            dataframe["rating"].mean(),
            2
        )

    else:

        metrics["average_rating"] = 0

    if "support_tickets" in dataframe.columns:

        metrics["total_support_tickets"] = int(
            dataframe["support_tickets"].sum()
        )

        metrics["average_support_tickets"] = round(
            dataframe["support_tickets"].mean(),
            2
        )

    else:

        metrics["total_support_tickets"] = 0
        metrics["average_support_tickets"] = 0

    return metrics


def display_basic_metrics(metrics):
    """
    Displays high-level business KPIs.
    """

    print("\n" + "=" * 65)
    print("PRODUCTPULSE BUSINESS KPIs")
    print("=" * 65)

    print(
        f"Total customers          : "
        f"{metrics['total_customers']}"
    )

    print(
        f"Total spend              : "
        f"{metrics['total_spend']:.2f}"
    )

    print(
        f"Average customer spend  : "
        f"{metrics['average_spend']:.2f}"
    )

    print(
        f"Total orders             : "
        f"{metrics['total_orders']}"
    )

    print(
        f"Average orders/customer : "
        f"{metrics['average_orders']:.2f}"
    )

    print(
        f"Churned customers        : "
        f"{metrics['churned_customers']}"
    )

    print(
        f"Churn rate               : "
        f"{metrics['churn_rate']:.2f}%"
    )

    print(
        f"Average rating           : "
        f"{metrics['average_rating']:.2f}"
    )

    print(
        f"Total support tickets    : "
        f"{metrics['total_support_tickets']}"
    )

    print(
        f"Avg support tickets      : "
        f"{metrics['average_support_tickets']:.2f}"
    )

def analyze_by_plan(dataframe):
    """
    Calculates performance metrics by subscription plan.
    """

    if "plan" not in dataframe.columns:

        return pd.DataFrame()

    aggregation = {}

    if "customer_id" in dataframe.columns:
        aggregation["customer_id"] = "count"

    if "total_spend" in dataframe.columns:
        aggregation["total_spend"] = ["sum", "mean"]

    if "total_orders" in dataframe.columns:
        aggregation["total_orders"] = ["sum", "mean"]

    if "churned" in dataframe.columns:
        aggregation["churned"] = "mean"

    if "rating" in dataframe.columns:
        aggregation["rating"] = "mean"

    result = dataframe.groupby(
        "plan"
    ).agg(aggregation)

    result.columns = [
        "_".join(
            column if isinstance(column, tuple)
            else (column,)
        ).strip("_")
        for column in result.columns
    ]

    result = result.reset_index()

    if "churned_mean" in result.columns:

        result["churn_rate_percent"] = (
            result["churned_mean"] * 100
        ).round(2)

    return result


def analyze_by_country(dataframe):
    """
    Calculates customer and business metrics by country.
    """

    if "country" not in dataframe.columns:

        return pd.DataFrame()

    aggregation = {}

    if "customer_id" in dataframe.columns:
        aggregation["customer_id"] = "count"

    if "total_spend" in dataframe.columns:
        aggregation["total_spend"] = "sum"

    if "total_orders" in dataframe.columns:
        aggregation["total_orders"] = "sum"

    if "churned" in dataframe.columns:
        aggregation["churned"] = "mean"

    if "rating" in dataframe.columns:
        aggregation["rating"] = "mean"

    result = dataframe.groupby(
        "country"
    ).agg(aggregation).reset_index()

    result = result.rename(
        columns={
            "customer_id": "customer_count",
            "total_spend": "total_spend",
            "total_orders": "total_orders",
            "churned": "churn_rate",
            "rating": "average_rating"
        }
    )

    if "churn_rate" in result.columns:

        result["churn_rate"] = (
            result["churn_rate"] * 100
        ).round(2)

    if "total_spend" in result.columns:

        result["total_spend"] = (
            result["total_spend"]
            .round(2)
        )

    if "average_rating" in result.columns:

        result["average_rating"] = (
            result["average_rating"]
            .round(2)
        )

    return result


def analyze_by_category(dataframe):
    """
    Calculates performance by product category.
    """

    if "product_category" not in dataframe.columns:

        return pd.DataFrame()

    aggregation = {}

    if "customer_id" in dataframe.columns:
        aggregation["customer_id"] = "count"

    if "total_spend" in dataframe.columns:
        aggregation["total_spend"] = "sum"

    if "total_orders" in dataframe.columns:
        aggregation["total_orders"] = "sum"

    if "rating" in dataframe.columns:
        aggregation["rating"] = "mean"

    if "churned" in dataframe.columns:
        aggregation["churned"] = "mean"

    result = dataframe.groupby(
        "product_category"
    ).agg(aggregation).reset_index()

    result = result.rename(
        columns={
            "customer_id": "customer_count",
            "total_spend": "total_spend",
            "total_orders": "total_orders",
            "rating": "average_rating",
            "churned": "churn_rate"
        }
    )

    if "churn_rate" in result.columns:

        result["churn_rate"] = (
            result["churn_rate"] * 100
        ).round(2)

    if "average_rating" in result.columns:

        result["average_rating"] = (
            result["average_rating"]
            .round(2)
        )

    return result


def analyze_sentiment(dataframe):
    """
    Calculates sentiment distribution.
    """

    if "sentiment" not in dataframe.columns:

        return pd.DataFrame()

    result = (
        dataframe["sentiment"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "sentiment",
        "customer_count"
    ]

    result["percentage"] = (
        result["customer_count"]
        / len(dataframe)
        * 100
    ).round(2)

    return result

def analyze_customer_value(dataframe):
    """
    Identifies high-value customers.
    """

    required_columns = [
        "customer_id",
        "customer_name",
        "total_spend"
    ]

    if not all(
        column in dataframe.columns
        for column in required_columns
    ):

        return pd.DataFrame()

    columns = [
        "customer_id",
        "customer_name",
        "total_spend"
    ]

    optional_columns = [
        "plan",
        "country",
        "total_orders",
        "rating",
        "churned"
    ]

    for column in optional_columns:

        if column in dataframe.columns:
            columns.append(column)

    result = (
        dataframe[columns]
        .sort_values(
            "total_spend",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return result


def identify_at_risk_customers(dataframe):
    """
    Identifies customers showing multiple risk signals.

    Risk signals:
    - churned
    - high support tickets
    - low session duration
    - negative sentiment
    """

    result = dataframe.copy()

    result["risk_score"] = 0

    if "churned" in result.columns:

        result["risk_score"] += (
            result["churned"] == 1
        ).astype(int) * 4

    if "support_tickets" in result.columns:

        ticket_threshold = result[
            "support_tickets"
        ].median()

        result["risk_score"] += (
            result["support_tickets"]
            > ticket_threshold
        ).astype(int) * 2

    if "avg_session_minutes" in result.columns:

        session_threshold = result[
            "avg_session_minutes"
        ].median()

        result["risk_score"] += (
            result["avg_session_minutes"]
            < session_threshold
        ).astype(int) * 2

    if "sentiment" in result.columns:

        result["risk_score"] += (
            result["sentiment"]
            .astype("string")
            .str.lower()
            .eq("negative")
        ).astype(int) * 2

    result["risk_level"] = pd.cut(
        result["risk_score"],
        bins=[
            -1,
            2,
            5,
            10
        ],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    columns = [
        column
        for column in [
            "customer_id",
            "customer_name",
            "country",
            "plan",
            "total_spend",
            "support_tickets",
            "avg_session_minutes",
            "sentiment",
            "churned",
            "risk_score",
            "risk_level"
        ]
        if column in result.columns
    ]

    return (
        result[columns]
        .sort_values(
            "risk_score",
            ascending=False
        )
        .reset_index(drop=True)
    )


def calculate_correlations(dataframe):
    """
    Calculates correlations between numerical variables.
    """

    numeric_data = dataframe.select_dtypes(
        include=["number"]
    )

    if numeric_data.empty:

        return pd.DataFrame()

    correlation_matrix = (
        numeric_data
        .corr()
        .round(3)
    )

    return correlation_matrix



def display_top_customers(
    customer_value_data,
    limit=10
):
    """
    Displays the highest-value customers.
    """

    if customer_value_data.empty:

        return

    print("\n" + "=" * 65)
    print(f"TOP {limit} CUSTOMERS BY SPEND")
    print("=" * 65)

    print(
        customer_value_data
        .head(limit)
        .to_string(index=False)
    )


def display_at_risk_customers(
    risk_data,
    limit=10
):
    """
    Displays highest-risk customers.
    """

    if risk_data.empty:

        return

    print("\n" + "=" * 65)
    print(f"TOP {limit} AT-RISK CUSTOMERS")
    print("=" * 65)

    print(
        risk_data
        .head(limit)
        .to_string(index=False)
    )


def display_group_analysis(
    title,
    dataframe
):
    """
    Displays grouped analytical results.
    """

    if dataframe.empty:

        print(
            f"\n{title}: No data available."
        )

        return

    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    print(
        dataframe.to_string(index=False)
    )

def analyze_data(dataframe):
    """
    Runs the complete ProductPulse analysis pipeline.

    Returns a dictionary containing all analysis outputs.
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
    print("PRODUCTPULSE AI - ANALYTICS ENGINE")
    print("=" * 65)


    basic_metrics = calculate_basic_metrics(
        dataframe
    )

    display_basic_metrics(
        basic_metrics
    )


    plan_analysis = analyze_by_plan(
        dataframe
    )

    display_group_analysis(
        "PLAN-WISE ANALYSIS",
        plan_analysis
    )


    country_analysis = analyze_by_country(
        dataframe
    )

    display_group_analysis(
        "COUNTRY-WISE ANALYSIS",
        country_analysis
    )


    category_analysis = analyze_by_category(
        dataframe
    )

    display_group_analysis(
        "PRODUCT CATEGORY ANALYSIS",
        category_analysis
    )


    sentiment_analysis = analyze_sentiment(
        dataframe
    )

    display_group_analysis(
        "SENTIMENT ANALYSIS",
        sentiment_analysis
    )

    customer_value = analyze_customer_value(
        dataframe
    )

    display_top_customers(
        customer_value
    )


    at_risk_customers = identify_at_risk_customers(
        dataframe
    )

    display_at_risk_customers(
        at_risk_customers
    )


    correlations = calculate_correlations(
        dataframe
    )

    if not correlations.empty:

        print("\n" + "=" * 65)
        print("CORRELATION ANALYSIS")
        print("=" * 65)

        print(
            correlations.to_string()
        )

    print("\n" + "=" * 65)
    print("DATA ANALYSIS COMPLETED SUCCESSFULLY")
    print("=" * 65)

    return {
        "basic_metrics": basic_metrics,
        "plan_analysis": plan_analysis,
        "country_analysis": country_analysis,
        "category_analysis": category_analysis,
        "sentiment_analysis": sentiment_analysis,
        "customer_value": customer_value,
        "at_risk_customers": at_risk_customers,
        "correlations": correlations
    }


if __name__ == "__main__":

    print("\n03_analysis.py is ready.")

    print(
        "This module receives the cleaned DataFrame "
        "from 02_cleaning.py."
    )

    print(
        "Charts are intentionally not generated here."
    )

    print(
        "The analytical outputs will later be "
        "exported for Power BI."
    )