import calendarRequest
import restaurantScraper

def main():
    url = 'https://lukkarit.vamk.fi/#/schedule'

    driver = restaurantScraper.create_driver(url)
    restaurantScraper.website_controller(driver, "TT2022-2C")
    restaurantScraper.select_groups(driver)

    php_session_id = restaurantScraper.get_php_session_id(driver)

    response = calendarRequest.get_calendar_with_cookie(php_session_id)
    print(response.text)

if __name__ == '__main__':
    main()