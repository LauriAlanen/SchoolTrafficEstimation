"""This module contains the main functions for fetching the traffic data."""

from scraper import file_operations
from scraper import data_operations
from estimation import traffic_operations

def get_traffic(date_to_check):
    """ Returns the estimated traffic at a given date."""

    restaurants = {
        "Cotton Club": 0,
        "August Restaurant": 0,
        "Cafe Techno": 0,
        "Restaurant W33": 0,
        "Juvenes Mathilda": 0,
        "Juvenes Alma": 0,
        "Juvenes Alere": 0,
        "Juvenes Serveri": 0
    }

    date_from, date_to = file_operations.get_file_dates()

    class_file_path = 'calendars/all_classes.json'
    all_classes_df = data_operations.get_all_classes(class_file_path)
    total_traffic_df = traffic_operations.get_traffic_df(
        f"results/traffic/{date_from}_to_{date_to}.csv", all_classes_df)
   
    if total_traffic_df is not None:
        traffic_at_date = [0, 0, 0, 0, 0, 0, 0, 0]
        traffic_at_date = traffic_operations.get_traffic_at_date(
            all_classes_df, total_traffic_df, traffic_at_date, date_to_check, restaurants)
        return traffic_at_date

    else:
        print("Warning - Unable to get total traffic...")
