import calendarRequest
import restaurantScraper
import fileOperations

def main():
    url = 'https://lukkarit.vamk.fi/#/schedule'

    for class_name, sub_class in fileOperations.getNextClass():
        driver = restaurantScraper.create_driver(url)

        restaurantScraper.website_controller(driver, sub_class)
        
        if(restaurantScraper.select_groups(driver) != 0):
            print("Failed to locate any groups quitting...")
            exit()
        
        else:
            php_session_id = restaurantScraper.get_php_session_id(driver)
            schedule = calendarRequest.get_calendar_with_cookie(php_session_id).text
            filtered_schedule = fileOperations.filterDataFrame(schedule)

            fileOperations.saveSchedule(filtered_schedule, f"schedules/{class_name}/{sub_class}.csv")
            df_schedule = fileOperations.readSchedule(f"schedules/{class_name}/{sub_class}.csv")
            occurances = fileOperations.getOccurance(df_schedule)
            print(occurances)
        
        driver.quit()
        
if __name__ == '__main__':
    main()