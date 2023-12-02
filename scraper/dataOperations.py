from io import StringIO
import pandas as pd
import json

def getAllClasses(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)

        return classes_json


def getOccuranceCount(df):
    df.sort_values(by=['end_date'])
    count = df['end_date'].value_counts()

    return count


def filterCalendar(schedule):
    filters = ["start_date", "event_id", "code", "visible", "color", "subject", 
             "description", "reserved_for", "location", "realizations"]

    try:
        df = pd.read_json(StringIO(schedule))
        for filter_to_try in filters:
            try:
                df.drop(filter_to_try ,axis=1, inplace=True)
            except KeyError:
                print(f"Could not filter with {filter_to_try}")

        return df
        
    except ValueError:
        print(f"Unable to convert schedule to dataframe")
        return None
        
    

def getNextClass(class_file_path):
    classes = getAllClasses(class_file_path)

    for class_name, class_list in classes.items():
        for sub_class in class_list:
            yield (class_name, sub_class)

def getAmountOfClasses(class_file_path):
    all_classes = getAllClasses(class_file_path)
    total_classes = sum(len(class_list) for class_list in all_classes.values())
    
    return total_classes