from tecton import batch_feature_view, Attribute
from tecton.types import Field, String, Timestamp, Struct, Bool, Array, Int64, Float64
from datetime import datetime, timedelta

from entities import restaurant
from data_sources import restaurants

restaurant_features_schema = [
    Field("restaurant_id", String),
    Field("timestamp", Timestamp),
    Field("name", String),
    Field("image_url", String),
    Field("is_closed", Bool),
    Field("url", String),
    Field("review_count", Int64),
    Field("categories", Array(Struct([Field("alias", String), Field("title", String)]))),
    Field("rating", Float64),
    Field("coordinates", Struct([Field("latitude", Float64), Field("longitude", Float64)])),
    Field("transactions", Array(String)),
    Field("price", String),
    Field(
        "location",
        Struct(
            [
                Field("address1", String),
                Field("address2", String),
                Field("address3", String),
                Field("city", String),
                Field("zip_code", String),
                Field("country", String),
                Field("state", String),
                Field("display_address", Array(String)),
            ]
        ),
    ),
    Field("phone", String),
    Field("display_phone", String),
    Field("distance", Float64),
    Field(
        "attributes",
        Struct(
            [
                Field("business_temp_closed", Bool),
                Field("menu_url", String),
                Field("open24_hours", Bool),
                Field("waitlist_reservation", Bool),
            ]
        ),
    ),
    Field("encid", String),
    Field(
        "operationHours",
        Struct(
            [
                Field(
                    "regularHoursMergedWithSpecialHoursForCurrentWeek",
                    Array(
                        Struct(
                            [
                                Field("dayOfWeekShort", String),
                                Field("regularHoursRaw", Array(Array(Int64))),
                                Field("__typename", String),
                            ]
                        )
                    ),
                ),
                Field("__typename", String),
            ]
        ),
    ),
    Field("popularItems", Array(String)),
]


@batch_feature_view(
    description="Restaurant dimension features",
    sources=[restaurants],
    entities=[restaurant],
    mode="pandas",
    batch_schedule=timedelta(days=1),
    features=[
        Attribute(column="name", column_dtype=String),
        Attribute(column="image_url", column_dtype=String),
        Attribute(column="is_closed", column_dtype=Bool),
        Attribute(column="url", column_dtype=String),
        Attribute(column="review_count", column_dtype=Int64),
        Attribute(
            column="categories",
            column_dtype=Array(Struct([Field("alias", String), Field("title", String)])),
        ),
        Attribute(column="rating", column_dtype=Float64),
        Attribute(
            column="coordinates",
            column_dtype=Struct([Field("latitude", Float64), Field("longitude", Float64)]),
        ),
        Attribute(column="transactions", column_dtype=Array(String)),
        Attribute(column="price", column_dtype=String),
        Attribute(
            column="location",
            column_dtype=Struct(
                [
                    Field("address1", String),
                    Field("address2", String),
                    Field("address3", String),
                    Field("city", String),
                    Field("zip_code", String),
                    Field("country", String),
                    Field("state", String),
                    Field("display_address", Array(String)),
                ]
            ),
        ),
        Attribute(column="phone", column_dtype=String),
        Attribute(column="display_phone", column_dtype=String),
        Attribute(column="distance", column_dtype=Float64),
        Attribute(
            column="attributes",
            column_dtype=Struct(
                [
                    Field("business_temp_closed", Bool),
                    Field("menu_url", String),
                    Field("open24_hours", Bool),
                    Field("waitlist_reservation", Bool),
                ]
            ),
        ),
        Attribute(column="encid", column_dtype=String),
        Attribute(
            column="operationHours",
            column_dtype=Struct(
                [
                    Field(
                        "regularHoursMergedWithSpecialHoursForCurrentWeek",
                        Array(
                            Struct(
                                [
                                    Field("dayOfWeekShort", String),
                                    Field("regularHoursRaw", Array(Array(Int64))),
                                    Field("__typename", String),
                                ]
                            )
                        ),
                    ),
                    Field("__typename", String),
                ]
            ),
        ),
        Attribute(column="popularItems", column_dtype=Array(String)),
    ],
    timestamp_field="timestamp",
    online=True,
    offline=True,
    feature_start_time=datetime(2020, 1, 1),
    environment="tecton-rift-core-0.9.0",
)
def restaurant_features(restaurants):
    return restaurants[
        [
            "restaurant_id",
            "timestamp",
            "name",
            "image_url",
            "is_closed",
            "url",
            "review_count",
            "categories",
            "rating",
            "coordinates",
            "transactions",
            "price",
            "location",
            "phone",
            "display_phone",
            "distance",
            "attributes",
            "encid",
            "operationHours",
            "popularItems",
        ]
    ]
