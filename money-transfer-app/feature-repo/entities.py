from tecton import Entity
from tecton.types import Field, String

user = Entity(name='user', join_keys=[Field("user_id", String)])
