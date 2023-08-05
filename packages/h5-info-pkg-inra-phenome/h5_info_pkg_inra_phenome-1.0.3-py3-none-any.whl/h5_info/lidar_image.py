class LidarImage:
    """Store HDF5 CameraImage attributes in a simplified structure"""

    def __init__(self):
        self.name = ""
        self.date = ""
        self.frequency = 0.0
        self.angle_increment = 0.0
        self.scans = {}

    def to_json(self):
        json_dict = {
            "name": self.name,
            "date": self.date,
            "frequency": self.frequency,
            "angle_increment": self.angle_increment
        }
        return json_dict

    def from_json(self, json_dict):
        self.name = json_dict["name"]
        self.date = json_dict["date"]
        self.frequency = json_dict["frequency"]
        self.angle_increment = json_dict["angle_increment"]
