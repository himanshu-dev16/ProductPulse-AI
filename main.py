import importlib


def find_function(module, function_names):
    for function_name in function_names:
        if hasattr(module, function_name):
            function = getattr(module, function_name)

            if callable(function):
                return function

    available_functions = [
        name
        for name in dir(module)
        if callable(getattr(module, name))
        and not name.startswith("_")
    ]

    raise AttributeError(
        f"No compatible function found in "
        f"{module.__name__}. "
        f"Available functions: {available_functions}"
    )


def run_pipeline():
    print("\n" + "=" * 70)
    print("PRODUCTPULSE AI - COMPLETE DATA ANALYTICS PIPELINE")
    print("=" * 70)

    print("\n[1/6] Loading data...")

    ingestion = importlib.import_module(
        "01_ingestion"
    )

    ingestion_function = find_function(
        ingestion,
        [
            "run_ingestion_pipeline",
            "load_data",
            "ingest_data",
            "load_dataset",
            "run_ingestion"
        ]
    )

    dataframe = ingestion_function()

    if dataframe is None:
        raise ValueError(
            "01_ingestion.py did not return a DataFrame."
        )

    print(
        f"\nData loaded successfully: "
        f"{len(dataframe)} rows x "
        f"{len(dataframe.columns)} columns"
    )

    print("\n[2/6] Cleaning data...")

    cleaning = importlib.import_module(
        "02_cleaning"
    )

    cleaning_function = find_function(
        cleaning,
        [
            "run_cleaning_pipeline",
            "clean_data",
            "clean_dataframe",
            "clean_dataset",
            "run_cleaning"
        ]
    )

    cleaned_data = cleaning_function(
        dataframe
    )

    if cleaned_data is None:
        raise ValueError(
            "02_cleaning.py did not return "
            "the cleaned DataFrame."
        )

    print(
        f"\nCleaning completed: "
        f"{len(cleaned_data)} rows x "
        f"{len(cleaned_data.columns)} columns"
    )

    print("\n[3/6] Running business analysis...")

    analysis = importlib.import_module(
        "03_analysis"
    )

    analysis_function = find_function(
        analysis,
        [
            "run_analysis_pipeline",
            "run_analysis",
            "analyze_data",
            "analyze_dataframe",
            "perform_analysis"
        ]
    )

    analysis_results = analysis_function(
        cleaned_data
    )

    print(
        "\nBusiness analysis completed."
    )

    print("\n[4/6] Running machine learning...")

    ml = importlib.import_module(
        "04_ml"
    )

    ml_function = find_function(
        ml,
        [
            "run_ml_pipeline",
            "run_machine_learning",
            "run_ml",
            "train_models"
        ]
    )

    ml_results = ml_function(
        cleaned_data
    )

    if not isinstance(
        ml_results,
        dict
    ):
        raise ValueError(
            "04_ml.py must return a dictionary "
            "containing ML results."
        )

    if "churn" not in ml_results:
        raise ValueError(
            "ML results do not contain churn results."
        )

    if "segmentation" not in ml_results:
        raise ValueError(
            "ML results do not contain segmentation results."
        )

    churn_results = ml_results[
        "churn"
    ]

    segmentation_results = ml_results[
        "segmentation"
    ]

    churn_data = churn_results[
        "churn_data"
    ]

    segmented_data = segmentation_results[
        "segmented_data"
    ]

    enriched_data = churn_data.copy()

    if "customer_segment" in segmented_data.columns:
        enriched_data[
            "customer_segment"
        ] = segmented_data[
            "customer_segment"
        ].values

    print(
        "\nMachine learning completed."
    )

    print("\n[5/6] Generating AI business insights...")

    ai = importlib.import_module(
        "05_ai"
    )

    ai_function = find_function(
        ai,
        [
            "run_ai_pipeline",
            "run_ai",
            "generate_ai_insights",
            "generate_business_insights"
        ]
    )

    ai_results = ai_function(
        enriched_data
    )

    if not isinstance(
        ai_results,
        dict
    ):
        raise ValueError(
            "05_ai.py must return a dictionary."
        )

    if "enriched_data" not in ai_results:
        raise ValueError(
            "AI results do not contain "
            "enriched_data."
        )

    final_data = ai_results[
        "enriched_data"
    ]

    print(
        "\nAI business intelligence completed."
    )

    print("\n[6/6] Exporting final dataset...")

    export = importlib.import_module(
        "06_export"
    )

    export_function = find_function(
        export,
        [
            "run_export_pipeline",
            "export_data",
            "export_dataframe",
            "run_export"
        ]
    )

    export_results = export_function(
        final_data
    )

    print("\n" + "=" * 70)
    print(
        "PRODUCTPULSE AI - PIPELINE COMPLETED"
    )
    print("=" * 70)

    print(
        f"\nFinal dataset: "
        f"{len(final_data)} rows x "
        f"{len(final_data.columns)} columns"
    )

    print(
        "\nAvailable final columns:"
    )

    for column in final_data.columns:
        print(
            f"- {column}"
        )

    print(
        "\nAll six pipeline stages completed successfully."
    )

    return {
        "raw_data": dataframe,
        "cleaned_data": cleaned_data,
        "analysis_results": analysis_results,
        "ml_results": ml_results,
        "ai_results": ai_results,
        "final_data": final_data,
        "export_results": export_results
    }


if __name__ == "__main__":
    try:
        run_pipeline()

    except Exception as error:

        print("\n" + "=" * 70)
        print("PRODUCTPULSE AI - PIPELINE ERROR")
        print("=" * 70)

        print(
            f"\nError: {error}"
        )

        print(
            "\nCheck the function names and configuration "
            "in the project files."
        )

        raise