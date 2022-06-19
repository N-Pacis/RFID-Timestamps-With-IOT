import requests
import csv
import serial

def readFile(file):
    jsonArray = []
    with open(file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)
    return jsonArray

ser = serial.Serial(
        port='COM12', #plz change this according to your port number
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser.flush()

if __name__ == '__main__':
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            f=open("transactions.txt","a")
            f.write(line)
            f.write("\n")
            f.close()
            data = readFile("transactions.txt")
            res = requests.post(
                'http://localhost:4000/data/upload', json=data)
            if res.ok:
                print("Data uploaded")
                ser.write(bytes("Data uploaded"), 'utf-8')
                ser.flush()
