from pathlib import Path
from logzero import logger, logfile
from sense_hat import SenseHat
from picamera import PiCamera
from orbit import ISS
from time import sleep
from datetime import datetime, timedelta
import csv

s = SenseHat()
cam = PiCamera()
location = ISS.coordinates()

base_folder = Path(__file__).parent.resolve()
data_file = base_folder/"data.csv"

sleep_duration = 30 # Seconds - Iterval between each iteration
time_frame = 175 # Minutes - Total time frame of data gathering


def create_csv_file():
    """
    Create data file
    """
    with open(data_file, 'w') as g:
        writer = csv.writer(g)
        header = (
            "Counter", "Date/time",
            "Latitude", "Longitude",
            "Temperature", "Humidity", "Pressure",
            "Accel Pitch", "Accel Roll", "Accel Yaw",
            "Accel X", "Accel Y", "Accel Z",
            "Gyro Pitch", "Gyro Roll", "Gyro Yaw",
            "Gyro X", "Gyro Y", "Gyro Z"
            )
        writer.writerow(header)


def setup():
    """
    Application setup:
    - create data file;
    - create log file;
    - setup camera resolution.
    """
    create_csv_file()
    logfile(base_folder/"events.log")
    cam.resolution = (1296, 972)


def get_data(counter):
    """
    Collect all sensors data:
    - ISS location;
    - humidity;
    - temperature;
    - pressure;
    - accelerometer;
    - gyroscope.

    :type counter: int
    :rtype: tuple
    """
    accel = s.accelerometer
    accel_raw = s.accelerometer_raw 
    gyro = s.gyroscope
    gyro_raw = s.gyroscope_raw

    data = (
        counter,
        datetime.now(),
        location.latitude.degrees,
        location.longitude.degrees,
        round(s.humidity, 4),
        round(s.temperature, 4),
        round(s.pressure, 4),
        accel["pitch"],
        accel["roll"],
        accel["yaw"],
        accel_raw["x"],
        accel_raw["y"],
        accel_raw["z"],
        gyro["pitch"],
        gyro["roll"],
        gyro["yaw"],
        gyro_raw["x"],
        gyro_raw["y"],
        gyro_raw["z"]
    )
    return data


def write_data(data):
    """
    Write collected sensors data to csv file

    :type data: tuple
    """
    with open(data_file, 'a') as g:
        writer = csv.writer(g)
        writer.writerow(data)


def convert(angle):
    """
    Utility to convert angle in to exif_angle notation

    :type angle: float
    :rtype: tuple
    """
    sign, degrees, minutes, seconds = angle.signed_dms()
    exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
    return sign < 0, exif_angle


def capture_photo(counter):
    """
    Get picture and tag it with additional exif data

    :type counter: int
    """
    south, exif_latitude = convert(location.latitude)
    west, exif_longitude = convert(location.longitude)

    cam.exif_tags['GPS.GPSLatitude'] = exif_latitude
    cam.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
    cam.exif_tags['GPS.GPSLongitude'] = exif_longitude
    cam.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

    cam.capture(f"{base_folder}/photo_{counter:03d}.jpg")


def main():
    setup()

    now = datetime.now()
    start = datetime.now()

    # Main loop
    while now < start + timedelta(minutes=time_frame):
        try:
            write_data(data_file, get_data(counter))
            capture_photo(counter)
            logger.info(f"iteration {counter}")
            counter += 1
            sleep(sleep_duration)
            now = datetime.now()
        except Exception as e:
            logger.error(f'{e.__class__.__name__}: {e}')


# Everything starts here
if __name__ == '__main__':
    main()
