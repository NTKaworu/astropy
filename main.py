import configparser, time, datetime, os, sys

sensorsNames = []
sensorsValues = []

def takePicture(i, c, now):    
    c.capture(f'output/images/{i}-{now}.jpg')


def takeDates(config, s , now):
    global sensorsValues
    sensorsValues = []
    if config['Sensori']['umidita']:
        humidity = s.get_humidity()
        sensorsValues.append(humidity)
    if config['Sensori']['temperatura']:
        temperature = s.get_temperature()
        sensorsValues.append(temperature)
    if config['Sensori']['pressione']:
        pressure = s.get_pressure()
        sensorsValues.append(pressure)
    if config['Sensori']['magnetismo']:
        magnetic = s.get_magnetic()
        sensorsValues.append(magnetic)
    if config['Sensori']['orientamento']:
        orientation =s.get_orientation()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**orientation))
    if config['Sensori']['giroscopio']:
        gyro_only = s.get_gyroscope()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**gyro_only))
    if config['Sensori']['giroscopio_raw']:
        gyro_raw = s.get_gyroscope_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**gyro_raw))
    if config['Sensori']['bussola']:
        compass_only = s.get_compass()
        sensorsValues.append(compass_only)
    if config['Sensori']['bussola_raw']:
        compass_raw = s.get_compass_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**compass_raw))
    if config['Sensori']['accelerometro']:
        accel_only = s.get_accelerometer()
        sensorsValues.append("{pitch}, {roll}, {yaw}".format(**accel_only))
    if config['Sensori']['accelerometro_raw']:
        accel_raw = s.get_accelerometer_raw()
        sensorsValues.append("{x}, {y}, {z}".format(**accel_raw))
    
    sensorsValues.append(now)


def saveValues(t, outSheet):
    for i in range(len(sensorsValues)):
        outSheet.write(1+t, i, sensorsValues[i])


def main():
    global sensorsNames
    file = "config.ini"
    config = configparser.ConfigParser()
    config.read(file)

    counter = 0
    path = 'output/images'

    while os.path.exists(path):   
        counter += 1
        path = 'output'+(str(counter)) +'/images'

    os.makedirs(path)

    c = picamera.PiCamera()
    s = sense_hat.SenseHat()
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    
    print(tuple(int(config['Fotocamera']['risoluzione'].split(","))))
    sys.exit(1)

    c.resolution = config['Fotocamera']['risoluzione']
    c.brightness = config['Fotocamera']['luminosità']
    c.image_effect = config['Fotocamera']['effetto']
    c.exposure_mode = config['Fotocamera']['esposizione']
    c.awb_mode = config['Fotocamera']['bilanciamento_bianchi']

    cicliNum = config['Generale']['numero_di_cicli']
    inter = config['Generale']['intervallo_tra_cicli']


    if config['Genare']['sensori'] == True:
        outWorkbook = xlsxwriter.Workbook('out.xlsx')
        outSheet = outWorkbook.add_worksheet()

        if config['Sensori']['umidita']:
            sensorsNames.append("Umidità")

        if config['Sensori']['temperatura']:
            sensorsNames.append("Temperatura")

        if config['Sensori']['pressione']:
            sensorsNames.append("Pressione")

        if config['Sensori']['magnetismo']:
            sensorsNames.append("magnetismo")

        if config['Sensori']['orientamento']:
            sensorsNames.append("Orientamento")

        if config['Sensori']['giroscopio']:
            sensorsNames.append("Giroscopio")

        if config['Sensori']['giroscopio_raw']:
            sensorsNames.append("Giroscopio-raw")

        if config['Sensori']['bussola']:
            sensorsNames.append("Bussola")

        if config['Sensori']['bussola_raw']:
            sensorsNames.append("Bussola-raw")

        if config['Sensori']['accelerometro']:
            sensorsNames.append("Accelerometro")

        if config['Sensori']['accelerometro_raw']:
            sensorsNames.append("Accelerometro-raw")

        sensorsNames.append("Date and time")
        
        for i in range(len(sensorsNames)):
            outSheet.write(0, i, sensorsNames[i])


    for i in range(cicliNum):
        if config['Generali']['fotocamera'] == True:
            takePicture(i, c, now)
        if config['Generali']['sensori'] == True:
            takeDates(config, s, now)
            saveValues(i, outSheet)
        time.sleep(inter)
    outWorkbook.close()


if __name__ == '__main__':
    try:
        import sense_hat, picamera, xlsxwriter
        main()
    except ImportError as error:
        print('\n  | Import ERROR')
        print(f"  | No module named '{error.message[16:]}'")
        sys.exit(1)
