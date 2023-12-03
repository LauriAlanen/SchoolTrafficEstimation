import fileOperations
import pandas as pd
from prophet import Prophet
from prophet.plot import plt

def plot_occurrences(total_occurrences_df):
    total_occurrences_df['end_date'] = pd.to_datetime(total_occurrences_df['end_date'])
    total_occurrences_df = total_occurrences_df.sort_values(by='end_date')
    plt.figure(figsize=(10, 6))
    plt.plot(total_occurrences_df['end_date'], total_occurrences_df['count'], marker='o', linestyle='-')
    plt.xlabel('End Date')
    plt.ylabel('Count')
    plt.title('Count over Time')
    plt.show()

def use_prophet(path_to_total_occurrences):
    total_occurrences_df = fileOperations.read_df_from_file(path_to_total_occurrences)
    total_occurrences_df = total_occurrences_df.reset_index()
    total_occurrences_df['ds'] = pd.to_datetime(total_occurrences_df['end_date'])
    total_occurrences_df['y'] = total_occurrences_df['count']
    total_occurrences_df = total_occurrences_df[['ds', 'y']]
    
    model = Prophet()
    model.fit(total_occurrences_df)
    
    future = model.make_future_dataframe(periods=7)
    forecast = model.predict(future)

    fig1 = model.plot(forecast)
    fig2 = model.plot_components(forecast)
    plt.show()


def distribute_to_restaurants(amount_of_people, restaurant_distribution):
    distributed_people = list()
    for distibution_multiplier in restaurant_distribution:
        distributed_people.append(round(amount_of_people * distibution_multiplier))

    print(distributed_people)
    return distributed_people

    