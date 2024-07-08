from tecton import on_demand_feature_view, FeatureService
from tecton.types import Field, String, Timestamp, Struct, Bool, Array, Int64, Float64
from datetime import datetime, timedelta

from data_sources import user_recommendation_request
from features.user_ratings_and_total_visits_by_cuisine import user_ratings_and_total_visits_by_cuisine_raw


# on-demand feature view that constructs the system prompt
@on_demand_feature_view(
    name="restaurant_recommender_prompt:v1",
    sources=[user_recommendation_request],
    mode="python",
    schema=[Field("system_prompt", String)],
    description="Contextual prompt for recommending a restaurant",
)
def restaurant_recommender_prompt_v1(user_recommendation_request):
    
    consierge_system_template = """
        You are a consierge service that recommends restaurants. 
        Your response always includes at least one specific restaurant recommendation 
        Also suggests menu items from the recommended restaurant. 
        Provide the address for the restaurant you recommend.
        Recommend places that are close to {location}.
        Unless prompted by the user, provide choices appropriate for this time: {time}
        You treat them like a good friend."
    """

    prompt_with_context = consierge_system_template.format(
        location=user_recommendation_request["location"],
        time=datetime.now().strftime("%H:%M")
    )

    return {"system_prompt": prompt_with_context}


#Create a variant ODFV for feature enhanced prompt with additional knowledge of the user
@on_demand_feature_view(
    name="restaurant_recommender_prompt:v2", #variant name for versioning
    sources=[user_recommendation_request, user_ratings_and_total_visits_by_cuisine_raw],
    mode="python",
    schema=[Field("system_prompt", String)],
    description="Contextual prompt for recommending a restaurant",
)
def restaurant_recommender_prompt_v2(user_recommendation_request, user_ratings_and_total_visits_by_cuisine_raw):
    
    consierge_system_template = """
        You are a consierge service that recommends restaurants. 
        Your response always includes at least one specific restaurant recommendation and suggests menu items. 
        Provide the address for the restaurant you recommend.
        Recommend places that are close to {location}.
        If they don't provide a cuisine choose one based on this data:
        {cuisine_data}
        Unless prompted by the user, provide choices appropriate for this time: {time}

        You treat them like a good friend."
    """

    # use preaggregated values from user's rating history
    cuisines = user_ratings_and_total_visits_by_cuisine_raw['cuisine_keys_1825d']
    ratings = user_ratings_and_total_visits_by_cuisine_raw['users_average_rating_by_cuisine_last_5y']
    visits = user_ratings_and_total_visits_by_cuisine_raw['users_total_visits_by_cuisine_last_5y']
    
    cuisine_ratings = []
    for cuisine, rating, visit in zip(cuisines, ratings, visits):
        cuisine_ratings.append({
            'cuisine': cuisine,
            'average_rating': rating,
            'total_visits': visit
        })
        
    prompt_with_context = consierge_system_template.format(
        location = user_recommendation_request["location"],
        time = datetime.now().strftime("%H:%M"),
        cuisine_data = str(cuisine_ratings)
    )

    return {"system_prompt": prompt_with_context}

prompt_restaurant_recommender = FeatureService(
    name = "prompt_restaurant_recommender:v1",
    description = "GenAI prompt for Restaurant Recommender system.",
    features = [restaurant_recommender_prompt_v1],
)

prompt_restaurant_recommender = FeatureService(
    name = "prompt_restaurant_recommender:v2",
    description = "GenAI prompt for Restaurant Recommender system.",
    features = [restaurant_recommender_prompt_v2],
)
