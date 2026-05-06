from flask import Flask, jsonify, send_from_directory, request, render_template
import socket
import struct
import time

app = Flask(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 4445))
sock.setblocking(False)

test_car_str = "Test Data"
test_gears_str = "N"
test_bars_float = 0.0
test_Lights_float = 0.0
test_Lights_int = 0
testDataAge = 0

def receiveData():
    data = None

    while True:
        try:
            data, fromAddr = sock.recvfrom(4096)
        except socket.error:
            break

    if data is None:
        return []
    outsim_pack = struct.unpack("16s4s13f9I", data)
    car_data = {
        # String 16 characters long
        "car": outsim_pack[0].decode("utf-8"),
        
        # String 4 characters long
        "gear": outsim_pack[1].decode("utf-8").replace("\x00", ""),
        
        # 13 Float values
        "wheelSpeed": outsim_pack[2],
        "airSpeed": outsim_pack[3],
        "rpm": outsim_pack[4],
        "rpmLimit": outsim_pack[5],
        "boost": outsim_pack[6],
        "boostMax": outsim_pack[7],
        "engTemp": outsim_pack[8],
        "oilTemp": outsim_pack[9],
        "fuel": outsim_pack[10],
        "throttle": outsim_pack[11],
        "brake": outsim_pack[12],
        "clutch": outsim_pack[13],
        "lights": outsim_pack[14],
        
        # 9 Intger values
        "parkingbrake": outsim_pack[15],
        "signal_L": outsim_pack[16],
        "signal_R": outsim_pack[17],
        "abs": outsim_pack[18],
        "engineRunning": outsim_pack[19],
        "checkengine": outsim_pack[20],
        "esc": outsim_pack[21],
        "tcs": outsim_pack[22],
        "ev": outsim_pack[23]
    }
    return car_data

def updateTestData():
    global test_Lights_int
    global test_gears_str
    global test_bars_float
    global test_Lights_float
    global testDataAge
    
    if test_bars_float <= 1:
        test_bars_float+= 0.01
    else:
        test_bars_float = 0
        
    if testDataAge >= 1000:
        testDataAge = 0
        if test_Lights_int == 0:
            test_Lights_int = 1
        else:
            test_Lights_int = 0

        if test_gears_str == "N":
            test_gears_str = "D"
        else:
            test_gears_str = "N"
    else:
        testDataAge+= 50   
        
    if (testDataAge == 500 or testDataAge == 1000):
        if test_Lights_float <= 2.0:
            test_Lights_float+= 1.0
        else:
            test_Lights_float = 0.0

def testData():
    updateTestData()
    car_data = {
        # String 16 characters long
        "car": test_car_str,
        
        # String 4 characters long
        # R - N - 1-6
        "gear": test_gears_str,
        
        # 13 Float values
        # 0 - 100
        "wheelSpeed": test_bars_float,
        "airSpeed": test_bars_float,
        "rpm": test_bars_float,
        "rpmLimit": 1.0,
        "boost": test_bars_float,
        "boostMax": test_bars_float,
        "engTemp": test_bars_float,
        "oilTemp": test_bars_float,
        "fuel": test_bars_float,
        "throttle": test_bars_float,
        "brake": test_bars_float,
        "clutch": test_bars_float,
        # 0 - 2
        "lights": test_Lights_float,
        
        # 9 Intger values
        # 0 - 1
        "parkingbrake": test_Lights_int,
        "signal_L": test_Lights_int,
        "signal_R": test_Lights_int,
        "abs": test_Lights_int,
        "engineRunning": test_Lights_int,
        "checkengine": test_Lights_int,
        "esc": test_Lights_int,
        "tcs": test_Lights_int,
        "ev": test_Lights_int
    }
    return car_data
    
@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/debug')
def debug():
    data = testData()
    return jsonify(data)

@app.route('/info')
def info():
    data = receiveData()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
