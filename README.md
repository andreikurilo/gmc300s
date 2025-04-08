# 🚀 Getting Started

## 🐳 Run the Project with Docker

## Run Project In Docker
You can build and start the project using Docker:
```bash
SERIAL_PORT=/dev/ttyUSB0 BAUD_RATE=57600 docker-compose up -d --build
```

Alternatively, use the helper script:

```bash
chmod +x compose.sh
./compose.sh
```

## 🔌 Check Connected USB Devices

To identify connected USB devices and available serial ports:

```bash
dmesg | grep tty
lsusb
ls /dev/tty*
udevadm info --query=all --name=/dev/ttyUSB0
```

## 🐍 Set Up Python Virtual Environment

If you prefer running locally without Docker:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create .env File

Create a .env file in the project root with your serial configuration:

```ini
SERIAL_PORT=/dev/ttyUSB0
BAUD_RATE=57600
```

## 📡 API Testing

Use curl to interact with the API:

* Get Current Data:

```bash
curl localhost:5000/state
```

* Get CPH Buffer for Last 5 Minutes:

```bash
curl localhost:5000/cph-buffer?count=300
```

* Send Commands to Device:

```bash
curl -X POST localhost:5000/command -d "command=<GETCPM>>" # Gets cpm
curl -X POST localhost:5000/command -d "command=<HEARTBEAT1>>"  # Enable heartbeat
curl -X POST localhost:5000/command -d "command=<HEARTBEAT0>>"  # Disable heartbeat
```

## 🐞 Debugging with VS Code

If you’re using VS Code, a launch configuration is included in .vscode/launch.json to help you start the Flask app with debugging enabled.
⚠️ Note:
*	The Flask app runs on port 5001, not the default 5000. If you have something else running on port 5000, this avoids conflicts.
* The launch config sets environment variables for the serial connection:

```json 
"SERIAL_PORT": "/dev/ttyUSB0",
"BAUD_RATE": "57600"
```
* Make sure to double-check these values based on your actual connected device. You can use commands like dmesg | grep tty or ls /dev/tty* to find the correct serial port.

If you’re not using VS Code, you can set these environment variables manually before running the app.