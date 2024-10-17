from tecton import BatchSource, FileConfig


user_info_src = BatchSource(
    name="user_info_src",
    batch_config=FileConfig(
        uri="s3://tecton.ai.public/tutorials/transfer-app/user_data.json",
        file_format="json",
    ),
)

tranfer_stats_src = BatchSource(
    name="tranfer_stats_src",
    batch_config=FileConfig(
        uri="s3://tecton.ai.public/tutorials/transfer-app/transfer_data.json",
        file_format="json",
    ),
)
