# main.py
import os
from flask import Flask, jsonify, render_template, request

from gmc300 import Gmc300
from serial_device import SerialDevice
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

serial_port = os.getenv('SERIAL_PORT')
baud_rate = int(os.getenv('BAUD_RATE'))

serial = SerialDevice(serial_port=serial_port, baud_rate=baud_rate)
gmc = Gmc300(serial=serial)
gmc.subscribe()


@app.route("/command", methods=["POST"])
def send_command():
    command = request.form.get("command")
    if not command:
        return jsonify({"error": "No command provided"}), 400
    
    result = gmc.send_command(command=command)
    try:
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Error: {e}"}), 500

@app.route("/state", methods=["GET"])
def get_data():
    """API endpoint to get the latest CPS, CPM, and CPH."""
    counter = gmc.get_counter()
    result = counter.get_data()
    return jsonify(result)


@app.route("/cph-buffer", methods=["GET"])
def get_cph_buffer():
    """
    Returns the last `count` values in the cph_buffer as a list.
    If the number of items in the queue is less than `count`,
    returns the entire queue.
    """
    count = request.args.get("count", default=None, type=int)
    counter = gmc.get_counter()
    result = counter.get_cph_buffer(count)
    return jsonify(result)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)