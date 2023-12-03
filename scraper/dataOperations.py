import pandas as pd
import json
import websiteScraper
import calendarRequest
import websiteScraper
import fileOperations

def get_all_classes(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def get_occurrence_count(calendar_df):
    sorted_df = calendar_df.sort_values(by=['end_date'])
    count = sorted_df['end_date'].value_counts()
    count_df = count.to_frame().reset_index()
    count_df = count_df.fillna(0)

    return count_df


def build_total_occurrences(calendar_df, total_occurrences_df):
    current_occurrences_df = get_occurrence_count(calendar_df)

    if total_occurrences_df.empty:
        return current_occurrences_df

    else:
        total_occurrences_df = pd.concat([total_occurrences_df, current_occurrences_df]).groupby(['end_date']).sum().reset_index()
        return total_occurrences_df


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
                print(f"Could not filter with {filter_to_try}")

    return calendar_df
        

def get_next_class(class_file_path):
    classes = get_all_classes(class_file_path)

    for class_name, class_list in classes.items():
        for sub_class in class_list:
            yield (class_list, class_name, sub_class)


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


def get_traffic_df(path_to_count_file, path_to_all_classes_file):
    try:
        classes_count_df = fileOperations.read_df_from_file(path_to_count_file)
        classes_df = pd.DataFrame(columns=[item for item in classes_count_df["end_date"]])

        current_class = get_next_class(path_to_all_classes_file)
        for index, (class_list, class_name, sub_class) in enumerate(current_class):
            class_df = fileOperations.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv")
            for date in classes_df:
                date_compare(classes_df, class_df, date, index, sub_class)

        classes_df = classes_df.fillna(0)
        return classes_df
        
    except FileNotFoundError:
        print(f"Cant locate file with path {path_to_count_file}... Unable to create traffic dataframe.")
        return None
    

def date_compare(classes_df, class_df, date_to_compare, index, sub_class):
    for date_to_check in class_df["end_date"]:
        if date_to_compare == date_to_check:
            classes_df.loc[index, date_to_compare] = sub_class    


def get_traffic_by_date(classes_df, date):
    try:
        filtered_df = classes_df[classes_df[date] != 0]
        filtered_df = filtered_df[date] 
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df
    
    except (KeyError, TypeError):
        print(f"Cant find any groups with date {date}")
        return None

traffic_df = get_traffic_df("results/predictions/2023-12-08_to_2023-12-15.csv", "calendars/all_classes.json") 
print(get_traffic_by_date(traffic_df, "2023-12-08 16:15"))