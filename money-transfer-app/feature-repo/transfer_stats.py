from datetime import timedelta

from data_sources import transfer_stats_src
from entities import user
from tecton import Attribute, batch_feature_view
from tecton.types import Int64


@batch_feature_view(
    name="transfer_stats",
    description="User profile and account status",
    sources=[transfer_stats_src],
    entities=[user],
    mode="pandas",
    batch_schedule=timedelta(days=1),
    features=[
        Attribute(column="transfers_in_last_7_days", column_dtype=Int64),
        Attribute(column="transfers_in_last_1_year", column_dtype=Int64),
    ],
    online=True,
    offline=True,
)
def transfer_stats(transfer_stats_src):
    return transfer_stats_src[["user_id", "transfers_in_last_7_days", "transfers_in_last_1_year"]]
