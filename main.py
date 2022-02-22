import configparser, time, datetime, os, sys

sensorsNames = []
sensorsValues = []
path = 'output/images'

def takePicture(i, c, now):    
    c.capture(f'{path}/{i}-{now}.jpg')


def takeValues(config, s , now):
    global sensorsValues
    sensorsValues = []
    if config['Sensori']['umidita'] == "True":
        humidity = s.get_humidity()
        sensorsValues.append(humidity)
    if config['Sensori']['temperatura'] == "True":
        temperature = s.get_temperature()
        sensorsValues.append(temperature)
    if config['Sensori']['pressione'] == "True":
        pressure = s.get_pressure()
        sensorsValues.append(pressure)
    if config['Sensori']['orientamento'] == "True":
        orientation =s.get_orientation()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**orientation))
    if config['Sensori']['giroscopio'] == "True":
        gyro_only = s.get_gyroscope()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**gyro_only))
    if config['Sensori']['giroscopio_raw'] == "True":
        gyro_raw = s.get_gyroscope_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**gyro_raw))
    if config['Sensori']['bussola'] == "True":
        compass_only = s.get_compass()
        sensorsValues.append(compass_only)
    if config['Sensori']['bussola_raw'] == "True":
        compass_raw = s.get_compass_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**compass_raw))
    if config['Sensori']['accelerometro'] == "True":
        accel_only = s.get_accelerometer()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**accel_only))
    if config['Sensori']['accelerometro_raw'] == "True":
        accel_raw = s.get_accelerometer_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**accel_raw))
    
    sensorsValues.append(now)

#    if config['Generali']['gelolocalizzazione'] == "True":
#        sensorsValues.append(orbit.ISS.coordinates())


def saveValues(t, outSheet):
    for i in range(len(sensorsValues)):
        outSheet.write(1+t, i, sensorsValues[i])


def unpackTuples(i):
    new = i.split(", ")
    k = []
    for e in new:
        k.append(int(e))
    return tuple(k)



def main():
    global path
    global sensorsNames
    file = "config.ini"
    config = configparser.ConfigParser()
    config.read(file)

    counter = 0

    while os.path.exists(path):   
        counter += 1
        path = 'output'+(str(counter)) +'/images'

    os.makedirs(path)

    c = picamera.PiCamera()
    s = sense_hat.SenseHat()
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")


    c.resolution = unpackTuples(config['Fotocamera']['risoluzione'])
    c.brightness = int(config['Fotocamera']['luminosita'])
    c.image_effect = config['Fotocamera']['effetto']
    c.exposure_mode = config['Fotocamera']['esposizione']
    c.awb_mode = config['Fotocamera']['bilanciamento_bianchi']

    cicliNum = int(config['Generali']['numero_di_cicli'])
    inter = int(config['Generali']['intervallo_tra_cicli'])


    if config['Generali']['sensori'] == "True":
        outWorkbook = xlsxwriter.Workbook('output'+(str(counter)) +'/out.xlsx')
        outSheet = outWorkbook.add_worksheet()

        if config['Sensori']['umidita'] == "True":
            sensorsNames.append("Umidita")

        if config['Sensori']['temperatura'] == "True":
            sensorsNames.append("Temperatura")

        if config['Sensori']['pressione'] == "True":
            sensorsNames.append("Pressione")

        if config['Sensori']['orientamento'] == "True":
            sensorsNames.append("Orientamento")

        if config['Sensori']['giroscopio'] == "True":
            sensorsNames.append("Giroscopio")

        if config['Sensori']['giroscopio_raw'] == "True":
            sensorsNames.append("Giroscopio-raw")

        if config['Sensori']['bussola'] == "True":
            sensorsNames.append("Bussola")

        if config['Sensori']['bussola_raw'] == "True":
            sensorsNames.append("Bussola-raw")

        if config['Sensori']['accelerometro'] == "True":
            sensorsNames.append("Accelerometro")

        if config['Sensori']['accelerometro_raw'] == "True":
            sensorsNames.append("Accelerometro-raw")

        sensorsNames.append("Date and time")

        if config['Generali']['gelolocalizzazione'] == "True":
            sensorsNames.append("ISS position")
        
#        for i in range(len(sensorsNames)):
#            outSheet.write(0, i, sensorsNames[i])


    for i in range(cicliNum):
        if config['Generali']['fotocamera'] == "True":
            takePicture(i, c, now)
        if config['Generali']['sensori'] == "True":
            takeValues(config, s, now)
            saveValues(i, outSheet)
        time.sleep(inter)
    outWorkbook.close()


if __name__ == '__main__':
    try:
        import sense_hat, picamera, xlsxwriter#, orbit
        main()
    except ImportError as error:
        print('\n  | Import ERROR')
        print(f"  | No module named '{error.message[16:]}'")
        sys.exit(1)