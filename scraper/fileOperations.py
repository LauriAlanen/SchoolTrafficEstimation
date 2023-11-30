import pandas as pd
import pyarrow.feather as feather
import json
import os
from io import StringIO


def saveSchedule(schedule, path):
    folder_path = os.path.dirname(path)

    try:
        os.makedirs(folder_path)
    
    except FileExistsError:
        print(f"Folder with path {folder_path} already exists")
    
    with open(path, "wb") as f:
        schedule.to_csv(f)


def filterDataFrame(schedule):
    filters = ["start_date", "event_id", "code", "visible", "color", "subject", 
             "description", "reserved_for", "location", "realizations"]

    try:
        df = pd.read_json(StringIO(schedule))

    except ValueError:
        print(f"Unable to convert to dataframe {df}")
        
    for filter_to_try in filters:
        try:
            df.drop(filter_to_try ,axis=1, inplace=True)
        except KeyError:
            print(f"Could not filter with {filter_to_try}")
    
    return df


def readSchedule(path):
    with open(path, "rb") as f:
        print(f"(foldername + filename) {path}")

        read_df = pd.read_csv(f)
        #read_df = feather.read_feather(f)
        return read_df


def getAllClasses(class_file_path):
    with open(class_file_path, "rb") as f:
        classes_json = json.load(f)
        return classes_json


def getOccurance(df):
    df.sort_values(by=['end_date'])
    count = df['end_date'].value_counts()
    return count


def getNextClass():
    classes = getAllClasses("schedules/all_classes.json")

    for class_name, class_list in classes.items():
        for sub_class in class_list:
            yield (class_name, sub_class)