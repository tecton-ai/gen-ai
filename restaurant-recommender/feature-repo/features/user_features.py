from tecton import batch_feature_view, Attribute
from tecton.types import String
from datetime import datetime, timedelta

from entities import user
from data_sources import users


@batch_feature_view(
    description="User dimension features",
    sources=[users],
    entities=[user],
    mode="pandas",
    batch_schedule=timedelta(days=1),
    features=[
        Attribute(column="preferred_name", column_dtype=String),
        Attribute(column="birth_year", column_dtype=String),
    ],
    timestamp_field="signup_time",
    online=True,
    offline=True,
    feature_start_time=datetime(2020, 1, 1),
    tags={"llm_enabled": "True"},
)
def user_features(users):
    df = users[["user_id", "signup_time"]]
    df["preferred_name"] = users["first_name"]
    df["birth_year"] = users["date_of_birth"].str.slice(0, 4)
    return df
