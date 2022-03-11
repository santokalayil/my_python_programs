from app_store_scraper import AppStore
import pandas as pd
import os


def get_reviews(app_name):
    app_search = AppStore(country="in", app_name=app_name)
    app_search.review(how_many=50000)
    return app_search.reviews

def convert_reviews_to_dataframe_n_save_as_csv(reviews, csv_url):

    rows = []
    for review in reviews:
        review_dict = {}
        for key in review:
            if key == 'developerResponse':
                dev = review['developerResponse']
                for key in dev:
                    review_dict[f"developer_response_{key}"] = dev[key]
            else:
                review_dict[key] = review[key]
        rows.append(review_dict)
    df = pd.DataFrame(rows)
    dev_resp_cols = [col for col in df.columns if col.startswith("developer_response_")]
    other_cols = [col for col in df.columns if not col.startswith("developer_response_")]
    df = df[other_cols+dev_resp_cols]
    df.to_csv(csv_url, index=False)

def get_reviews_of_app_from_list(app_names):
    apple_appstore_reviews_dir = "apple_appstore_reviews"
    if not os.path.isdir(apple_appstore_reviews_dir):
        os.mkdir(apple_appstore_reviews_dir)
    
    for app_name in app_names:
        csv_url = os.path.join(apple_appstore_reviews_dir, app_name.replace(" ", "_").replace("/", "_")+".csv")
        reviews = get_reviews(app_name)
        convert_reviews_to_dataframe_n_save_as_csv(reviews, csv_url)


if __name__ == "__main__":
    app_names = [
        "iMobile Pay by ICICI Bank",       # 18292 reviews
    ]


    get_reviews_of_app_from_list(app_names)
