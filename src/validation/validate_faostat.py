import pandas as pd
from pandera import DataFrameSchema, Column, String, Int, Float, Check
import pandera as pa

def faostat_schema() -> DataFrameSchema:
    return DataFrameSchema(
        {
            "country_code": Column(String, nullable=False, checks=[Check.str_matches(r"^[A-Z]{3}$")]),
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

def validate_faostat(df: pd.DataFrame) -> bool:
    schema = faostat_schema()
    try:
        schema.validate(df, lazy=True)
        return True
    except pa.errors.SchemaError:
        return False
