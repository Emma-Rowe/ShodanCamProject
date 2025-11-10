# 📹 AI Camera Security Scanner - User Guide

## Overview
This tool is specifically designed to scan for exposed IP cameras using Shodan's database and analyze them with machine learning to identify potential security risks.
---

## 🌍 Search Methods

### 1. 📍 Location Search (Recommended)
Best for: Finding cameras in specific cities or regions

**Fields:**
- **City** (Required): Enter any city name
  - Examples: `San Diego`, `London`, `Tokyo`, `Paris`
- **Country** (Optional): 2-letter code to narrow results
  - Examples: `US`, `UK`, `JP`, `FR`
- **State** (Optional): For U.S. locations only
  - Examples: `California`, `Texas`, `New York`

**Example:** 
- City: `San Diego` + Country: `US` → Find all cameras in San Diego, USA

---

### 2. 🗺️ Coordinates
Best for: Precise location targeting

**Fields:**
- **Latitude**: GPS latitude coordinate
  - Example: `32.7157`
- **Longitude**: GPS longitude coordinate
  - Example: `-117.1611`
- **Radius** (Optional): Search distance in km
  - Example: `50`

**Example:**
- Lat: `40.7128`, Lon: `-74.0060` → Cameras near New York City coordinates

---

### 3. 🌐 Network Range
Best for: Scanning specific IP ranges (advanced users)

**Field:**
- **Network Range (CIDR)**: IP range in CIDR notation
  - Examples: `192.168.1.0/24`, `8.8.8.0/24`

**Example:**
- `192.168.0.0/16` → Scan entire 192.168.x.x network

---

## 📹 Camera Types

Choose what type of cameras to search for:

- **🎥 All Cameras** - Searches for all types of IP cameras (default)
- **💻 Webcams** - Only personal/computer webcams
- **📹 Surveillance** - Only surveillance/security cameras
- **📡 RTSP Streams** - Cameras using RTSP protocol (port 554)

---

## 🤖 AI Analysis Results

After searching, you'll see:

### ML Statistics Dashboard
- **Model Accuracy**: How confident the AI is in its predictions (higher = better)
- **Exposed Devices**: Cameras flagged as potentially vulnerable (🔴 Red)
- **Benign Devices**: Cameras that appear secure (🟢 Green)
- **Total Analyzed**: Total cameras found

### Visualization Chart
Bar graph showing the distribution of exposed vs benign cameras

### Device Cards
Each camera shows:
- 🔴 **Exposed Badge** or 🟢 **Benign Badge**
- IP address and port
- Location (city, country)
- Organization/ISP
- Product information
- AI classification
- Banner data (device information)

---

## 💡 Tips for Best Results

1. **Start with Location Search** - Easiest and most intuitive
2. **Be Specific** - Adding country/state narrows results
3. **Use Your Own API Key** - To use your new API key:

Open app.py (line 16)
Replace the old key with your new one:

4. **Check Exposed Cameras** - Red-flagged devices need attention
5. **Experiment with Camera Types** - Different types yield different results

---

## ⚠️ Common Errors

### "No query credits available"
- **Solution**: Enter your own Shodan API key with credits
- Free accounts get limited searches per month
- Upgrade at: https://account.shodan.io/billing

### "No devices found"
- Try a broader search (e.g., remove optional fields)
- Try a different location or camera type
- Some locations may have no exposed cameras

---

## 🎯 Example Searches

### Find webcams in Tokyo
- Tab: **Location Search**
- City: `Tokyo`
- Country: `JP`
- Camera Type: **Webcams**

### Find all cameras in California
- Tab: **Location Search**
- State: `California`
- Country: `US`
- Camera Type: **All Cameras**

### Scan a specific network
- Tab: **Network Range**
- Network: `8.8.8.0/24`
- Camera Type: **All Cameras**

---

## 🔒 Ethical Use

- This tool is for **educational and security research** purposes only
- Do not access cameras without authorization
- Use responsibly and legally
- Report vulnerabilities to affected organizations

---

**Enjoy scanning! 🎉**
