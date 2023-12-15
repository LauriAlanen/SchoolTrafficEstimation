""" This module contains functions for handling and modifying the calendar data."""

import re
import json
import pandas as pd

from scraper import fetch_calendar
from scraper import file_operations
from scraper import website_controller


def get_all_classes(class_file_path):
    """ Returns a dictionary which contains all the classes. Data is read from a json file."""
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def get_date_counts(calendar_df):
    """ Returns a dataframe containing the amount of occurrences for each date."""
    sorted_df = calendar_df.sort_values(by=['end_date'])
    count = sorted_df['end_date'].value_counts()
    count_df = count.to_frame().reset_index()
    count_df = count_df.fillna(0)

    return count_df


def filter_calendar(calendar):
    """ Filters the json calendar data and returns a filter calendar dataframe."""
    filters = ["start_date", "event_id", "code", "visible", "color", "subject",
               "description", "reserved_for", "location", "realizations"]

    calendar_df = file_operations.json_to_df(calendar)
    if calendar_df is not None:
        for filter_to_try in filters:
            try:
                calendar_df.drop(filter_to_try, axis=1, inplace=True)

            except KeyError:
                print(f"Warning - Could not filter with {filter_to_try}")

    return calendar_df


def get_next_class(all_classes_df):
    """ Generator for iterating through all the classes"""
    for (class_name, class_list) in all_classes_df.items():
        for sub_class in class_list:
            yield (class_list, class_name, sub_class)


def get_amount_of_classes(all_classes_df):
    """ Returns the amount of classes in the all_classes_df"""
    total_classes = sum(len(class_list)
                        for class_list in all_classes_df.values())

    return total_classes


def get_calendar(driver, sub_class, date_from, date_to):
    """ Main function for getting the calendar data. Returns a filtered calendar dataframe."""    
    print(f"Notification - Gathering {sub_class} information")

    website_controller.search_groups(driver, sub_class)
    website_controller.select_available_groups(driver, sub_class)

    php_session_cookie = website_controller.get_php_session_cookie(driver)
    calendar = fetch_calendar.get_calendar_cookie(
        php_session_cookie, date_from, date_to)
    filtered_calendar = filter_calendar(calendar.text)

    return filtered_calendar


def build_total_traffic_df(calendar_df, total_traffic_df):
    """ Builds a dataframe containing the total traffic at a all available dates."""
    current_calendar_counts = get_date_counts(calendar_df)

    if total_traffic_df.empty:
        return current_calendar_counts

    total_traffic_df = pd.concat([total_traffic_df, current_calendar_counts]).groupby(
        ['end_date']).sum().reset_index()
    return total_traffic_df


def get_amount_of_people_in_class(all_classes_df, sub_class):
    try:
        class_name = get_class_name_from_subclass(sub_class)
        amount_of_people = all_classes_df[class_name[0]][sub_class]["people"]
        return amount_of_people

    except KeyError:
        print(f"Warning - Unable to get amount of people with class name : {class_name[0]} and sub class : {sub_class}")
        return None


def build_dates_df(total_traffic_df):
    """ Returns a dataframe containing all the which have traffic."""
    dates_df = total_traffic_df.drop(['count'], axis=1)
    return dates_df


def get_class_name_from_subclass(sub_class):
    return re.split(r'(\d+)', sub_class)
