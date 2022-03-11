
from google_play_scraper import app
from google_play_scraper import Sort, reviews
import pandas as pd
import numpy as np
import os


def get_reviews(app_id):
    rows = []
    result, continuation_token = reviews(
        app_id,
        lang='en', # defaults to 'en'
        country='in', # defaults to 'us'
        sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
        count=200, # defaults to 100
        # filter_score_with=5 # defaults to None(means all score)
    )

    rows += result
    # If you pass `continuation_token` as an argument to the reviews function at this point,
    # it will crawl the items after 3 review items.
    # more_views = True
    iteration = 0
    while continuation_token.token and (len(rows) <= 50000):
    # while result:
        iteration += 1
        print(f"Iteration number : {iteration}")
        result, continuation_token = reviews(
            app_id,
            continuation_token=continuation_token # defaults to None(load from the beginning)
        )
        rows += result
        print(f"Total_reviews so far is {len(rows)}")


    df = pd.DataFrame(rows)


    result = app(
        app_id,
        lang='en', # defaults to 'en'
        country='in' # defaults to 'us'
    )

    print(f"retrived total of {len(rows)} for app -> {result['title']}")

    app_reviews_folder = "app_reviews"
    if not os.path.isdir(app_reviews_folder):
        os.mkdir(app_reviews_folder)
    csv_file_name = result['title'].replace(" ", "_").replace("/", "_")+"__"+app_id.replace(".", "_")
    csv_url = os.path.join(app_reviews_folder, csv_file_name+".csv")
    df.to_csv(csv_url, index=False)
    print(f"saved reviews for {app_id} to {csv_url}")

if __name__ == "__main__":
    app_ids = [
        # "com.thoughtripples.Syromalankara", # for test
        "org.nic.entejilla", # for test
        # "com.pesitonew.india", # for test

    ]


    for app_id in app_ids:
        print(app_id.center(100, "-"))
        get_reviews(app_id)
