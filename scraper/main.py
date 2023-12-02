import fileOperations
import dataOperations
import websiteScraper
import matplotlib.pyplot as plt

import pandas as pd
from alive_progress import alive_bar

def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'
    date_from = "2023-12-02" # YYYY-MM-DD
    date_to = "2023-12-09" # YYYY-MM-DD
    
    total_class_count = dataOperations.get_amount_of_classes(class_file_path)
    current_class = dataOperations.get_next_class(class_file_path)
    total_occurrences_df = pd.DataFrame(columns=['end_date'])

    with alive_bar(total_class_count) as bar:
        for class_name, sub_class in current_class:
            driver = websiteScraper.create_driver(url_to_scrape)
            filtered_calendar = dataOperations.gather_and_filter_calendar_information(driver, sub_class, date_from, date_to)
            
            if(filtered_calendar is not None):
                fileOperations.save_df_to_file(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
                df_schedule = fileOperations.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv")
                total_occurrences_df = dataOperations.build_total_occurrences(df_schedule, total_occurrences_df)

            print("")
            bar()
            driver.refresh()
    
    fileOperations.save_df_to_file(total_occurrences_df, f"results/busy_times/{date_from}_to_{date_to}.csv")
    print("All calendars successfully scraped!")
    driver.quit()
        
if __name__ == '__main__':
    main()