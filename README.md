# 🎙️ Voice Stress Detection System

A real-time AI-powered application that analyzes voice input to detect stress levels using audio features and machine learning techniques.

---

## 🚀 Features

* 🎤 Real-time voice recording and analysis
* 🧠 Stress detection using ML models
* 🔊 Audio feature extraction (Librosa-based)
* 🌐 Interactive UI built with Streamlit
* 🤖 Integration with external AI APIs (Gemini / Hugging Face)
* 📊 Visualization of results

---

## 🏗️ Project Structure

```
voice-stress-detector/
│
├── app.py                  # Main Streamlit app
├── main.py                 # Core execution logic
├── requirements.txt        # Dependencies
├── Dockerfile              # Container setup
│
├── data/                   # Dataset (if any)
├── model/                  # Trained models
│
├── tabs/                   # UI sections
├── utils/                  # Helper functions
│   ├── gemini_utils.py
│   ├── fusion_utils.py
│
├── test_api.py             # API testing
├── test_gemini.py          # Gemini integration test
└── .gitignore
```

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```bash
git clone https://github.com/adarshsingh3618/voice-stress-detector.git
cd voice-stress-detector
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in root directory:

```
GEMINI_API_KEY=your_gemini_api_key
HF_TOKEN=your_huggingface_token
```

⚠️ Never commit `.env` file to GitHub.

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t stress-detector .
```

### Run Container

```bash
docker run -d -p 8501:8501 stress-detector
```

---

## ☁️ AWS Deployment

* Launch EC2 instance (Ubuntu)
* Install Docker or Python environment
* Clone repo
* Run using Docker or Streamlit

---

## 🧠 Tech Stack

* Python
* Streamlit
* Librosa
* Scikit-learn
* NumPy / Pandas
* Docker
* AWS EC2
* Gemini API / Hugging Face

---

## 📌 Versioning

This project follows semantic versioning:

* `v1.0` → Initial stable version
* `v1.1` → Feature improvements
* `v2.0` → Major updates

---

## ⚠️ Security Notes

* API keys are stored using environment variables
* Do NOT expose tokens in code
* Regenerate keys if leaked

---

## 📈 Future Improvements

* 🔁 CI/CD pipeline (GitHub Actions)
* 🌐 Custom domain with HTTPS
* 📦 Kubernetes deployment
* 🧠 Improved ML model accuracy
* 📱 Mobile-friendly UI

---

## 👨‍💻 Author

**Adarsh Singh**
B.Tech Computer Science | DevOps & Cloud Enthusiast

---

## ⭐ Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License.
