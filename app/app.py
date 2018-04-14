import pandas as pd

vehicle_states = pd.read_csv("../resources/vehicle_states.csv", sep=';')
print(vehicle_states.describe())
