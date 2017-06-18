import twitter
import re
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import urllib
import datetime
import pprint

# Can maybe remove these imports
import nltk
import json
import numpy as np
from nltk.corpus import stopwords


from pymongo import MongoClient


client = MongoClient()
db = client.test_database

# Use Twitter API to get all tweets from a specific handle
api = twitter.Api(consumer_key='uJGBbVHC8Ph8Qe2HFIxO6v7bX',
                  consumer_secret='78NZzYNcbrHkU2wGKnmbooj0nbUXq3e5Ot9ofpgsPJm2varhiZ',
                  access_token_key= '869585426520170500-CgymaP0a37Y0cU5iSAIVa1XY9B7ruap',
                  access_token_secret='1bzkszzLcnsaOw2mYsC8p9Qt5f2nKkcgBBxXbKyOg7azg')

def fetch_tweets(from_handle=None, to_handle=None, keywords=None, filter_replies=True, reply_id=None):
    # Function to retrieve Tweets for sent to/from a specific Twitter handle and/or that mention a specific keyword

    # If the tweets are already in the Tweet database, return null
    if check_cache(from_handle):
        # collection = db[from_handle]

        # cur = collection.find({})
        # x   = []
        # for i in cur:
        #     x.append(i)
        # print(x)

        return None

    # Otherwise, build up a query to send to the Twitter API to retrieve the tweets
    else:
        query = ""

        if from_handle is not None:
            query +='from:'+ from_handle

        if to_handle is not None:
            query += 'to:'+ to_handle

        if keywords:
            query += " " + keywords

        if filter_replies:
            query += " AND -filter:replies"

        else:
            pass

        query = urllib.parse.quote(query)
        query = 'q=' + query
        if reply_id is not None:
            query += '&count=100000'
            query += '&since_id='+str(reply_id)
        else:
            query += '&count=20'

        print(query)
        results = api.GetSearch(raw_query=query)

        replies = []
        if reply_id is not None:
            for r in results:
                if r.in_reply_to_status_id == int(reply_id):
                    print("ayyy")
                    replies.append(r)
            return replies

        return results

def extract_data(text):
    # Use Watson's NLU API to extract the keywords, entities and concepts from a text
    bm_username = "d48f7c58-cfe1-4e8f-a482-7d06cc88e76b"
    bm_password = "Cg5jF1jfcz8d"

    nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                username=bm_username,
                                                                password=bm_password)
    ents = nlu.analyze(text=text,
                        features=[features.Entities(), features.Keywords(), features.Concepts()])

    ents["tweet"] = text
    return ents

def store_tweet_data_pairs(pairs, handle):
    # Store Tweet IDs + Watson's analysis of Tweets as pairs the database
    collection = db[handle]

    handle_id = collection.insert_one(pairs).inserted_id

    # Update the cache collection (table)
    update_cache(handle, datetime.datetime.utcnow())

def store_tweets_to(tweets, handle):
    handle = "to_" + handle
    # Store Tweets + Watson's analysis of Tweets as pairs the database
    collection = db[handle]

    collection.insert_one(tweets).inserted_id

    # Update the cache collection (table)
    update_cache(handle, datetime.datetime.utcnow())


def check_cache(handle):
    # Returns True if the handle passed is in is in the cache collection (table)
    # and if the date in the cache is less than 4 hours ago

    # If this function returns True, it means there are recent enough tweets
    # in the database, so they should be pulled from there rather than the
    # Twitter API

    collection = db.cache

    result = collection.find_one({"handle" : handle})

    if result is None:
        return False

    else:
        current_datetime = datetime.datetime.utcnow()
        time_diff = datetime.datetime.utcnow() - result["last_modified"]

        if time_diff.total_seconds() > 14400:
            return False
        else:
            return True

def update_cache(handle, time):
    # Updates the cache collection (table) when Tweets are stored in thex
    # main Tweets database
    collection = db.cache

    result = collection.find_one({"handle" : handle})
    if result is None:
        cache_id = collection.insert_one({"last_modified": time,
                                          "handle" : handle})
    else:
        collection.update(result, {"last_modified": time, "handle" : handle})



# Defines the handle to pull tweets from
from_hand = "applesupport"

# Returns tweets sent by the defined handle
tweets = fetch_tweets(from_handle=from_hand)

if tweets:
    processed_tweets = {}

    # URLs and . characters create issues so remove them
    # Build up a dictionary of {Tweet text : Tweet JSON object}
    for t in tweets:
        t.text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', t.text).replace(".", " ")
        processed_tweets[t.text] = t

    # Build up a dictionary of {Tweet ID : entities, concepts, keywords contained in tweet}
    tweet_data = {}
    for t in processed_tweets.keys():
        tweet_id = processed_tweets[t].id_str
        data = extract_data(t)
        tweet_data[tweet_id] = data

    replies = {}

    for t_id in tweet_data:
        results = fetch_tweets(to_handle=from_hand, reply_id=t_id, filter_replies=False)
        replies[t_id] = results

    print(replies)

    # Store built up dictionary in the database
    store_tweet_data_pairs(tweet_data, from_hand)




    # related_tweets = {}
    # # Get Tweets sent to organizations mentioning the concepts/entities/keywords
    # for t in text_only_tweet_data:

    #     obj = {}
    #     for key in keys:
    #         obj[key] = {}

    #         for i in t[key]:
    #             obj[key][i] = []

    #             results = fetch_tweets(to_handle=from_hand, in_reply_to_status_id=)

    #             for r in results:
    #                 obj[key][i].append({
    #                     "text": r.text,
    #                     "date": r.created_at
    #                 })

    #     related_tweets[t["text"]] = obj

    # pprint.pprint(related_tweets)

    # store_tweets_to(related_tweets, from_hand)

else:
    pass

#def tweet_cleaner(tweet):
#     # Function to process raw tweet

#     # Remove any URLs from the tweet
#     # no_URLs = re.sub(
#     #     "[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
#     #     " ",
#     #     tweet)

#     # Remove non-letters
#     letters_only = re.sub("[^a-zA-Z]", " ", tweet)

#     # Convert to lower case, split into individual words
#     words = letters_only.lower().split()

#     # Remove stop words
#     stops = set(stopwords.words("english"))
#     meaningful_words = [w for w in words if not w in stops]

#     return( " ".join( meaningful_words ))


# # print("Cleaning and parsing Tweets...\n")
# # clean_tweets = []
# # for i in range(0, len(tweets)):
# #     # If the index is evenly divisible by 1000, print a message
# #     if( (i+1)%1000 == 0 ):
# #         print("Review %d of %d\n" % ( i+1, tweets.size ))
# #     clean_tweets.append(tweet_cleaner(tweets[i]))

# # print(clean_tweets
