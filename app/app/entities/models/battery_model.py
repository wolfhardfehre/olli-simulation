class BatteryModel:
    def __init__(self, start_percent=100.0, drain_per_meter=0.014):
        self.drain_per_meter = drain_per_meter
        self.status = start_percent

    def update(self, meters):
        self.status -= meters * self.drain_per_meter

    def low_battery(self):
        return self.status < 20.0
