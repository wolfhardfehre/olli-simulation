import pandas as pd

vehicle_states = pd.read_csv("./resources/vehicle_states.csv", sep=';',
                             parse_dates=['last_seen','created_at'], index_col='last_seen')
vehicle_states.sort_index(inplace=True)
print(vehicle_states.describe())
