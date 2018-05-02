class Booking:
    # unix times, graph ids
    def __init__(self, start_station, end_station, earliest_departure, latest_arrival):
        self.start_station = start_station
        self.end_station = end_station
        self.earliest_departure = earliest_departure
        self.latest_arrival = latest_arrival