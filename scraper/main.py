import calendarRequest
import restaurantScraper
import fileOperations

def main():
    url = 'https://lukkarit.vamk.fi/#/schedule'
    driver = restaurantScraper.create_driver(url)

    restaurantScraper.website_controller(driver, "TT2022-2")
    
    if(restaurantScraper.select_groups(driver) != 0):
        print("Failed to locate any groups quitting...")
        exit()
    
    else:
        php_session_id = restaurantScraper.get_php_session_id(driver)
        schedule = calendarRequest.get_calendar_with_cookie(php_session_id).text

        fileOperations.saveSchedule(schedule, "schedules/test.csv")
        df_schedule = fileOperations.readSchedule("schedules/test.csv")
        print(df_schedule)        
if __name__ == '__main__':
    main()