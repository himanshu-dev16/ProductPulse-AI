import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    silhouette_score
)


def ml_log(message):
    print(message)


def prepare_churn_features(dataframe):
    required_columns = [
        "total_orders",
        "total_spend",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing ML columns: {missing_columns}"
        )

    features = dataframe[required_columns].copy()

    features = features.replace(
        [np.inf, -np.inf],
        np.nan
    )

    features = features.fillna(
        features.median()
    )

    target = None

    if "churned" in dataframe.columns:
        target = dataframe["churned"].astype(int)

    return features, target


def train_logistic_regression(features, target):
    model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42
                )
            )
        ]
    )

    model.fit(
        features,
        target
    )

    return model


def train_random_forest(features, target):
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=4,
        random_state=42
    )

    model.fit(
        features,
        target
    )

    return model


def evaluate_model(model, x_test, y_test):
    predictions = model.predict(
        x_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    return {
        "accuracy": round(
            accuracy,
            4
        ),
        "precision": round(
            precision,
            4
        ),
        "recall": round(
            recall,
            4
        ),
        "f1_score": round(
            f1,
            4
        ),
        "confusion_matrix": matrix
    }


def display_model_results(
    model_name,
    results
):
    print("\n" + "=" * 65)
    print(model_name)
    print("=" * 65)

    print(
        f"Accuracy  : "
        f"{results['accuracy'] * 100:.2f}%"
    )

    print(
        f"Precision : "
        f"{results['precision'] * 100:.2f}%"
    )

    print(
        f"Recall    : "
        f"{results['recall'] * 100:.2f}%"
    )

    print(
        f"F1 Score  : "
        f"{results['f1_score'] * 100:.2f}%"
    )

    print("\nConfusion Matrix:")
    print(
        results["confusion_matrix"]
    )


def generate_churn_predictions(
    model,
    features,
    dataframe
):
    result = dataframe.copy()

    predictions = model.predict(
        features
    )

    probabilities = model.predict_proba(
        features
    )[:, 1]

    result["predicted_churn"] = predictions

    result["churn_probability"] = (
        probabilities * 100
    ).round(2)

    result["churn_risk"] = pd.cut(
        result["churn_probability"],
        bins=[
            -1,
            30,
            60,
            100
        ],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    return result


def calculate_feature_importance(
    model,
    feature_names
):
    if not hasattr(
        model,
        "feature_importances_"
    ):
        return pd.DataFrame()

    importance = pd.DataFrame(
        {
            "feature": feature_names,
            "importance": model.feature_importances_
        }
    )

    importance = (
        importance
        .sort_values(
            "importance",
            ascending=False
        )
        .reset_index(drop=True)
    )

    importance["importance_percent"] = (
        importance["importance"] * 100
    ).round(2)

    return importance


def display_feature_importance(
    importance
):
    if importance.empty:
        return

    print("\n" + "=" * 65)
    print("CHURN MODEL FEATURE IMPORTANCE")
    print("=" * 65)

    print(
        importance.to_string(
            index=False
        )
    )


def prepare_segmentation_features(
    dataframe
):
    required_columns = [
        "total_orders",
        "total_spend",
        "support_tickets",
        "avg_session_minutes",
        "feature_usage_count"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing segmentation columns: "
            f"{missing_columns}"
        )

    features = dataframe[
        required_columns
    ].copy()

    features = features.replace(
        [np.inf, -np.inf],
        np.nan
    )

    features = features.fillna(
        features.median()
    )

    return features


def perform_customer_segmentation(
    dataframe,
    number_of_clusters=4
):
    features = prepare_segmentation_features(
        dataframe
    )

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(
        features
    )

    model = KMeans(
        n_clusters=number_of_clusters,
        random_state=42,
        n_init=10
    )

    clusters = model.fit_predict(
        scaled_features
    )

    result = dataframe.copy()

    result["customer_segment"] = (
        clusters + 1
    )

    silhouette = silhouette_score(
        scaled_features,
        clusters
    )

    return result, model, round(
        silhouette,
        4
    )


def describe_segments(
    segmented_data
):
    if "customer_segment" not in segmented_data.columns:
        return pd.DataFrame()

    numeric_columns = [
        column
        for column in [
            "total_orders",
            "total_spend",
            "support_tickets",
            "avg_session_minutes",
            "feature_usage_count",
            "rating",
            "churned"
        ]
        if column in segmented_data.columns
    ]

    if not numeric_columns:
        return pd.DataFrame()

    result = (
        segmented_data
        .groupby(
            "customer_segment"
        )[numeric_columns]
        .mean()
        .round(2)
        .reset_index()
    )

    return result


def display_segment_results(
    segment_summary,
    silhouette
):
    print("\n" + "=" * 65)
    print("CUSTOMER SEGMENTATION")
    print("=" * 65)

    print(
        f"Silhouette Score: "
        f"{silhouette:.4f}"
    )

    print("\nSegment Profiles:")

    print(
        segment_summary.to_string(
            index=False
        )
    )


def identify_high_risk_customers(
    churn_data
):
    if "churn_probability" not in churn_data.columns:
        return pd.DataFrame()

    result = churn_data[
        churn_data["churn_probability"] >= 60
    ].copy()

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
            "churn_probability",
            "churn_risk"
        ]
        if column in result.columns
    ]

    return (
        result[columns]
        .sort_values(
            "churn_probability",
            ascending=False
        )
        .reset_index(drop=True)
    )


