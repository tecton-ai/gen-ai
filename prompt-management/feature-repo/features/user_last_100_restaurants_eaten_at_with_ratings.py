from tecton import batch_feature_view, Aggregation, on_demand_feature_view
from tecton.types import Field, String, Timestamp, Int64, Struct, Array
from tecton.aggregation_functions import last
from datetime import datetime, timedelta

from entities import user
from data_sources import ratings

@batch_feature_view(
    description='Restaurant features',
    sources=[ratings],
    entities=[user],
    mode='pandas',
    batch_schedule=timedelta(days=1),
    aggregation_interval=timedelta(days=1),
    schema=[Field('user_id', String), Field('restaurant_id', String), Field('timestamp', Timestamp), Field('rating', Int64)],
    timestamp_field='timestamp',
    environment='tecton-rift-core-0.9.0',
    aggregations=[
        Aggregation(name='last_100_restaurants_eaten_at', column='restaurant_id', function=last(100), time_window=timedelta(days=365*5)),
        Aggregation(name='last_100_restaurant_ratings_for_last_100_restaurants_eaten_at', column='rating', function=last(100), time_window=timedelta(days=365*5)),
    ],
    online=True,
    offline=True,
    feature_start_time=datetime(2020,1,1)
)
def user_last_restaurant_ratings(ratings):
    return ratings[['user_id', 'timestamp', 'restaurant_id', 'rating']]


@on_demand_feature_view(
    sources=[user_last_restaurant_ratings],
    mode='python',
    schema=[Field('user_last_100_restaurants_eaten_at_with_ratings', Array(Struct([Field('restaurant_id', String), Field('rating', Int64)])))],
    tags={'llm_enabled': 'True'}
)
def user_last_100_restaurants_eaten_at_with_ratings(user_last_restaurant_ratings):
    restaurants = user_last_restaurant_ratings['last_100_restaurants_eaten_at']
    ratings = user_last_restaurant_ratings['last_100_restaurant_ratings_for_last_100_restaurants_eaten_at']
    restaurants_ratings = [{"restaurant_id": restaurant, "rating": rating} for restaurant, rating in zip(restaurants, ratings)]
    return {'user_last_100_restaurants_eaten_at_with_ratings': restaurants_ratings}