from cloudant.client import Cloudant
from cloudant.error import CloudantException
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .local_params_settings import COUCH_URL, COUCH_USERNAME, IAM_API_KEY, API_URL_SENTIMENT, API_KEY_NLU

# API_URL_DEALERSHIP, API_URL_REVIEW, API_URL_SENTIMENT

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    try:
        print("params: ",kwargs)
        if api_key:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key),
                                        params=kwargs)
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                        params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        json_data = json.loads(response.text)
        return response
    except:
        print(json_data)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    results = []
    json_result = get_request(url)
    if json_result:
        dealerships = json_result['dealerships']
        for anydealer in dealerships:
            dealer = CarDealer(
                id=anydealer["id"],
                full_name=anydealer["full_name"],
                short_name=anydealer["short_name"],
                address=anydealer["address"], 
                city=anydealer["city"],
                state=anydealer["state"], 
                st=anydealer["st"], 
                zip=anydealer["zip"],
                lat=anydealer["lat"], 
                long=anydealer["long"]
            )
            results.append(dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["reviews"]
        for anyreview in reviews:
            sentiment = analyze_review_sentiments(anyreview["review"])
            review = {}
            if anyreview["purchase"]:
                review = DealerReview(
                  id=anyreview["id"],
                  name=anyreview["name"],
                  dealership=anyreview["dealership"],
                  review=anyreview["review"],
                  purchase=anyreview["purchase"],
                  car_make=anyreview["car_make"],
                  car_model=anyreview["car_model"],
                  car_year=anyreview["car_year"],
                  purchase_date=anyreview["purchase_date"],
                  sentiment=sentiment)
            else:
                review = DealerReview(
                  id=anyreview["id"],
                  name=anyreview["name"],
                  dealership=anyreview["dealership"],
                  review=anyreview["review"],
                  purchase=anyreview["purchase"],
                  car_make=None,
                  car_model=None,
                  car_year=None,
                  purchase_date=None,
                  sentiment=sentiment)                   
            results.append(review)
    return results


def add_dealer_review(review_to_post):
    review = {
        "id": review_to_post['review_id'],
        "name": review_to_post['reviewer_name'],
        "dealership": review_to_post['dealership'],
        "review": review_to_post['review'],
        "purchase": review_to_post.get('purchase', False),
        "purchase_date": review_to_post.get('purchase_date'),
        "car_make": review_to_post.get('car_make'),
        "car_model": review_to_post.get('car_model'),
        "car_year": review_to_post.get('car_year')
    }
    return post_request(API_URL_REVIEW, review)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
#    sentiment_result="not analyzed"
#    try:
#        json_result = get_request(API_URL_SENTIMENT, api_key=API_KEY_NLU, features="sentiment", text=text)
#        print(json_result)
#        if json_result:
#            sentiment_result = json_result["sentiment"]["document"]["label"]
#    finally:
#        print(text)
#        print(sentiment_result)
#        return sentiment_result

    authenticator = IAMAuthenticator(API_KEY_NLU)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator)
    
    natural_language_understanding.set_service_url(API_URL_SENTIMENT)
    
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            entities=EntitiesOptions(emotion=True, sentiment=True, limit=2),
            keywords=KeywordsOptions(emotion=True, sentiment=True,limit=2))).get_result()
    return response["keywords"][0]["sentiment"]["label"]
