# ⚽ Football\_YOLO8

**Transforming Sports Analysis with Intelligent Video Insights**

![Last Commit](https://img.shields.io/github/last-commit/Dinth132/Football_Yolo8?style=flat-square)
![Jupyter Notebooks](https://img.shields.io/badge/Jupyter-54.4%25-yellow?style=flat-square)
![Languages](https://img.shields.io/github/languages/count/Dinth132/Football_Yolo8?style=flat-square)

---

## 📌 Table of Contents

* [📖 Overview](#-overview)
* [🚀 Features](#-features)
* [📦 Getting Started](#-getting-started)

  * [✅ Prerequisites](#-prerequisites)
  * [⚙️ Installation](#-installation)
  * [▶️ Usage](#-usage)
  * [🧪 Testing](#-testing)
* [🛠 Technologies Used](#-technologies-used)
* [📄 License](#-license)

---

## 📖 Overview

**Football\_YOLO8** is an advanced toolkit for automated football (soccer) video analysis. It integrates object detection, multi-object tracking, and spatial transformations to deliver powerful insights for players, coaches, and analysts.
Whether you're building a sports analytics engine, training AI models, or processing match footage — this is your foundation.

---

## 🚀 Features

* **🔌 Modular Architecture** – Detection, tracking, and spatial transformation as separate components.
* **⚡ Real-time Detection** – Uses YOLOv8 for high-speed, accurate object detection.
* **📐 Spatial Analysis** – Player positioning, speed, distance covered, and ball possession estimation.
* **🎞 Video I/O & Visualization** – Annotated video output, frame-by-frame insights, overlays.
* **📊 Data Exploration Tools** – Tools for plotting heatmaps, player movement paths, and event statistics.

---

## 📦 Getting Started

### ✅ Prerequisites

Make sure you have the following installed:

* [Python 3.8+](https://www.python.org/)
* [Anaconda](https://www.anaconda.com/) (recommended)

### ⚙️ Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/Dinth132/Football_Yolo8.git
cd Football_Yolo8
conda env create -f conda.yml
conda activate football_yolo8
```

### ▶️ Usage

After activating the environment, run the main script:

```bash
python main.py
```

> Replace `main.py` with your actual entry-point script if different.

### 🧪 Testing

To run unit and integration tests (ensure test framework is installed):

```bash
pytest tests/
```

> Replace `tests/` with the appropriate path if your tests are structured differently.

---

## 🛠 Technologies Used

* **Language:** Python
* **Object Detection:** [YOLOv8](https://github.com/ultralytics/ultralytics)
* **Tracking:** ByteTrack / SORT (based on config)
* **Visualization:** OpenCV, Matplotlib
* **Environment Management:** Conda
* **Notebook Support:** Jupyter

---

## 🙌 Acknowledgements

* Ultralytics for YOLOv8
* OpenCV community
* DeepSort/ByteTrack authors for tracking logic
* Matplotlib/Pandas for data insights

---

## 📬 Contact

Created and maintained by [Dinith](https://github.com/Dinth132)
Feel free to [open issues](https://github.com/Dinth132/Football_Yolo8/issues) or suggest features!

---

