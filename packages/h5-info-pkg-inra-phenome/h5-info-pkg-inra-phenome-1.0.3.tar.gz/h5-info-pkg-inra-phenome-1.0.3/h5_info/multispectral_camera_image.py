class MultispectralCameraImage:
    """Store HDF5 MultispectralCameraImage attributes in a simplified structure"""
    def __init__(self):
        self.name = ""
        self.date = ""
        self.size = 0
        self.data = None
        self.channel = 0

    def to_json(self):
        json_dict = {
            "name": self.name,
            "date": self.date,
            "size": self.size,
            "channel": self.channel
        }
        return json_dict

    def from_json(self, json_dict):
        self.name = json_dict["name"]
        self.date = json_dict["date"]
        self.size = json_dict["size"]
        self.channel = json_dict["channel"]
