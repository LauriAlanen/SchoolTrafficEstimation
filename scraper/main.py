import calendarRequest
import websiteScraper
import fileOperations
import dataOperations
from alive_progress import alive_bar

def main():
    url_to_scrape = 'https://lukkarit.vamk.fi/#/schedule'
    class_file_path = 'calendars/all_classes.json'

    total_class_count = dataOperations.getAmountOfClasses(class_file_path)
    
    current_class = dataOperations.getNextClass(class_file_path)

    with alive_bar(total_class_count) as bar:
        for class_name, sub_class in current_class:
            driver = websiteScraper.create_driver(url_to_scrape)
            websiteScraper.search_groups(driver, sub_class)
            
            if(websiteScraper.select_available_groups(driver) == 1):
                print("Failed to locate any groups quitting...")
                exit()
            
            else:
                php_session_cookie = websiteScraper.get_php_session_cookie(driver)
                calendar = calendarRequest.get_calendar_with_cookie(php_session_cookie).text
                filtered_calendar = dataOperations.filterCalendar(calendar)
                
                if(filtered_calendar is not None):
                    fileOperations.saveSchedule(filtered_calendar, f"calendars/{class_name}/{sub_class}.csv")
                    df_schedule = fileOperations.readSchedule(f"calendars/{class_name}/{sub_class}.csv")
                    occurances = dataOperations.getOccuranceCount(df_schedule)

                print(f"\n{occurances}\n")

            bar()
            driver.refresh()
    
    driver.quit()
    print("All class calendars successfully scraped!")
        
if __name__ == '__main__':
    main()