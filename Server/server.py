from flask import Flask, jsonify, send_from_directory, request, render_template
import socket
import struct
import time

app = Flask(__name__)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 4445))
sock.setblocking(False)

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
        "car": outsim_pack[0].decode("utf-8"),
        "gear": outsim_pack[1].decode("utf-8").replace("\x00", ""),
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
    
@app.route('/')
def home():
    data = receiveData()
    return render_template('Home.html')

@app.route('/info')
def info():
    data = receiveData()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
