from tecton import batch_feature_view, Aggregate, on_demand_feature_view, Attribute
from tecton.types import Field, String, Timestamp, Int64, Struct, Array
from tecton.aggregation_functions import last
from datetime import datetime, timedelta

from entities import user
from data_sources import tranfer_stats_src

@batch_feature_view(
    name='transfer_stats'
    description='User profile and account status',
    sources=[tranfer_stats_src],
    entities=[user],
    mode='pandas',
    batch_schedule=timedelta(days=1),
    features=[
        Attribute(column='transfers_in_last_7_days', column_dtype=Int64),
        Attribute(column='transfers_in_last_1_year', column_dtype=Int64)
    ],
    online=True,
    offline=True
)
def transfer_stats(tranfer_stats_src):
    return ratings[['user_id', 'transfers_in_last_7_days', 'transfers_in_last_1_year']]