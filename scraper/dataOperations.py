from io import StringIO
import pandas as pd
import json

def get_all_classes(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def get_occurance_count(df):
    df.sort_values(by=['end_date'])
    count = df['end_date'].value_counts()

    return count


def json_to_df(schedule):
    try:
        df = pd.read_json(StringIO(schedule))
        #print(f"\n{df}\n")

    except ValueError:
        print(f"Unable to convert schedule to dataframe")
        return None
    
    return df


def filter_calendar(schedule):
    filters = ["start_date", "event_id", "code", "visible", "color", "subject", 
             "description", "reserved_for", "location", "realizations"]
    
    df = json_to_df(schedule)
    #print(f"\n{df}\n")

    if df is not None:
        for filter_to_try in filters:
            try:
                df.drop(filter_to_try ,axis=1, inplace=True)

            except KeyError:
                print(f"Could not filter with {filter_to_try}")

    return df
        

def get_next_class(class_file_path):
    classes = get_all_classes(class_file_path)

    for class_name, class_list in classes.items():
        for sub_class in class_list:
            yield (class_name, sub_class)


def get_amount_of_classes(class_file_path):
    all_classes = get_all_classes(class_file_path)
    total_classes = sum(len(class_list) for class_list in all_classes.values())
    
    return total_classes