import pandas as pd
import sys

sys.path.append("scraper/")

import fileOperations as fo
import dataOperations as do

def get_traffic_df(path_to_count_file, all_classes_df):
    try:
        classes_count_df = fo.read_df_from_file(path_to_count_file, True)
        traffic_df = pd.DataFrame(columns=[item for item in classes_count_df["end_date"]])

        current_class = do.get_next_class(all_classes_df)
        for index, (class_info_list, class_name, sub_class) in enumerate(current_class):
            class_df = fo.read_df_from_file(f"calendars/{class_name}/{sub_class}.csv", True)
            for date in traffic_df:
                date_compare_and_insert(traffic_df, class_df, date, index, sub_class)

        traffic_df = traffic_df.fillna(0)
        return traffic_df
        
    except FileNotFoundError:
        print(f"Warning - Cant locate file with path {path_to_count_file}... Unable to create traffic dataframe.")
        return None
    

def date_compare_and_insert(traffic_df, class_df, date_to_compare, index, sub_class):
    for date in class_df["end_date"]:
        if date_to_compare == date:
            traffic_df.loc[index, date] = sub_class   

    
def get_traffic_by_date(traffic_df, date):
    try:
        filtered_df = traffic_df[traffic_df[date] != 0]
        filtered_df = filtered_df[date] 
        filtered_df = filtered_df.reset_index(drop=True)
        return filtered_df
    
    except (KeyError, TypeError):
        print(f"Warning - Cant find any groups with date {date}")
        return None



def get_traffic_distribution(all_classes_df, sub_class):
    try:
        class_name = do.get_class_name_from_subclass(sub_class)
        restaurant_distribution = all_classes_df[class_name[0]][sub_class]["restaurants"]
        return restaurant_distribution
    
    except KeyError:
        print(f"Warning - Unable to get restaurant distribution with class name : {class_name[0]} and sub class : {sub_class}")
        return None
    

def distribute_to_restaurants(amount_of_people, restaurant_distribution):
    distributed_people =  []

    for distibution_multiplier in restaurant_distribution:
        distributed_people.append(round(amount_of_people * distibution_multiplier))
        
    return distributed_people
    

def add_distributions_to_total(total_distribution, class_distribution):
    res = []
    for i in range(len(total_distribution)):
        res.append(total_distribution[i] + class_distribution[i])
    
    return res


def connect_distribution_to_restaurant(total_distribution, restaurants):
    for index, key in enumerate(restaurants):
        restaurants[key] = total_distribution[index]

    return restaurants


def get_restaurant_traffic(all_classes_df, total_traffic_df, total_restaurant_distribution, date):
    traffic_at_date = get_traffic_by_date(total_traffic_df, date)

    if traffic_at_date is not None:
        for sub_class in traffic_at_date:
            traffic_distribution = get_traffic_distribution(all_classes_df, sub_class)
            amount_of_people = do.get_amount_of_people_in_class(all_classes_df, sub_class)
            class_restaurant_distribution = distribute_to_restaurants(amount_of_people, traffic_distribution)
            total_restaurant_distribution = add_distributions_to_total(total_restaurant_distribution, class_restaurant_distribution)
    
    return total_restaurant_distribution


def get_traffic_at_date(all_classes_df, total_traffic_df, total_restaurant_distribution, date, restaurants):
    total_restaurant_distribution = get_restaurant_traffic(all_classes_df, total_traffic_df, total_restaurant_distribution, date)
    restaurants = connect_distribution_to_restaurant(total_restaurant_distribution, restaurants)

    return restaurants


