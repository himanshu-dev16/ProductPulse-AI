import pandas as pd
import numpy as np
import json
from datetime import datetime

from config import (
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


def ai_log(message):
    print(message)


def prepare_ai_dataset(dataframe):
    data = dataframe.copy()

    numeric_columns = [
        "monthly_spend",
        "total_orders",
        "total_spend",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count",
        "rating",
        "churned",
        "churn_probability"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    return data


def calculate_business_metrics(data):
    metrics = {}

    metrics["total_customers"] = int(
        len(data)
    )

    metrics["total_revenue"] = round(
        data["total_spend"].sum(),
        2
    )

    metrics["average_customer_spend"] = round(
        data["total_spend"].mean(),
        2
    )

    metrics["average_monthly_spend"] = round(
        data["monthly_spend"].mean(),
        2
    )

    metrics["total_orders"] = int(
        data["total_orders"].sum()
    )

    metrics["average_orders_per_customer"] = round(
        data["total_orders"].mean(),
        2
    )

    metrics["churned_customers"] = int(
        data["churned"].sum()
    )

    metrics["churn_rate"] = round(
        data["churned"].mean() * 100,
        2
    )

    metrics["average_rating"] = round(
        data["rating"].mean(),
        2
    )

    metrics["total_support_tickets"] = int(
        data["support_tickets"].sum()
    )

    return metrics


def calculate_plan_insights(data):
    result = (
        data
        .groupby("plan")
        .agg(
            customers=("customer_id", "count"),
            revenue=("total_spend", "sum"),
            average_spend=("total_spend", "mean"),
            average_orders=("total_orders", "mean"),
            churn_rate=("churned", "mean"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )

    result["revenue"] = result["revenue"].round(2)

    result["average_spend"] = (
        result["average_spend"]
        .round(2)
    )

    result["average_orders"] = (
        result["average_orders"]
        .round(2)
    )

    result["churn_rate"] = (
        result["churn_rate"] * 100
    ).round(2)

    result["average_rating"] = (
        result["average_rating"]
        .round(2)
    )

    return result


def calculate_country_insights(data):
    result = (
        data
        .groupby("country")
        .agg(
            customers=("customer_id", "count"),
            revenue=("total_spend", "sum"),
            average_spend=("total_spend", "mean"),
            churn_rate=("churned", "mean"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )

    result["revenue"] = result["revenue"].round(2)

    result["average_spend"] = (
        result["average_spend"]
        .round(2)
    )

    result["churn_rate"] = (
        result["churn_rate"] * 100
    ).round(2)

    result["average_rating"] = (
        result["average_rating"]
        .round(2)
    )

    return result


def calculate_product_insights(data):
    result = (
        data
        .groupby("product_category")
        .agg(
            customers=("customer_id", "count"),
            revenue=("total_spend", "sum"),
            average_rating=("rating", "mean"),
            average_orders=("total_orders", "mean"),
            churn_rate=("churned", "mean")
        )
        .reset_index()
    )

    result["revenue"] = result["revenue"].round(2)

    result["average_rating"] = (
        result["average_rating"]
        .round(2)
    )

    result["average_orders"] = (
        result["average_orders"]
        .round(2)
    )

    result["churn_rate"] = (
        result["churn_rate"] * 100
    ).round(2)

    return result


def calculate_sentiment_insights(data):
    result = (
        data["sentiment"]
        .value_counts()
        .rename_axis("sentiment")
        .reset_index(name="customers")
    )

    result["percentage"] = (
        result["customers"]
        / len(data)
        * 100
    ).round(2)

    return result


def generate_customer_actions(data):
    actions = []

    median_spend = data[
        "total_spend"
    ].median()

    for _, row in data.iterrows():

        risk = row.get(
            "churn_risk",
            "Unknown"
        )

        sentiment = row.get(
            "sentiment",
            "Unknown"
        )

        support = row.get(
            "support_tickets",
            0
        )

        rating = row.get(
            "rating",
            0
        )

        spend = row.get(
            "total_spend",
            0
        )

        action = "Maintain regular engagement"

        if risk == "High":
            action = (
                "Prioritize retention outreach "
                "and identify churn drivers"
            )

        elif sentiment == "Negative":
            action = (
                "Review customer feedback and "
                "resolve service concerns"
            )

        elif support >= 5:
            action = (
                "Review support history and "
                "provide proactive assistance"
            )

        elif rating <= 2:
            action = (
                "Investigate product experience "
                "and collect detailed feedback"
            )

        elif spend >= median_spend:
            action = (
                "Consider loyalty engagement "
                "and premium retention offers"
            )

        actions.append(action)

    result = data.copy()

    result["recommended_action"] = actions

    return result


def generate_ai_insights(data, metrics):
    insights = []

    churn_rate = metrics[
        "churn_rate"
    ]

    average_rating = metrics[
        "average_rating"
    ]

    average_spend = metrics[
        "average_customer_spend"
    ]

    total_customers = metrics[
        "total_customers"
    ]

    if churn_rate >= 30:
        insights.append(
            "Customer churn is elevated and "
            "retention activity should be reviewed."
        )

    elif churn_rate >= 15:
        insights.append(
            "Customer churn is at a moderate level "
            "and should be monitored."
        )

    else:
        insights.append(
            "Customer churn is currently below "
            "the moderate threshold."
        )

    if average_rating < 3:
        insights.append(
            "Average customer rating indicates "
            "a need to investigate product experience."
        )

    elif average_rating >= 4:
        insights.append(
            "Average customer rating indicates "
            "generally positive customer experience."
        )

    if "churn_probability" in data.columns:

        high_risk_count = int(
            (
                data["churn_probability"] >= 60
            ).sum()
        )

        insights.append(
            f"{high_risk_count} customers have "
            "a churn probability of at least 60%."
        )

    if "customer_segment" in data.columns:

        segment_count = int(
            data["customer_segment"]
            .nunique()
        )

        insights.append(
            f"Customer behavior is divided into "
            f"{segment_count} data-driven segments."
        )

    if average_spend > 0:

        insights.append(
            f"Average customer lifetime spend "
            f"is {average_spend:.2f}."
        )

    insights.append(
        f"The dataset contains {total_customers} "
        "customer records for business analysis."
    )

    return insights


def generate_ai_summary(
    data,
    metrics,
    plan_insights,
    country_insights,
    product_insights
):
    summary = {}

    summary["generated_at"] = (
        datetime.now().isoformat()
    )

    summary["business_metrics"] = metrics

    summary["insights"] = generate_ai_insights(
        data,
        metrics
    )

    if not plan_insights.empty:

        top_plan = (
            plan_insights
            .sort_values(
                "revenue",
                ascending=False
            )
            .iloc[0]
        )

        summary["top_revenue_plan"] = (
            str(top_plan["plan"])
        )

    if not country_insights.empty:

        top_country = (
            country_insights
            .sort_values(
                "revenue",
                ascending=False
            )
            .iloc[0]
        )

        summary["top_revenue_country"] = (
            str(top_country["country"])
        )

    if not product_insights.empty:

        top_product = (
            product_insights
            .sort_values(
                "revenue",
                ascending=False
            )
            .iloc[0]
        )

        summary["top_revenue_product"] = (
            str(
                top_product["product_category"]
            )
        )

    return summary


def prepare_powerbi_table(data):
    result = data.copy()

    result["signup_date"] = pd.to_datetime(
        result["signup_date"],
        errors="coerce"
    )

    result["last_purchase_date"] = pd.to_datetime(
        result["last_purchase_date"],
        errors="coerce"
    )

    result["customer_lifetime_days"] = (
        result["last_purchase_date"]
        - result["signup_date"]
    ).dt.days

    result["average_order_value"] = np.where(
        result["total_orders"] > 0,
        result["total_spend"]
        / result["total_orders"],
        0
    )

    result["average_order_value"] = (
        result["average_order_value"]
        .round(2)
    )

    if "churn_probability" in result.columns:

        result["churn_probability"] = (
            result["churn_probability"]
            .round(2)
        )

    return result


def display_ai_insights(summary):
    print("\n" + "=" * 65)
    print(
        "PRODUCTPULSE AI - BUSINESS INTELLIGENCE"
    )
    print("=" * 65)

    print(
        "\nAI-Generated Business Insights:"
    )

    for index, insight in enumerate(
        summary["insights"],
        start=1
    ):
        print(
            f"{index}. {insight}"
        )

    print(
        "\nKey Business Findings:"
    )

    keys = [
        "top_revenue_plan",
        "top_revenue_country",
        "top_revenue_product"
    ]

    for key in keys:

        if key in summary:

            print(
                f"{key}: {summary[key]}"
            )


def run_ai_pipeline(dataframe):

    if dataframe is None:
        raise ValueError(
            "Input DataFrame cannot be None."
        )

    if dataframe.empty:
        raise ValueError(
            "Input DataFrame is empty."
        )

    print("\n" + "=" * 65)
    print(
        "STARTING AI BUSINESS INSIGHT ENGINE"
    )
    print("=" * 65)

    data = prepare_ai_dataset(
        dataframe
    )

    metrics = calculate_business_metrics(
        data
    )

    plan_insights = calculate_plan_insights(
        data
    )

    country_insights = (
        calculate_country_insights(
            data
        )
    )

    product_insights = (
        calculate_product_insights(
            data
        )
    )

    sentiment_insights = (
        calculate_sentiment_insights(
            data
        )
    )

    action_data = generate_customer_actions(
        data
    )

    summary = generate_ai_summary(
        action_data,
        metrics,
        plan_insights,
        country_insights,
        product_insights
    )

    powerbi_data = prepare_powerbi_table(
        action_data
    )

    display_ai_insights(
        summary
    )

    print(
        "\nAI BUSINESS INSIGHT ENGINE "
        "COMPLETED"
    )

    return {
        "enriched_data": powerbi_data,
        "business_metrics": metrics,
        "plan_insights": plan_insights,
        "country_insights": country_insights,
        "product_insights": product_insights,
        "sentiment_insights": sentiment_insights,
        "ai_summary": summary
    }


if __name__ == "__main__":

    print(
        "\n05_ai.py is ready."
    )

    print(
        "This module receives the enriched "
        "DataFrame from the ML pipeline."
    )

    print(
        "It generates business insights, "
        "customer actions and Power BI data."
    )