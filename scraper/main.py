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
        response = calendarRequest.get_calendar_with_cookie(php_session_id)
        fileOperations.saveSchedule(response.text, "schedules/test.csv")
        print(fileOperations.readSchedule("schedules/test.csv"))
        
if __name__ == '__main__':
    main()