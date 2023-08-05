class Geo:
    """Store HDF5 Geolocalisation attributes in a simplified structure"""
    def __init__(self):
        self.date = 0
        self.longitude = 0.0
        self.latitude = 0.0
        self.uncertainty = 0.0
        self.tray_height = 0.0
        self.heading = 0.0
        self.course = 0.0
        self.roll = 0.0
        self.pitch = 0.0
        self.sog = 0.0
