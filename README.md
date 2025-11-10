# AI Camera Security Scanner# ShodanCamProject



## 🔒 OverviewThis project contains a Shodan-based scanner and a simple ML classifier: `shodan_scan.py` connects to the Shodan API, searches for IP camera devices using a query, and writes the results into `data/shodan_results.csv`; `ai_classifier.py` loads that CSV, heuristically labels banners containing camera-related keywords, vectorizes the banner text, trains a RandomForest classifier to distinguish “exposed” vs “benign” devices, prints the model accuracy, and displays a histogram of flagged devices. I removed Markdown fences so the scripts run as Python, installed the required packages in a virtual environment, and — because the provided Shodan key was limited (403 / no query credits) — I added a realistic sample `data/shodan_results.csv` so the classifier and visualization can be tested without Shodan access.



An intelligent web application that scans for exposed IP cameras using the Shodan API and analyzes them with machine learning to identify potential security vulnerabilities. Unlike generic Shodan interfaces, this tool is **specifically designed for camera security research** with location-based search and AI-powered risk assessment.To reproduce: activate the venv, run `python shodan_scan.py` with a paid/unlocked Shodan key to generate live data, then run `python ai_classifier.py` to train and view results.

# ShodanCamProject

---This project contains a Shodan-based scanner and a simple ML classifier: shodan_scan.py connects to the Shodan API, searches for IP camera devices using a query, and writes the results into data/shodan_results.csv; ai_classifier.py loads that CSV, heuristically labels banners containing camera-related keywords, vectorizes the banner text, trains a RandomForest classifier to distinguish “exposed” vs “benign” devices, prints the model accuracy, and displays a histogram of flagged devices. I removed Markdown fences so the scripts run as Python, installed the required packages in a virtual environment, and—because the provided Shodan key was limited (403 / no query credits)—I added a realistic sample data/shodan_results.csv so the classifier and visualization can be tested without Shodan access. To reproduce: activate the venv, run python shodan_scan.py with a paid/unlocked Shodan key to generate live data, then run python ai_classifier.py to train and view results.

## ✨ Key Features

### 📹 **Camera-Focused Scanning**
- Specialized search interface designed exclusively for IP cameras
- Filter by camera type: webcams, surveillance cameras, RTSP streams, or all cameras
- No generic device scanning - pure camera security focus

### 🌍 **Three Search Methods**
1. **Location Search** - Find cameras by city, country, or state
2. **Coordinate Search** - Pinpoint cameras using GPS coordinates with radius
3. **Network Search** - Scan specific IP ranges (CIDR notation)

### 🤖 **AI-Powered Analysis**
- **RandomForest Machine Learning** model analyzes device banners
- Automatic classification: **Exposed** (vulnerable) vs **Benign** (secure)
- Real-time accuracy metrics and confidence scores
- Visual charts showing risk distribution

### 🔑 **Flexible API Key Management**
- Built-in default key for testing (limited credits)
- Easy custom API key input for paid Shodan accounts
- Secure key handling (not stored, session-only)

