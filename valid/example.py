from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
from picamera import PiCamera
from orbit import ISS
from time import sleep
from datetime import datetime, timedelta
import csv
s = SenseHat()
s.set_imu_config(False, True, True) 
accel_raw = s.get_accelerometer_raw()
gyro_raw = s.get_gyroscope_raw()
cam = PiCamera()
data_file = None
base_folder = None
counter = 1


def create_csv_file(data_file):
    with open(data_file, 'w') as g:
        writer = csv.writer(g)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure", "Acceleration", "Gyroscope ")
        writer.writerow(header)


def setup():
    global data_file
    global base_folder
    base_folder = Path(__file__).parent.resolve()
    logfile(base_folder/"events.log")

    cam.resolution = (2599, 1944)

    data_file = base_folder/"data.csv"
    create_csv_file(data_file)


def get_datas(counter):
    location = ISS.coordinates()
    data = (
    counter,
    datetime.now(),
    location.latitude.degrees,
    location.longitude.degrees,
    round(s.humidity, 4),
    round(s.temperature, 4),
    round(s.pressure, 4),
    round(s. accelerometer_accel_raw, 4),
    round(s. gyroscope_gyro_raw, 4),
    )
    return data


def write_data(data_file, data):
    with open(data_file, 'a') as g:
        writer = csv.writer(g)
        writer.writerow(data)


def convert(angle):
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle


def capture_photo():
    location = ISS.coordinates()

    # Convert the latitude and longitude to EXIF-appropriate representations
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    # Set the EXIF tags specifying the current location
    cam.exif_tags['GPS.GPSLatitude'] = exif_latitude
    cam.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    cam.exif_tags['GPS.GPSLongitude'] = exif_longitude
    cam.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    cam.capture(f"{base_folder}/photo_{counter:03d}.jpg")


def main():
    global counter

    setup()

    now = datetime.now()
    start = datetime.now()
    while (now < start + timedelta(minutes=60)):
        try:
            write_data(data_file, get_datas(counter))
            capture_photo()
            logger.info(f"iteration {counter}")
            counter += 1
            sleep(10)
            now = datetime.now()
        except Exeption as es:
            logger.error(f'{e.__class__.__name__}: {e}')


if __name__ == '__main__':
    main()