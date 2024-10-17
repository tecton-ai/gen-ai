from tecton import Entity
from tecton.types import Field, String

user = Entity(name="user", join_keys=[Field("user_id", String)])
restaurant = Entity(name="restaurant", join_keys=[Field("restaurant_id", String)])
