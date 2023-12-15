""" Main file for the scraper. Which is used to scrape lukkarit.vamk.fi for calendar data."""
import file_operations
import data_operations
import website_controller

import pandas as pd
from alive_progress import alive_bar


def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'
    all_classes_df = data_operations.get_all_classes(class_file_path)
    date_from, date_to = file_operations.get_file_dates()
    print(f"Scraping calendars from {date_from} to {date_to}...")

    total_class_count = data_operations.get_amount_of_classes(all_classes_df)
    current_class = data_operations.get_next_class(all_classes_df)

    total_traffic_df = pd.DataFrame(columns=['end_date'])

    with alive_bar(total_class_count) as bar:
        for _, class_name, sub_class in current_class:
            driver = website_controller.create_driver(url_to_scrape)
            filtered_calendar = data_operations.get_calendar(driver, sub_class, date_from, date_to)

            if filtered_calendar is not None:
                file_operations.save_df_to_file(filtered_calendar,
                                   f"calendars/{class_name}/{sub_class}.csv")
                calendar_df = file_operations.read_df_from_file(
                    f"calendars/{class_name}/{sub_class}.csv", silent=False)
                total_traffic_df = data_operations.build_total_traffic_df(
                    calendar_df, total_traffic_df)
            
            bar()
            print("")

    print("All calendars successfully scraped!")
    file_operations.save_df_to_file(
        total_traffic_df, f"results/traffic/{date_from}_to_{date_to}.csv")

    driver.quit()


if __name__ == '__main__':
    main()
