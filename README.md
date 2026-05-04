# 🎙️ Voice Stress Detection System (AI Companion + Analytics)

An AI-powered web application that analyzes voice and text inputs to detect stress levels using machine learning, audio processing, and generative AI.

This system goes beyond basic prediction by combining **voice intelligence**, **text emotion analysis**, and **behavioral analytics** into a single interactive dashboard.

---

## 🚀 Key Features

### 🎤 Voice-Based Stress Detection

* Audio analysis using **Librosa**
* ML model prediction using extracted features
* Supports file upload, recording, and real-time monitoring

### 💬 Text Emotion Analysis (AI)

* Powered by **Google Gemini API**
* Detects emotional tone from user input
* Enhances prediction accuracy

### ⚗️ Fusion Engine

* Combines voice + text scores into a final stress score
* Weighted prediction system for better reliability

### 📊 Analytics Dashboard

* Stress trends over time
* Average, max, min stress levels
* Visual timeline and insights
* CSV export support

### 🤖 AI Companion

* Provides emotional feedback
* Responds intelligently based on detected stress
* Acts as a supportive assistant

### 🔐 User Authentication System

* Signup/Login functionality
* Password hashing using bcrypt
* User-specific stress history tracking

### 🗄️ Database Integration

* SQLite database (`users.db`)
* Stores:

  * User credentials
  * Stress history
  * Timestamps and scores

---

## 🏗️ Project Structure

```
voice-stress-detector/
│
├── app.py                  # Streamlit app entry point
├── main.py                 # Core prediction pipeline
├── requirements.txt        # Dependencies
├── Dockerfile
├── README.md
│
├── tabs/                   # UI modules
│   ├── upload.py
│   ├── record.py
│   └── realtime.py
│
├── utils/                  # Helper modules
│   ├── audio_utils.py
│   ├── gemini_utils.py
│   ├── fusion_utils.py
│   └── db_auth.py
│
├── model/                  # ML model files
│   ├── stress_model.pkl
│   └── scaler.pkl
│
├── users.db                # SQLite database (local only)
└── .env                    # Environment variables (not committed)
```

---

## 🧠 How It Works

```
User Input (Audio / Text)
        ↓
Audio Processing (Librosa)
        ↓
ML Model Prediction
        ↓
Gemini API (Text Analysis)
        ↓
Fusion Engine (Final Score)
        ↓
Store in Database + Display Dashboard
```

---

## ⚙️ Tech Stack

**Frontend**

* Streamlit

**Backend**

* Python

**Machine Learning**

* scikit-learn (HistGradientBoosting)
* librosa
* numpy

**AI Integration**

* Google Gemini API

**Database**

* SQLite (users.db)
* bcrypt (password hashing)

**Realtime**

* streamlit-webrtc

---

## ⚙️ Local Setup

### 1. Clone Repository

```
git clone https://github.com/adarshsingh3618/voice-stress-detector.git
cd voice-stress-detector
```

---

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in root directory:

```
GEMINI_API_KEY=your_api_key_here
```

⚠️ Do NOT upload `.env` to GitHub

---

## ▶️ Run Application

```
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## ☁️ Deployment

### 🌐 Streamlit Cloud (Recommended)

* Push code to GitHub
* Deploy via Streamlit Cloud
* Add API key in **Secrets**

---

### ☁️ AWS EC2 (Production)

```
ssh -i your-key.pem ubuntu@your-ip
git clone <repo>
cd voice-stress-detector

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

### 🐳 Docker Deployment

```
docker build -t stress-detector .
docker run -d -p 8501:8501 stress-detector
```

---

## 📊 Stress Level Classification

| Score | Level    |
| ----- | -------- |
| 0–3   | Low      |
| 4–6   | Moderate |
| 7–8   | High     |
| 9–10  | Extreme  |

---

## ⚠️ Notes

* SQLite is used for local storage (resets on cloud deployment)
* Real-time monitoring may have limitations on Streamlit Cloud
* Model files must be included in the repository

---

## 📈 Future Improvements

* AI-generated stress reports
* Weekly/monthly analytics
* Cloud database integration (Supabase/Firebase)
* CI/CD pipeline
* Mobile-friendly UI
* Advanced visualization (Plotly)

---

## 👨‍💻 Author

**Adarsh Singh**
B.Tech Computer Science
DevOps & Cloud Enthusiast

---

## ⭐ Contribution

Contributions are welcome.
Feel free to open issues or submit pull requests.

---

## 📄 License

MIT License
