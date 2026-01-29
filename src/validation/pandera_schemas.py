from pandera import DataFrameSchema, Column, String, Int, Float, Check
import pandera as pa
import pandas as pd

def faostat_schema() -> DataFrameSchema:
    # Minimal validated schema for FAOSTAT-like interim data
    return DataFrameSchema(
        {
            "country_code": Column(String, nullable=True, checks=[Check.str_matches(r"^[A-Z]{3}$")]),
            "year": Column(Int, nullable=False, checks=[Check.ge(0)]),
            "indicator_id": Column(String, nullable=True),
            "indicator_name": Column(String, nullable=True),
            "indicator_value": Column(Float, nullable=True),
            "quality_score": Column(Float, nullable=True),
            "data_source": Column(String, nullable=True),
            "ingestion_timestamp": Column(String, nullable=True),
        },
        strict=True,
    )
