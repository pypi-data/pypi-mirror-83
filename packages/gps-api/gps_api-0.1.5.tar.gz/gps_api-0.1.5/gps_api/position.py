import pynmea2

class Position:
    """ position class, used to store latitude, longitude and altitude.
        get_latitude, get_longitude and get_current_location methods
    """

    def __init__(self):
        # initialisation of variables
        self.latitude = ""
        self.longitude = ""
        self.altitude = ""
        self.location = ""
        self.time = ""
        self.date = ""
        self.speed = ""

    def update(self, nmea_msg):
        if "GPGGA" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.latitude = msg.latitude
            self.longitude = msg.longitude
            self.altitude = msg.altitude
        elif "GPRMC" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.time = msg.timestamp
            self.date = msg.datestamp
        elif "GPVTG" in nmea_msg:
            msg = pynmea2.parse(nmea_msg)
            self.speed = msg.spd_over_grnd_kmph

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_altitude(self):
        return self.altitude

    def get_current_location(self):
        location = (self.latitude, self.longitude)
        return location

    def get_UTC_time(self):
        return self.time

    def get_date(self):
        return self.date

    def get_speed(self):
        return self.speed
