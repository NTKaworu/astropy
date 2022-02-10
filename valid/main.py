from pathlib import Path
from typing import Counter
from logzero import logger, logfile
from sense_hat import SenseHat
from picamera import PiCamera
from orbit import ISS
from time import sleep
from datetime import datetime, timedelta
import csv

s = SenseHat()
cam = PiCamera()
data_file = None

def create_csv_file(data_file):
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Counter", "Date/time", "Latitude", "Longitude", "Temperature", "Humidity", "Pressure")
        writer.writerow(header)


def setup():
    global data_file
    base_folder = Path(__file__).parent.resolve()
    logfile(base_folder/"events.log")

    cam.resolution = (1296, 972)

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
    round(s.pressure, 4)
    )
    return data


def write_data(data_file, data):
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


def capture_photo():
    cam.capture()


def main():
    setup()

    counter = 1
    now = datetime.now()
    start = datetime.now()
    while (now < start + timedelta(minutes=175)):
        try:
            write_data(data_file, get_datas(counter))
            capture_photo()
        except:
            print("ciao")


if __name__ == '__main__':
    main()