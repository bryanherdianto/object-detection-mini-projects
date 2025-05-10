# Setup Jetson Nano Developer Kit 4GB for YOLOv4-tiny Object Detection

For the most part, you can follow this excellent [guide on Medium](https://medium.com/@aimanhadif10/what-i-have-learned-while-setting-up-jetson-nano-for-an-ai-object-detection-project-b670b5e82de) to set up your Jetson Nano.

However, there are some gaps that may confuse beginners — this README aims to fill in those missing details.

---

## 🧼 1. Formatting an Old Jetson Nano SD Card

If your SD card was previously used for a Jetson Nano OS image, you might run into some strange behavior on your PC:

- Multiple windows may pop up when you insert the SD card.
- It might look like the SD card is corrupted — **but it's not**.

### ✅ What to Do:
- Close all the popups patiently.
- Don't try to explore or fix the partitions manually.

---

## 💾 2. Identifying the Real SD Card

If you're using a file manager (especially on Windows), you may see several drives appear from the same SD card, which can be confusing.

### ✅ Recommended:
- Install and use **[SD Card Formatter](https://www.sdcard.org/downloads/formatter/)**.
- It automatically detects the correct device and lets you cleanly format it.
- This will delete all partitions and prepare the SD card for flashing.

---

## 🚀 3. Flashing the OS and Aftermath

Once formatted:

- Flash the Jetson Nano OS image using tools like **balenaEtcher**.
- After flashing and validating the image, more windows may pop up again — that's **normal**.

### ✅ Just:
- Close those windows one by one.
- **EJECT the SD card SAFELY** before inserting it into your Jetson Nano.

---

## 🕒 4. First Boot Takes Forever

Something most articles don't mention: **the first boot of the Jetson Nano OS can take a *very* long time.**  
You might see a black screen and feel like it's stuck. In my case, I waited for **over an hour**.

![WhatsApp Image 2025-05-10 at 13 23 56_fee17fb1](https://github.com/user-attachments/assets/63e666ab-8279-4f6c-ac31-28ef2d413465)

### ✅ Tip:
- Try pressing the **spacebar** if the screen seems frozen — it may help proceed past any hanging UI.
- Alternatively, check out this workaround image I found online:
  ![WhatsApp Image 2025-05-05 at 09 07 25_a68b8825](https://github.com/user-attachments/assets/2342f837-74c2-4af1-ba83-22e5d3d8b5ba)

---

## 📶 5. WiFi Dongle Might Speed Things Up?

This is anecdotal, but worth noting:

- When I inserted a **WiFi dongle (TP-LINK WN725N)** *before* booting, the initial setup completed significantly faster.
- Maybe it prevents the OS from stalling while searching for a network?

If you have one, plug it in before the first boot — can't hurt.

---

## 🖥️ 6. Camera Setup for Arducam IMX477

Once the OS is running, open a terminal — time to do some magic.

Follow this guide to set up your CSI camera:
📖 [Arducam Native Camera Quick Start](https://docs.arducam.com/Nvidia-Jetson-Camera/Native-Camera/Quick-Start-Guide/)

---

## ⚠️ 7. NEVER Run `apt upgrade` (JetPack Warning)

Before installing anything, **check your JetPack / L4T version**:

```bash
cat /etc/nv_tegra_release
```

---

## 📷 8. Install Arducam IMX477 Support

Run the following commands to install drivers for your CSI camera:

```bash
cd ~
wget https://github.com/ArduCAM/MIPI_Camera/releases/download/v0.0.3/install_full.sh
chmod +x install_full.sh
./install_full.sh -m imx477
````

---

## 🔍 9. Check if Camera is Detected

You can use `v4l2-utils` to confirm your camera is connected:

```bash
sudo apt install v4l-utils
v4l2-ctl --list-formats-ext
```

Or just check with:

```bash
ls /dev/video*
```

You should see something like `/dev/video0`.

---

## 🎥 10. View the Camera Feed with GStreamer

Use the following command to view your camera's live video using GStreamer:

```bash
sensor_id=0  # Use 0 for CAM0 port, 1 for CAM1
Framerate=30

gst-launch-1.0 nvarguscamerasrc sensor_id=$sensor_id ! \
"video/x-raw(memory:NVMM),width=1920,height=1080,framerate=$Framerate/1,format=NV12" ! \
nvvidconv flip-method=0 ! "video/x-raw,width=960,height=720" ! \
nvvidconv ! nvegltransform ! nveglglessink -e
```

![WhatsApp Image 2025-05-10 at 13 23 56_1366519b](https://github.com/user-attachments/assets/e46e78d2-73c5-42fd-8552-4b66cbec1a6a)

## ⚙️ 11. Installing and Running YOLOv4-tiny on Jetson Nano

---

### 🧱 a. Update and Install Dependencies

```bash
sudo apt update
sudo apt upgrade
sudo apt install git build-essential cmake libopencv-dev nano
````

---

### 📦 b. Clone Darknet

```bash
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
```

---

### 📝 c. Edit the Makefile

Use a text editor like `nano`:

```bash
nano Makefile
```

Update these options to enable GPU and OpenCV support on Jetson Nano:

```makefile
GPU=1
CUDNN=1
CUDNN_HALF=0
OPENCV=1
AVX=0
OPENMP=1
LIBSO=1
```

Then save and exit (Ctrl+X → Y → Enter in nano).

---

### 🔨 d. Compile Darknet

```bash
make -j4
```

> Note: `-j4` enables parallel compilation using 4 threads (safe for Jetson Nano 4GB).

---

### ⚡️ e. Verify CUDA Installation

Jetson Nano comes with CUDA preinstalled as part of JetPack. First, check if CUDA is working:

```bash
nvcc --version
```

If you see `command not found`, it means CUDA paths are not set.

---

### ✅ f. Set Up CUDA Environment Variables

Add CUDA paths to your shell config:

```bash
echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

Now check again:

```bash
nvcc --version
```

---

### 🧪 g. Run YOLOv4-tiny Inference

Navigate to your Darknet directory:

```bash
cd ~/darknet
```

#### 📷 Run detection on a static image:

```bash
./darknet detector test data/obj.data yolov4-obj.cfg yolov4-obj.weights data/test.jpg
```

The result will be saved as `predictions.jpg`.

---

#### 🎥 Real-Time Detection with Camera

Use this GStreamer pipeline to access your CSI camera (e.g. Arducam IMX477):

```bash
./darknet detector demo data/obj.data yolov4-obj.cfg yolov4-obj.weights \
"nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=30/1 ! \
nvvidconv flip-method=2 ! video/x-raw, format=BGRx ! \
videoconvert ! video/x-raw, format=BGR ! appsink"
```

![WhatsApp Image 2025-05-10 at 13 23 56_fcddd0bf](https://github.com/user-attachments/assets/e51f6dce-6cfe-45a9-b85e-9cd6604299a7)

You should now see bounding boxes appear in real-time from your live camera feed. The average FPS I got from my real-time detection is 16.8, which is quite good.
