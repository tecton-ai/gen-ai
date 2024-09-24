from tecton import batch_feature_view, Aggregate, on_demand_feature_view, Attribute
from tecton.types import Field, String, Timestamp, Int64, Struct, Array
from tecton.aggregation_functions import last
from datetime import datetime, timedelta

from entities import user
from data_sources import user_info_src

@batch_feature_view(
    name='user_profile'
    description='User profile and account status',
    sources=[user_info_src],
    entities=[user],
    mode='pandas',
    batch_schedule=timedelta(days=1),
    aggregation_interval=timedelta(days=1),
    features=[
        Attribute(column='name', column_dtype=String),
        Attribute(column='age', column_dtype=Int64),
        Attribute(column='account_status', column_dtype=String)
    ],
    online=True,
    offline=True
)
def user_profile(user_info_src):
    return ratings[['user_id', 'name', 'age', 'account_status']]