def display_high_risk_customers(
    dataframe
):
    if dataframe.empty:
        return

    print("\n" + "=" * 65)
    print("HIGH-RISK CUSTOMERS")
    print("=" * 65)

    print(
        dataframe
        .head(10)
        .to_string(index=False)
    )


def run_churn_prediction(
    dataframe
):
    features, target = prepare_churn_features(
        dataframe
    )

    if target is None:
        raise ValueError(
            "The churned column is required "
            "for supervised ML."
        )

    if target.nunique() < 2:
        raise ValueError(
            "Churn target must contain at least "
            "two classes."
        )

    x_train, x_test, y_train, y_test = (
        train_test_split(
            features,
            target,
            test_size=0.25,
            random_state=42,
            stratify=target
        )
    )

    logistic_model = train_logistic_regression(
        x_train,
        y_train
    )

    random_forest_model = train_random_forest(
        x_train,
        y_train
    )

    logistic_results = evaluate_model(
        logistic_model,
        x_test,
        y_test
    )

    random_forest_results = evaluate_model(
        random_forest_model,
        x_test,
        y_test
    )

    display_model_results(
        "LOGISTIC REGRESSION",
        logistic_results
    )

    display_model_results(
        "RANDOM FOREST",
        random_forest_results
    )

    churn_data = generate_churn_predictions(
        random_forest_model,
        features,
        dataframe
    )

    importance = calculate_feature_importance(
        random_forest_model,
        features.columns
    )

    display_feature_importance(
        importance
    )

    high_risk = identify_high_risk_customers(
        churn_data
    )

    display_high_risk_customers(
        high_risk
    )

    return {
        "model": random_forest_model,
        "logistic_model": logistic_model,
        "churn_data": churn_data,
        "feature_importance": importance,
        "high_risk_customers": high_risk,
        "logistic_results": logistic_results,
        "random_forest_results": random_forest_results
    }


def run_customer_segmentation(
    dataframe
):
    segmented_data, model, silhouette = (
        perform_customer_segmentation(
            dataframe,
            number_of_clusters=4
        )
    )

    segment_summary = describe_segments(
        segmented_data
    )

    display_segment_results(
        segment_summary,
        silhouette
    )

    return {
        "model": model,
        "segmented_data": segmented_data,
        "segment_summary": segment_summary,
        "silhouette_score": silhouette
    }


def run_ml_pipeline(
    dataframe
):
    if dataframe is None:
        raise ValueError(
            "Input DataFrame cannot be None."
        )

    if dataframe.empty:
        raise ValueError(
            "Input DataFrame is empty."
        )

    print("\n" + "=" * 65)
    print("PRODUCTPULSE AI - MACHINE LEARNING ENGINE")
    print("=" * 65)

    print("\nStarting churn prediction...")

    churn_results = run_churn_prediction(
        dataframe
    )

    print("\nStarting customer segmentation...")

    segmentation_results = (
        run_customer_segmentation(
            dataframe
        )
    )

    print("\n" + "=" * 65)
    print("MACHINE LEARNING COMPLETED SUCCESSFULLY")
    print("=" * 65)

    return {
        "churn": churn_results,
        "segmentation": segmentation_results
    }


if __name__ == "__main__":

    print(
        "\n04_ml.py is ready."
    )

    print(
        "This module receives the cleaned "
        "DataFrame from 02_cleaning.py."
    )

    print(
        "It performs churn prediction and "
        "customer segmentation."
    )