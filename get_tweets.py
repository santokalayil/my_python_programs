import tweepy
import pandas as pd
import json
import datetime
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


api_key = "YOUR API KEY"
api_key_secret = "YOUR API KEY SECRET"
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR ACCESS TOKEN SECRET"

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


search_keywords = [
    "ukrain", "russia",
]



use_as_hashtag = False  # if this is true with all above search_keywords a hash(#) will be included in front of each word
use_OR = True # use or in search ( by default if space is used between keywords it will check for tweets contain all of them)
remove_retweets = True


keywords_with_hashtags = [f"#{word}" if use_as_hashtag else word for word in search_keywords]
# https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
search_words_as_str = " OR ".join(keywords_with_hashtags) if use_OR else " ".join(keywords_with_hashtags)



# removing ReTweets bcz they contain the same information (if needed to remove based on requirement)
query = f"{search_words_as_str} -filter:retweets" if remove_retweets else search_words_as_str

pages = []  # api.search_tweets, q=query, tweet_mode="extended"
print("getting pages".upper().center(200, " "))

import time
import random

i = 1
minute = 60
waiting_minutes = 15

n_requests = 1

try:
    for page in tweepy.Cursor(api.search_tweets, q=query, count=100, tweet_mode='extended').pages():
        # process status here
        if page:
            print(f"received page [{i}]".ljust(200)) # , end="\r"
            pages.append(page)
            i+=1
            
            if n_requests < 180:
                # time.sleep(random.choice([5,6,7,8,9,10]))
                n_requests+=1
            else:
                print(f"Since number of requests is {n_requests}, waiting for {waiting_minutes} minutes")
                time.sleep(waiting_minutes*minute)
                n_requests = 1 # resetting requests_number
        else:
            print(f"total_pages {i}".ljust(200))
            break
except:
    print("Could Not complete full page downloads due to Limit or connection error")

print(f"Total Number of pages found is {len(pages)}")

rows = []
json_data_list = []

# processing pages
print("processing pages".upper().center(200, " "))
for i, page in enumerate(pages, start=1):
    print(f"Processing page [{i}]".ljust(200), end="\r")

    data = [item for item in page]

    # getting json list data for extra information
    json_data = [data_item._json for data_item in data]
    json_data_list += json_data

    # getting results from cursor

    def run_eval(attr):
        try:
            out = eval(f"item.{attr}")
        except:
            out = "not_found"
        return out

    for item in data:

        item_content = {attr: run_eval(attr) for attr in dir(item) if not attr.startswith("_")}
        tweet_methods = [key for key in item_content.keys() if str(type(item_content[key])) == "<class 'method'>"]

        # item_attr = [attr for attr in dir(item) if not attr.startswith("__")]
        # item_attr_v1 = [attr for attr in item_attr if not attr.startswith("_")] # removing ['_api', '_json']
        item_content = {attr: eval(f"item.{attr}") for attr in dir(item) if not attr.startswith("_")}

        tweet_methods = [key for key in item_content.keys() if str(type(item_content[key])) == "<class 'method'>"] # find what it is
        tweet_sequences = [key for key in item_content.keys() if type(item_content[key]) in [dict, list]]  # more info in lists or dictionaries
        tweet_more_info_fields = [key for key in item_content.keys() if type(item_content[key]) == tweepy.models.User] # more info of data in tweepy objects
        tweet_usable_fields = [key for key in item_content.keys() if key not in tweet_methods+tweet_sequences+tweet_more_info_fields] # single value fields

        record = {field:item_content[field] for field in tweet_usable_fields}

        try:
            entities = item_content['entities']
            media_items = entities['media']

            media_urls = "|||".join([media_item['media_url_https'] for media_item in media_items])
            # media_url = item_content['entities']['media']['media_url_https']

        except:
            media_urls = None

        record['media_urls'] = media_urls

        author = item_content['author']
        author_json = author._json
        # [key for key in author_json.keys() if type(author_json[key]) in [dict, list]]
        author_data = {f"author_{key}": author_json[key] for key in author_json.keys() if type(author_json[key]) not in [dict, list]}
        record.update(author_data)


        rows.append(record)

print(f"In total, {len(rows)} tweets retrieved")

print("creating dataframe out of the records of tweets extracted from pages".upper().center(200, " "))
df = pd.DataFrame(rows)  # creating dataframe out of records list


# removing truncated column and all number_id columns with numbers (duplicates) while keeping all string converted id columns
str_dup_cols = [col for col in df.columns if col.endswith("_str")]
to_remove_cols= [col.rstrip("_str") for col in str_dup_cols]
to_remove_cols.append('truncated')
df.drop(columns=to_remove_cols, inplace=True)

# adding search keywords into the dataframe as a new column
df.loc[:, "search_keywords"] = str(keywords_with_hashtags)  # or search_words_as_str


print("saving data to csv and json formats for later usage".upper().center(200, " "))
# creating unique and understandable filename for json and csv output files
now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") \
    .replace("/", '-')\
    .replace(', ', "_")\
    .replace(":", "-")

# q_name = f"{'OR' if use_OR else 'AND'}_" + query.replace("#","").replace(f" OR ", "_")
# q_name = "hashtag_" +q_name if use_as_hashtag else q_name

q_name = "hashtag_search" if use_as_hashtag else "keyword_search"

filename = f"{now}_{q_name}"

# creating relevant directories
data_dir = "data_outputs"
if not os.path.isdir(data_dir):os.mkdir(data_dir)
csv_dir, json_dir = os.path.join(data_dir, "csv"), os.path.join(data_dir, "json")
for path in (csv_dir, json_dir):
    if not os.path.isdir(path):os.mkdir(path)


# saving to csv
df.to_csv(os.path.join(csv_dir, f"{filename}.csv"), index=False)

# saving to json
with open(os.path.join(json_dir, filename+".json"), 'w') as f:
    json.dump(json_data_list, f)

# serializing pages list object for later access
import pickle
with open("pages.pkl", 'wb') as f:
    pickle.dump(pages, f)
