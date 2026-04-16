# 🎙️ Voice Stress Detection System

An AI-powered web application that analyzes voice input to detect stress levels using audio processing and machine learning techniques.

---

## 🚀 Features

* 🎤 Real-time voice recording & analysis
* 🧠 Stress detection using ML models
* 🔊 Audio feature extraction (Librosa)
* 🌐 Interactive UI with Streamlit
* 🤖 AI API integration (Gemini / Hugging Face)
* 📊 Result visualization

---

## 🏗️ Project Structure

```
voice-stress-detector/
│
├── app.py                  # Streamlit app entry point
├── main.py                 # Core logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker setup
├── README.md
│
├── data/                   # Dataset (if used)
├── model/                  # Trained models
├── tabs/                   # UI modules
├── utils/                  # Helper utilities
│
├── test_api.py             # API test scripts
├── test_gemini.py          # Gemini integration
└── venv/                   # Virtual environment (not pushed)
```

---

## ⚙️ Local Setup (Recommended)

### 1. Clone Repository

```
git clone https://github.com/adarshsingh3618/voice-stress-detector.git
cd voice-stress-detector
```

### 2. Install Python Tools

```
sudo apt update
sudo apt install python3-pip python3-venv -y
```

### 3. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in root directory:

```
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token
```

⚠️ Important:

* Do NOT push `.env` to GitHub
* Add `.env` to `.gitignore`

---

## ▶️ Run Application

```
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Open in browser:

```
http://localhost:8501
```

---

## ☁️ AWS Deployment (Ubuntu EC2)

### 1. Launch EC2

* OS: Ubuntu
* Open ports: **22, 8501**

---

### 2. Connect to Server

```
ssh -i your-key.pem ubuntu@your-public-ip
```

---

### 3. Clone Project

```
git clone https://github.com/adarshsingh3618/voice-stress-detector.git
cd voice-stress-detector
```

---

### 4. Install Python & Setup Environment

```
sudo apt update
sudo apt install python3-pip python3-venv -y

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. Run Application

```
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

### 6. Access App

```
http://your-public-ip:8501
```

---

## 🐳 Docker Deployment (Optional)

### Build Image

```
docker build -t stress-detector .
```

### Run Container

```
docker run -d -p 8501:8501 stress-detector
```

---

## 📌 Versioning

This project follows semantic versioning:

* `v1.0` → Initial stable version
* `v1.1` → Feature improvements
* Future → enhancements & scaling

---

## ⚠️ Security Best Practices

* Never hardcode API keys
* Use environment variables (`.env`)
* Rotate keys if exposed
* Use SSH for GitHub access

---

## 📈 Future Improvements

* 🔁 CI/CD pipeline (GitHub Actions)
* 🌐 Domain + HTTPS (Nginx)
* 🐳 Optimized Docker image
* ☸️ Kubernetes deployment
* 🧠 Model accuracy improvements

---

## 👨‍💻 Author

**Adarsh Singh**
B.Tech Computer Science
DevOps & Cloud Enthusiast

---

## ⭐ Contributing

Contributions are welcome. Open an issue or submit a PR.

---

## 📄 License

MIT License
