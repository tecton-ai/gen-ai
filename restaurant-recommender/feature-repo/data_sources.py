from tecton import BatchSource, FileConfig, RequestSource
from tecton.types import Field, String


def users_post_processor(df):
    df["date_of_birth"] = df["date_of_birth"].astype(str)
    return df


users = BatchSource(
    name="users",
    batch_config=FileConfig(
        uri="s3://tecton.ai.public/tutorials/llm_demo/users.parquet",
        file_format="parquet",
        timestamp_field="timestamp",
        post_processor=users_post_processor,
    ),
)


def restaurants_post_processor(df):
    import pandas

    df["timestamp"] = pandas.Timestamp("2020-01-01")
    df = df.rename(columns={"alias": "restaurant_id"}).drop("id", axis=1)
    df_filtered = df[df["restaurant_id"].apply(lambda x: x.isascii())]
    return df_filtered


restaurants = BatchSource(
    name="restaurants",
    batch_config=FileConfig(
        uri="s3://tecton.ai.public/tutorials/llm_demo/yelp_dataset.parquet",
        file_format="parquet",
        timestamp_field="timestamp",
        post_processor=restaurants_post_processor,
    ),
)


def ratings_post_processor(df):
    df_filtered = df[df["restaurant_id"].apply(lambda x: x.isascii())]
    return df_filtered


ratings = BatchSource(
    name="ratings",
    batch_config=FileConfig(
        uri="s3://tecton.ai.public/tutorials/llm_demo/ratings.parquet",
        file_format="parquet",
        timestamp_field="timestamp",
        post_processor=ratings_post_processor,
    ),
)

# real-time location request
request_schema = [Field("location", String)]
user_recommendation_request = RequestSource(schema=request_schema)
