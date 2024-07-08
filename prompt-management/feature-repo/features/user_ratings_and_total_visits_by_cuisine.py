from tecton import batch_feature_view, Aggregation, on_demand_feature_view
from tecton.types import Field, String, Timestamp, Float64, Array, Struct, Int64
from datetime import datetime, timedelta

from entities import user
from data_sources import ratings, restaurants

@batch_feature_view(
    description='User ratings and total visits by cuisine',
    sources=[ratings, restaurants],
    entities=[user],
    mode='pandas',
    batch_schedule=timedelta(days=1),
    aggregation_interval=timedelta(days=1),
    schema=[Field('user_id', String), Field('cuisine', String), Field('timestamp', Timestamp), Field('rating', Int64)],
    timestamp_field='timestamp',
    environment='tecton-rift-core-0.9.0',
    aggregation_secondary_key='cuisine',
    aggregations=[
        Aggregation(name='users_average_rating_by_cuisine_last_5y', column='rating', function='mean', time_window=timedelta(days=365*5)),
        Aggregation(name='users_total_visits_by_cuisine_last_5y', column='rating', function='count', time_window=timedelta(days=365*5))
    ],
    online=True,
    offline=True,
    feature_start_time=datetime(2020,1,1)
)
def user_ratings_and_total_visits_by_cuisine_raw(ratings, restaurants):
    df = ratings.merge(restaurants, on='restaurant_id', how='left').explode('categories')
    df['cuisine'] = df['categories'].apply(lambda x: x['title'])
    df['rating'] = df['rating_x']
    df['timestamp'] = df['timestamp_x']
    return df[['user_id', 'cuisine', 'timestamp', 'rating']]


@on_demand_feature_view(
    description='User ratings and total visits by cuisine',
    sources=[user_ratings_and_total_visits_by_cuisine_raw],
    mode='python',
    schema=[Field('user_ratings_and_total_visits_by_cuisine', Array(Struct([Field('cuisine', String), Field('average_rating', Float64), Field('total_visits', Int64)])))],
    tags={'llm_enabled': 'True'}
)
def user_ratings_and_total_visits_by_cuisine(user_ratings_and_total_visits_by_cuisine_raw):
    cuisines = user_ratings_and_total_visits_by_cuisine_raw['cuisine_keys_1825d']
    ratings = user_ratings_and_total_visits_by_cuisine_raw['users_average_rating_by_cuisine_last_5y']
    visits = user_ratings_and_total_visits_by_cuisine_raw['users_total_visits_by_cuisine_last_5y']
    
    result = []
    for cuisine, rating, visit in zip(cuisines, ratings, visits):
        result.append({
            'cuisine': cuisine,
            'average_rating': rating,
            'total_visits': visit
        })
    
    return {'user_ratings_and_total_visits_by_cuisine': result}