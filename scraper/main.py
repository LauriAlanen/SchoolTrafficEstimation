import fileOperations as fo
import dataOperations as do
import websiteScraper as ws
import forecasting

import matplotlib.pyplot as plt
import pandas as pd
from alive_progress import alive_bar


def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'
    date_from = "2023-12-8" # YYYY-MM-DD
    date_to = "2023-12-15" # YYYY-MM-DD
    
    all_classes_df = do.get_all_classes(class_file_path)
    total_class_count = do.get_amount_of_classes(all_classes_df)
    current_class = do.get_next_class(all_classes_df)

    total_traffic_df = pd.DataFrame(columns=['end_date'])
    total_restaurant_distribution = [0, 0, 0, 0, 0, 0, 0, 0]

    restaurants = {
        "Cotton Club" : 0,
        "August Restaurant" : 0,
        "Cafe Techno" : 0,
        "Restaurant W33" : 0,
        "Juvenes Mathilda" : 0,
        "Juvenes Alma" : 0,
        "Juvenes Alere" : 0,
        "Juvenes Serveri" : 0
    }

    #with alive_bar(total_class_count) as bar:
    #    for class_info_list, class_name, sub_class in current_class:
    #        driver = ws.create_driver(url_to_scrape)
    #        filtered_calendar = do.gather_and_filter_calendar_information(driver, sub_class, date_from, date_to)
#
    #        if(filtered_calendar is not None):
    #            fo.save_df_to_file(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
    #            calendar_df = fo.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv", silent=False)
    #            total_traffic_df = do.build_total_traffic_df(calendar_df, total_traffic_df)
#
    #        print("")
    #        bar()
    #        driver.refresh()
    #
    #print("All calendars successfully scraped!")
    #fo.save_df_to_file(total_traffic_df, f"results/traffic/{date_from}_to_{date_to}.csv")

    total_traffic_df = do.get_traffic_df(f"results/traffic/{date_from}_to_{date_to}.csv", all_classes_df)
    for date in total_traffic_df:
        total_restaurant_distribution = do.get_restaurant_traffic(all_classes_df, total_traffic_df, total_restaurant_distribution, date)
        restaurants = do.connect_distribution_to_restaurant(total_restaurant_distribution, restaurants)
        print(f"At date {date} restaurants are distributed {restaurants}")
        total_restaurant_distribution = [0, 0, 0, 0, 0, 0, 0, 0]
    #driver.quit()


if __name__ == '__main__':
    main()