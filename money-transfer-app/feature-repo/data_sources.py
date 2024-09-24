from tecton import BatchSource, FileConfig, RequestSource
from tecton.types import String, Timestamp, Float64, Field, Bool, String
from pandas import Timestamp


user_info_src = BatchSource(
    name='user_info_src',
    batch_config=FileConfig(
        uri='s3://tecton.ai.public/tutorials/transfer-app/user_data.json',
        file_format='json'
    ),
)

tranfer_stats_src = BatchSource(
    name='tranfer_stats_src',
    batch_config=FileConfig(
        uri='s3://tecton.ai.public/tutorials/transfer-app/transfer_data.json',
        file_format='json'
    ),
)




