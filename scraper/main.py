import fileOperations
import dataOperations
import websiteScraper
import forecasting

import matplotlib.pyplot as plt
import pandas as pd
from alive_progress import alive_bar


def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'
    date_from = "2023-12-08" # YYYY-MM-DD
    date_to = "2023-12-15" # YYYY-MM-DD
    
    total_class_count = dataOperations.get_amount_of_classes(class_file_path)
    current_class = dataOperations.get_next_class(class_file_path)
    total_traffic_df = pd.DataFrame(columns=['end_date'])

    with alive_bar(total_class_count) as bar:
        for class_info_list, class_name, sub_class in current_class:
            driver = websiteScraper.create_driver(url_to_scrape)
            filtered_calendar = dataOperations.gather_and_filter_calendar_information(driver, sub_class, date_from, date_to)

            if(filtered_calendar is not None):
                fileOperations.save_df_to_file(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
                calendar_df = fileOperations.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv", False)
                total_traffic_df = dataOperations.build_total_traffic_df(calendar_df, total_traffic_df)
                forecasting.distribute_to_restaurants(class_info_list[sub_class]["people"], class_info_list[sub_class]["restaurants"])
                
            print("")
            bar()
            driver.refresh()
    
    fileOperations.save_df_to_file(total_traffic_df, f"results/traffic/{date_from}_to_{date_to}.csv")
    total_traffic_df = dataOperations.get_traffic_df(f"results/traffic/{date_from}_to_{date_to}.csv", "calendars/all_classes.json")
    print(dataOperations.get_traffic_by_date(total_traffic_df, "2023-12-08 16:15"))
    print("All calendars successfully scraped!")
    driver.quit()


if __name__ == '__main__':
    main()