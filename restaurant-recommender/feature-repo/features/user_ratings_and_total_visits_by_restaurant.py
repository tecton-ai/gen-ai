from tecton import batch_feature_view, Aggregate, Attribute, on_demand_feature_view
from tecton.types import Field, String, Float64, Array, Struct, Int64
from datetime import datetime, timedelta

from entities import user
from data_sources import ratings


@batch_feature_view(
    description="User restaurant engagement features",
    sources=[ratings],
    entities=[user],
    mode="pandas",
    batch_schedule=timedelta(days=1),
    aggregation_interval=timedelta(days=1),
    timestamp_field="timestamp",
    environment="tecton-rift-core-0.9.0",
    aggregation_secondary_key="restaurant_id",
    features=[
        Aggregate(
            name="users_average_rating_by_restaurant_last_5y",
            column="rating",
            column_dtype=Int64,
            function="mean",
            time_window=timedelta(days=365 * 5),
        ),
        Aggregate(
            name="users_total_visits_by_restaurant_last_5y",
            column="rating",
            column_dtype=Int64,
            function="count",
            time_window=timedelta(days=365 * 5),
        ),
    ],
    online=True,
    offline=True,
    feature_start_time=datetime(2020, 1, 1),
)
def user_engagement_by_restaurant_features(ratings):
    return ratings[["user_id", "restaurant_id", "timestamp", "rating"]]


@on_demand_feature_view(
    description="User ratings and total visits by restaurant",
    sources=[user_engagement_by_restaurant_features],
    mode="python",
    features=[
        Attribute(
            column="user_ratings_and_total_visits_by_restaurant",
            column_dtype=Array(
                Struct(
                    [
                        Field("restaurant_id", String),
                        Field("average_rating", Float64),
                        Field("total_visits", Int64),
                    ]
                )
            ),
        )
    ],
    tags={"llm_enabled": "True"},
)
def user_ratings_and_total_visits_by_restaurant(
    user_ratings_and_total_visits_by_restaurant_raw,
):
    restaurants = user_ratings_and_total_visits_by_restaurant_raw["restaurant_id_keys_1825d"]
    ratings = user_ratings_and_total_visits_by_restaurant_raw["users_average_rating_by_restaurant_last_5y"]
    visits = user_ratings_and_total_visits_by_restaurant_raw["users_total_visits_by_restaurant_last_5y"]

    result = []
    for restaurant, rating, visit in zip(restaurants, ratings, visits):
        result.append(
            {
                "restaurant_id": restaurant,
                "average_rating": rating,
                "total_visits": visit,
            }
        )

    return {"user_ratings_and_total_visits_by_restaurant": result}
