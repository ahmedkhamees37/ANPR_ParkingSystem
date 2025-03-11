# 🚗 ANPR Parking System

## 🌟 Introduction
Welcome to the **ANPR Parking System**, an innovative solution designed to revolutionize parking management! 🚀 This system utilizes **Automatic Number Plate Recognition (ANPR)** technology to detect vehicle license plates seamlessly, logging entries and exits to ensure an efficient and automated parking experience. 

## 🎯 Key Features
✅ **Automatic License Plate Recognition** - Detects and processes vehicle plates with high accuracy.  
✅ **Real-time Entry & Exit Logging** - Keeps track of vehicles entering and leaving the parking area.  
✅ **Database Integration** - Securely stores vehicle records for easy access and retrieval.  
✅ **Web-Based Dashboard** - Intuitive interface for monitoring and management.  
✅ **Scalable & Secure** - Designed to handle multiple vehicles efficiently.  

## 🛠 Installation Guide
### Prerequisites
Before running the system, ensure you have the following installed:
🔹 **Python 3.x**  
🔹 **OpenCV** (for image processing)  
🔹 **Flask** (for backend development)  
🔹 **MongoDB** (for data storage)  
🔹 **Docker** (optional, for containerization)  

### 🚀 Quick Setup
1️⃣ Clone the repository:
   ```bash
   git clone https://github.com/ahmedkhamees37/ANPR_ParkingSystem.git
   cd ANPR_ParkingSystem
   ```
2️⃣ Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3️⃣ Set up the database (**MongoDB**):
   - Ensure MongoDB is running.
   - Configure the connection settings in `config.py`.
4️⃣ Run the application:
   ```bash
   python app.py
   ```
5️⃣ Open your browser and visit **`http://localhost:5000`** to access the system. 🎉

## 📌 How It Works
🚘 **Capture & Recognize** - The system automatically detects and reads license plates using a connected camera.  
📜 **Store & Manage** - Logs all detected vehicles in the database for easy tracking.  
📊 **Monitor & Control** - Admins can view parking logs, manage entries, and generate reports from the web dashboard.  

## 🏗 Technologies Used
🔹 **Python** - Core programming language.  
🔹 **Flask** - Web framework for backend operations.  
🔹 **OpenCV** - Image processing and ANPR engine.  
🔹 **MongoDB** - NoSQL database for record storage.  
🔹 **Docker** - Optional, for containerization and deployment.  

## 🤝 Contribute & Collaborate
We welcome contributions! Follow these steps to get involved:  
1️⃣ **Fork** this repository.  
2️⃣ Create a **new feature branch** (`feature-branch`).  
3️⃣ Commit your changes and improvements.  
4️⃣ Push your branch and submit a **Pull Request**!  

## 📜 License
This project is open-source and licensed under the **MIT License**. Feel free to use and enhance it! ✨

---
📌 **Created with passion by Ahmed Khamis Hassan as a Graduation Project.** 🎓 🚀

