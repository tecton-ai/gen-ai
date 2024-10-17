from datetime import timedelta

from data_sources import user_info_src
from entities import user
from tecton import Attribute, batch_feature_view
from tecton.types import Int64, String


@batch_feature_view(
    name="user_profile",
    description="User profile and account status",
    sources=[user_info_src],
    entities=[user],
    mode="pandas",
    batch_schedule=timedelta(days=1),
    aggregation_interval=timedelta(days=1),
    features=[
        Attribute(column="name", column_dtype=String),
        Attribute(column="age", column_dtype=Int64),
        Attribute(column="account_status", column_dtype=String),
    ],
    online=True,
    offline=True,
)
def user_profile(user_info_src):
    return user_info_src[["user_id", "name", "age", "account_status"]]
