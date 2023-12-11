import pandas as pd
import pyarrow.feather as feather
import os
import json
from io import StringIO
from datetime import datetime, timedelta

def save_df_to_file(df_to_save, path):
    folder_path = os.path.dirname(path)
    create_folder_path(folder_path)

    with open(path, "wb") as f:
        df_to_save.to_csv(f)
        print("Notification - Succesfully saved schedule!")


def read_df_from_file(path, silent):
    with open(path, "rb") as f:
        if not silent : print(f"Notification - Reading schedule {path}")

        df_to_read = pd.read_csv(f)
        #read_df = feather.read_feather(f)
        df_to_read = df_to_read.drop(df_to_read.columns[0], axis=1)

        return df_to_read


def create_folder_path(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"Notification - Created folder with path {folder_path}")

    except FileExistsError:
        print(f"Notification - Folder with path {folder_path} already exists")

def json_to_df(calendar):
    try:
        calendar_df = pd.read_json(StringIO(calendar))
        #print(f"\n{df}\n")

    except ValueError:
        print(f"Warning - Unable to convert schedule to dataframe")
        return None
    
    return calendar_df

def save_dict_as_json(path, dictionary_to_save):
    folder_path = os.path.dirname(path)
    create_folder_path(folder_path)

    json_obj = json.dumps(dictionary_to_save, indent=4)
    with open(path, "wb") as f:
        f.write(json_obj)
        print("Notification - Succesfully saved dictionary!")

def get_file_dates():
    date = datetime.now().date()
    date_from = date - timedelta(days=(date.weekday() - 0) % 7)
    date_to = date + timedelta(days=(6 - date.weekday()) % 7)

    return date_from, date_to