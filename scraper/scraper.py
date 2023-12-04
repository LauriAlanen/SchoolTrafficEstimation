import fileOperations as fo
import dataOperations as do
import websiteOperations as wo

import matplotlib.pyplot as plt
import pandas as pd
from alive_progress import alive_bar


def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'
    all_classes_df = do.get_all_classes(class_file_path)
    date_from = "2024-02-10" # YYYY-MM-DD
    date_to = "2024-02-20" # YYYY-MM-DD
    
    total_class_count = do.get_amount_of_classes(all_classes_df)
    current_class = do.get_next_class(all_classes_df)

    total_traffic_df = pd.DataFrame(columns=['end_date'])

    with alive_bar(total_class_count) as bar:
        for class_info_list, class_name, sub_class in current_class:
            driver = wo.create_driver(url_to_scrape)
            filtered_calendar = do.gather_and_filter_calendar_information(driver, sub_class, date_from, date_to)

            if(filtered_calendar is not None):
                fo.save_df_to_file(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
                calendar_df = fo.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv", silent=False)
                total_traffic_df = do.build_total_traffic_df(calendar_df, total_traffic_df)

            print("")
            bar()
            driver.refresh()
    
    print("All calendars successfully scraped!")
    fo.save_df_to_file(total_traffic_df, f"results/traffic/{date_from}_to_{date_to}.csv")

    
    driver.quit()


if __name__ == '__main__':
    main()