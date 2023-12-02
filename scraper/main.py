import calendarRequest
import websiteScraper
import fileOperations
import dataOperations
from alive_progress import alive_bar

def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'

    total_class_count = dataOperations.get_amount_of_classes(class_file_path)
    
    current_class = dataOperations.get_next_class(class_file_path)

    with alive_bar(total_class_count) as bar:
        for class_name, sub_class in current_class:
            driver = websiteScraper.create_driver(url_to_scrape)
            
            websiteScraper.search_groups(driver, sub_class)
            websiteScraper.select_available_groups(driver, sub_class)
            
            php_session_cookie = websiteScraper.get_php_session_cookie(driver)
            calendar = calendarRequest.get_calendar_cookie(php_session_cookie).text
            filtered_calendar = dataOperations.filter_calendar(calendar)
                
            if(filtered_calendar is not None):
                fileOperations.save_calendar(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
                df_schedule = fileOperations.read_calendar(f"calendars/{class_name}/{sub_class}.csv")
                occurances = dataOperations.get_occurance_count(df_schedule)

            #print(f"\n{occurances}\n")

            bar()
            driver.refresh()
    
    driver.quit()
    print("All class calendars successfully scraped!")
        
if __name__ == '__main__':
    main()