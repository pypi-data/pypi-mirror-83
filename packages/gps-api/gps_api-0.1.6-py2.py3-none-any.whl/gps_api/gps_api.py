"""Main module."""
import serial
import serial.tools.list_ports
from haversine import haversine
from . import position

class GPS:
    def __init__(self, port):
        self.port = port
        # list com ports
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # if port in listed com ports
            if self.port in p:
                # connect serial port
                self.ser = serial.Serial(port, baudrate=9600, timeout=0.5)
            else: raise Exception('Invalid port')
        # change NMEA message type and frequency:
        # set GLL, RMC, VTG and GGA output frequency to be outputting once every position fix
        self.ser.write(b'\$PMTK314,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n')
        # initialisation of variables
        self.nmea_msg = ""
        self.position = position.Position()
        self.distance = 0
        self.another_location = None

    def reboot(self):
        '''
        reboot involves a full cold start
        FULL COLD START: time, position, almanacs and ephemeris data will be redownloaded
                         system/user configurations will be cleared
                         process will take approximately 8 minutes, use with patience
        instantiate GPS class after reboot to apply the configuration of NMEA message type and frequency
        '''
        self.ser.write("\$PMTK104*37\r\n")

    def clean_string(self):
        '''
        clear data held in nmea_msg
        '''
        self.nmea_msg = ""

    def get_latitude(self):
        '''
        return latitude data from latest nmea message
        '''
        self.clean_string()
        while "GPGGA" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_latitude()

    def get_longitude(self):
        '''
        return longitude data from latest nmea message
        '''
        self.clean_string()
        while "GPGGA" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_longitude()

    def get_altitude(self):
        '''
        return altitude data from latest nmea message
        '''
        self.clean_string()
        while "GPGGA" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_altitude()

    def get_current_location(self):
        '''
        return current location data from latest nmea message
        (latitude, longitude)
        '''
        self.clean_string()
        while "GPGGA" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_current_location()

    def get_UTC_time(self):
        '''
        return UTC time of current location from latest nmea message
        '''
        self.clean_string()
        while "GPRMC" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_UTC_time()

    def get_date(self):
        '''
        return date of current location from latest nmea message
        '''
        self.clean_string()
        while "GPRMC" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_date()

    def set_another_location(self, latitude, longitude):
        '''
        set the distination variable
        (latitude, longitude)
        '''
        self.another_location = (latitude, longitude)

    def get_distance(self, latitude, longitude):
        '''
        return distance between current location and given latitude and longitude as starting point
        '''
        self.set_another_location(latitude, longitude)
        distance = haversine(self.get_current_location(), self.another_location)
        return distance

    def get_speed(self):
        '''
        return current speed over ground in km/h
        '''
        self.clean_string()
        while "GPVTG" not in self.nmea_msg:
            self.nmea_msg = self.ser.readline().decode("utf-8", "ignore")
        self.position.update(self.nmea_msg)
        return self.position.get_speed()

    def get_time_of_arrival(self, latitude, longitude):
        '''
        calculates travel_time in hours
        '''
        speed = self.get_speed()
        if speed == 0.0:
            message = "You are stationary, time of arrival unknown"
            return message
        else:
            time = float(self.get_distance(latitude,longitude))/float(speed)*3600
            day = time // (24 * 3600)
            time = time % (24 * 3600)
            hour = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time

            # gettings arrival time and splitting into hours, minutes and seconds
            current_time = str(self.get_UTC_time())
            c_hour = int(current_time[0,2])
            c_minutes =  int(current_time[2,4])
            c_seconds = int(current_time[4,6])

            # calculating arival times
            a_hours = c_hour+hour
            a_minutes = c_minutes+minutes
            a_seconds = c_seconds+seconds

            arrival_time = ("%d:%d:%d" % (a_hours, a_minutes, a_seconds))
            return arrival_time
