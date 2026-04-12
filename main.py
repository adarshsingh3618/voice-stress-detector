import os
import librosa
import numpy as np
import soundfile as sf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import HistGradientBoostingClassifier
import joblib

DATA_DIR = "data"
MODEL_PATH = "model/stress_model.pkl"
SCALER_PATH = "model/scaler.pkl"

# -----------------------------------------
# Emotion → Stress Mapping (RAVDESS)
# -----------------------------------------
emotion_to_stress = {
    "01": 0,  # neutral
    "02": 0,  # calm
    "03": 0,  # happy
    "04": 1,  # sad
    "05": 1,  # angry
    "06": 1,  # fearful
    "07": 1,  # disgust
    "08": 0,  # surprised
}

# -----------------------------------------
# Feature Extraction (MFCC + Delta + Delta2)
# -----------------------------------------
def extract_features(file_path):
    try:
        audio, sr = sf.read(file_path)

        # Convert stereo → mono
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        # MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)

        # Delta features
        delta = librosa.feature.delta(mfcc)
        delta2 = librosa.feature.delta(mfcc, order=2)

        # Combine features
        combined = np.concatenate([mfcc, delta, delta2], axis=0)

        # Mean pooling
        return np.mean(combined.T, axis=0)

    except Exception as e:
        print(f"Error: {file_path} → {e}")
        return None


# -----------------------------------------
# Load Dataset
# -----------------------------------------
def load_dataset():
    X, y = [], []

    print("🔍 Loading dataset...")

    for actor in os.listdir(DATA_DIR):
        actor_path = os.path.join(DATA_DIR, actor)

        if not os.path.isdir(actor_path):
            continue

        for file in os.listdir(actor_path):
            if file.endswith(".wav"):
                emotion_code = file.split("-")[2]

                label = emotion_to_stress.get(emotion_code)
                if label is None:
                    continue

                path = os.path.join(actor_path, file)
                features = extract_features(path)

                if features is not None:
                    X.append(features)
                    y.append(label)

    print(f"✅ Loaded {len(X)} samples")
    return np.array(X), np.array(y)


# -----------------------------------------
# Train Model
# -----------------------------------------
def train_model():
    X, y = load_dataset()

    print("⚙️ Scaling features...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    print("🧠 Training model...")
    model = HistGradientBoostingClassifier(
        max_iter=300,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("\n📊 Evaluation:")
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    # Save model
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    print("\n✅ Model saved")
    print("📁", MODEL_PATH)


# -----------------------------------------
# Predict Function
# -----------------------------------------
def predict(audio_path):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    feat = extract_features(audio_path)

    if feat is None:
        return "Error", 0.0

    feat_scaled = scaler.transform([feat])

    pred = model.predict(feat_scaled)[0]
    prob = model.predict_proba(feat_scaled)[0][1]

    return ("Stress" if pred == 1 else "Not Stress"), float(prob)


# -----------------------------------------
# Run Training
# -----------------------------------------
if __name__ == "__main__":
    train_model()