apt update
apt install -y python3-pip libbluetooth-dev libhidapi-dev libatlas-base-dev python3-llvmlite python-llvmlite llvm-dev libopenjp2-7-dev libtiff5
pip3 install --no-cache-dir -r requirements.txt
echo You need to reboot your Pi before using this
