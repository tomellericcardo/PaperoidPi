apt update
apt install -y python3-pip python3-gpiozero python3-picamera python3-llvmlite libbluetooth-dev libhidapi-dev libatlas-base-dev python-llvmlite llvm-dev libopenjp2-7-dev libtiff5
pip3 install --no-cache-dir -r requirements.txt
echo You need to reboot your Pi before using this tool
