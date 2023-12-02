from io import StringIO
import pandas as pd
import json
import websiteScraper
import calendarRequest
import websiteScraper


def get_all_classes(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def get_occurrence_count(calendar_df):
    sorted_df = calendar_df.sort_values(by=['end_date'])
    count = sorted_df['end_date'].value_counts()
    count_df = count.to_frame()

    return count_df.reset_index()


def build_total_occurrences(calendar_df, total_occurrences_df):
    current_occurrences_df = get_occurrence_count(calendar_df)
    print(total_occurrences_df)

    if total_occurrences_df.empty:
        return current_occurrences_df

    else:
        total_occurrences_df = pd.concat([total_occurrences_df, current_occurrences_df]).groupby(['end_date']).sum().reset_index()
        return total_occurrences_df


def json_to_df(calendar):
    try:
        calendar_df = pd.read_json(StringIO(calendar))
        #print(f"\n{df}\n")

    except ValueError:
        print(f"Unable to convert schedule to dataframe")
        return None
    
    return calendar_df


def filter_calendar(calendar):
    filters = ["start_date", "event_id", "code", "visible", "color", "subject", 
             "description", "reserved_for", "location", "realizations"]
    
    calendar_df = json_to_df(calendar)
    #print(f"\n{df}\n")

    if calendar_df is not None:
        for filter_to_try in filters:
            try:
                calendar_df.drop(filter_to_try ,axis=1, inplace=True)

            except KeyError:
                print(f"Could not filter with {filter_to_try}")

    return calendar_df
        

def get_next_class(class_file_path):
    classes = get_all_classes(class_file_path)

    for class_name, class_list in classes.items():
        for sub_class in class_list:
            yield (class_name, sub_class)


def get_amount_of_classes(class_file_path):
    all_classes = get_all_classes(class_file_path)
    total_classes = sum(len(class_list) for class_list in all_classes.values())
    
    return total_classes


def gather_and_filter_calendar_information(driver, sub_class, date_from, date_to):
    print(f"Gathering {sub_class} information")
    
    websiteScraper.search_groups(driver, sub_class)
    websiteScraper.select_available_groups(driver, sub_class)
    
    php_session_cookie = websiteScraper.get_php_session_cookie(driver)
    calendar = calendarRequest.get_calendar_cookie(php_session_cookie, date_from, date_to)
    filtered_calendar = filter_calendar(calendar.text)
    
    # Return or do something with the filtered_calendar if needed
    return filtered_calendar
