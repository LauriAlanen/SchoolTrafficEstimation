import pandas as pd
import re
import json
import websiteOperations
import calendarRequest
import fileOperations

def get_all_classes(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def get_date_counts(calendar_df):
    sorted_df = calendar_df.sort_values(by=['end_date'])
    count = sorted_df['end_date'].value_counts()
    count_df = count.to_frame().reset_index()
    count_df = count_df.fillna(0)

    return count_df


def filter_calendar(calendar):
    filters = ["start_date", "event_id", "code", "visible", "color", "subject", 
            "description", "reserved_for", "location", "realizations"]
    
    calendar_df = fileOperations.json_to_df(calendar)
    #print(f"\n{df}\n")
    if calendar_df is not None:
        for filter_to_try in filters:
            try:
                calendar_df.drop(filter_to_try ,axis=1, inplace=True)

            except KeyError:
                print(f"Warning - Could not filter with {filter_to_try}")

    return calendar_df
        

def get_next_class(all_classes_df):
    for (class_name, class_list) in all_classes_df.items():
        for sub_class in class_list:
            yield (class_list, class_name, sub_class)


def get_amount_of_classes(all_classes_df):
    total_classes = sum(len(class_list) for class_list in all_classes_df.values())
    
    return total_classes


def gather_and_filter_calendar_information(driver, sub_class, date_from, date_to):
    print(f"Notification - Gathering {sub_class} information")
    
    websiteOperations.search_groups(driver, sub_class)
    websiteOperations.select_available_groups(driver, sub_class)
    
    php_session_cookie = websiteOperations.get_php_session_cookie(driver)
    calendar = calendarRequest.get_calendar_cookie(php_session_cookie, date_from, date_to)
    filtered_calendar = filter_calendar(calendar.text)
    # Return or do something with the filtered_calendar if needed

    return filtered_calendar


def build_total_traffic_df(calendar_df, total_traffic_df):
    current_occurrences_df = get_date_counts(calendar_df)

    if total_traffic_df.empty:
        return current_occurrences_df

    else:
        total_traffic_df = pd.concat([total_traffic_df, current_occurrences_df]).groupby(['end_date']).sum().reset_index()
        return total_traffic_df


def get_amount_of_people_in_class(all_classes_df, sub_class):
    try:
        class_name = get_class_name_from_subclass(sub_class)
        amount_of_people = all_classes_df[class_name[0]][sub_class]["people"]
        return amount_of_people
    
    except KeyError:
        print(f"Warning - Unable to get amount of people with class name : {class_name[0]} and sub class : {sub_class}")
        return None
    
def get_class_name_from_subclass(sub_class):
    return re.split(r'(\d+)',sub_class)