### 📊 **Interactive Results Dashboard**
- ML statistics: accuracy, exposed count, benign count
- Color-coded device cards (🔴 Red = Exposed, 🟢 Green = Benign)
- Risk badges on each camera
- Detailed device information with banner analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Emma-Rowe/ShodanCamProject.git
   cd ShodanCamProject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the web server**
   ```bash
   cd shodan_camera_scanner
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

That's it! The app is ready to use.

---

## 💻 Usage Guide

### Setting Up Your API Key

1. The app comes with a **default API key** (limited credits - likely exhausted)
2. For full functionality, get your own key:
   - Visit https://account.shodan.io/
   - Sign up or log in
   - Copy your API key
   - Paste it in the **"Shodan API Key"** field in the app
3. Your key is used only during your session (not saved)

### Searching for Cameras

#### Method 1: Location Search (Recommended)
- **City**: Enter any city name (e.g., "San Diego", "Tokyo", "London")
- **Country** (optional): 2-letter code (e.g., "US", "JP", "GB")
- **State** (optional): U.S. state name (e.g., "California", "Texas")

#### Method 2: Coordinates
- **Latitude**: GPS latitude (e.g., 32.7157)
- **Longitude**: GPS longitude (e.g., -117.1611)
- **Radius** (optional): Search distance in kilometers

#### Method 3: Network Range
- **CIDR Notation**: IP range (e.g., "192.168.1.0/24", "8.8.8.0/24")

### Select Camera Type
- 🎥 **All Cameras** - Searches all camera types
- 💻 **Webcams** - Personal/computer webcams only
- 📹 **Surveillance** - Security/surveillance cameras
- 📡 **RTSP Streams** - Cameras using RTSP protocol (port 554)

### Understanding Results

After clicking **"🔍 Scan for Cameras"**, you'll see:

1. **ML Statistics Dashboard**
   - Model Accuracy (%)
   - Exposed Device Count (potentially vulnerable)
   - Benign Device Count (appears secure)
   - Total Cameras Analyzed

2. **Visualization Chart**
   - Bar graph showing exposed vs benign distribution

3. **Device Cards**
   - Each camera shows:
     - Risk badge (🔴 Exposed or 🟢 Benign)
     - IP address and port
     - Location (city, country)
     - Organization/ISP
     - Product information
     - AI classification result
     - Device banner data

---

## 🛠️ Technical Details

### Machine Learning Model
- **Algorithm**: RandomForest Classifier (50 estimators)
- **Features**: Bag-of-words vectorization (100 max features)
- **Training**: On-the-fly with each search (70/30 train/test split)
- **Classification**: Binary (Exposed=1, Benign=0)
- **Keywords**: webcam, surveillance, camera, rtsp, unauthorized, default, admin

### Tech Stack
- **Backend**: Flask (Python web framework)
- **ML**: scikit-learn (RandomForest, CountVectorizer)
- **Data**: pandas (data manipulation)
- **Visualization**: matplotlib (chart generation)
- **API**: Shodan (device search)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

---

## 📁 Project Structure

```
ShodanCamProject/
├── README.md                       # This file
├── requirements.txt                # Python dependencies
└── shodan_camera_scanner/
    ├── app.py                      # Flask backend with ML
    ├── templates/
    │   └── index.html              # Web interface
    ├── static/
    │   ├── style.css               # Styling
    │   └── script.js               # Frontend logic
    ├── data/
    │   └── shodan_results.csv      # Sample data
    ├── USER_GUIDE.md               # Detailed user guide
    └── QUICK_START.md              # Quick setup guide
```

---

## 📝 Example Searches

### Find webcams in Tokyo, Japan
1. Tab: **Location Search**
2. City: `Tokyo`
3. Country: `JP`
4. Camera Type: **Webcams**

### Find all cameras in California
1. Tab: **Location Search**
2. State: `California`
3. Country: `US`
4. Camera Type: **All Cameras**

### Scan cameras in specific coordinates
1. Tab: **Coordinates**
2. Latitude: `40.7128`
3. Longitude: `-74.0060`
4. Camera Type: **All Cameras**

### Scan a network range
1. Tab: **Network Range**
2. Network: `192.168.1.0/24`
3. Camera Type: **All Cameras**

---

## ⚠️ Common Issues

### "No query credits available"
**Solution**: The default API key is exhausted. Enter your own Shodan API key with credits.
- Free accounts: Limited queries per month
- Paid accounts: More credits
- Get key at: https://account.shodan.io/

### "Invalid API key"
**Solution**: Double-check your API key for typos or extra spaces.

### "No devices found"
**Solutions**:
- Try a different location
- Use broader search (remove optional fields)
- Try a different camera type
- Some areas may have fewer exposed cameras

---

## 🔒 Ethical Use & Legal Notice

This tool is intended for:
- ✅ Educational purposes
- ✅ Security research
- ✅ Authorized penetration testing
- ✅ Identifying vulnerabilities in your own systems

**DO NOT**:
- ❌ Access cameras without authorization
- ❌ Use for malicious purposes
- ❌ Violate privacy laws or regulations
- ❌ Exploit vulnerabilities without permission

**Always use this tool responsibly and legally.**

---

## 📦 Dependencies

```
flask          # Web framework
shodan         # Shodan API client
pandas         # Data manipulation
scikit-learn   # Machine learning
matplotlib     # Visualization
```

All dependencies are in `requirements.txt`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

**Emma Rowe**
- GitHub: [@Emma-Rowe](https://github.com/Emma-Rowe)
- Repository: [ShodanCamProject](https://github.com/Emma-Rowe/ShodanCamProject)

---

## 🙏 Acknowledgments

- **Shodan** - For providing the device search API
- **scikit-learn** - For ML capabilities
- **Flask** - For the web framework

---

**🎉 Happy (ethical) scanning!**
