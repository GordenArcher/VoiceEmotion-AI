# Voice Emotion AI

A **Speech Emotion Recognition (SER)** system built with **React Native (frontend)** and **Django REST Framework (backend)**, with a machine-learning model trained in **Google Colab**. The application records audio on mobile, sends it to a Django API, and receives predicted emotions such as *happy, sad, angry, calm,* etc.

This README provides:

* Full project overview
* Architecture
* Folder structure
* Backend (Django) setup
* Frontend (React Native) setup
* Authentication workflow
* Upload flow
* Model training (placeholder, to be added)
* Common errors & debugging

---

## Project Overview

Voice Emotion AI enables users to record their voice on mobile and get an emotion classification. It integrates:

### **Frontend (React Native)**

* Records audio
* Uses Expo or bare RN (depending on your environment)
* Sends audio to Django using authenticated requests (access + refresh token)
* Handles token refresh for long-running sessions

### **Backend (Django + DRF)**

* Provides JWT authentication
* Accepts audio uploads securely
* Runs inference using a trained SER ML model
* Returns predicted emotion + confidence score

### **Machine Learning Model (Google Colab)**

* Reads dataset (RAVDESS)
* Extracts MFCC features
* Trains CNN or LSTM model
* Exports model as `.h5` or `.pt`
* Loaded by Django at runtime

---

## Folder Structure

```
voice-emotion-ai/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── emoapp/
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── utils.py   # ML model loading + inference
│   │   ├── urls.py
│   │   └── ml_models/
│   │       ├── emotional_recognition_model.h5 or model.pt
│   │       └── label_encoder.pkl
│   │       └── scaler.pkl
│   └── media/
│       └── audio_uploads/
│
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── app/
│   │   ├── api/
│   │   │   ├── axiosConfig.js
│   │   │   └── api.ts
│   │   ├── hooks/
│   │   │   └── useAuthRefresh.js
│   │   ├── tabs/
│   └── assets/
│
└── model-training/   # to be added
    └── colab_notebook.ipynb
```

---

## Backend Setup (Django)

### **Install dependencies**

```
pip install -r requirements.txt
```

### **Run migrations**

```
python manage.py migrate
```

### **Start backend**

```
python manage.py runserver
```

---

## Authentication Workflow (Very Important)

The system uses **JWT** with:

* Access Token (short-lived)
* Refresh Token (long-lived)

### How your app works now:

1. User logs in → receives access + refresh
2. Access token expires → upload requests start failing (`401 Unauthorized`)
3. React Native should automatically call refresh endpoint
4. Backend issues a new access token
5. Upload retry succeeds

If refresh is not called → audio upload fails.

---

## Audio Upload Flow

### **Frontend**

1. Record audio using `expo-av` or `react-native-audio-recorder-player`
2. Convert audio → `FormData`
3. Send `POST /recordings/upload/` with header:

```
Authorization: Bearer <access_token>
```

4. If `401` → call refresh token

### **Backend**

1. Receives audio
2. Saves to `media/voice_recordings/`
3. Loads ML model
4. Extracts MFCC features
5. Runs prediction
6. Returns:

```json
{
  "emotion": "happy",
  "confidence": 0.92
}
```

---

## Model Training (to add later)

Include:

* Dataset download steps
* Preprocessing (MFCC extraction)
* Model architecture
* Training logs
* Export steps

---

## Common Issues & Fixes

### **1. Mobile doesn’t need CORS**

Correct → CORS does **not** apply to React Native mobile apps.
Only browsers.

### **2. Unauthorized on upload**

Caused by **expired access token**.
Fix: implement refresh.

### **3. Django logs not showing**

Add this to `settings.py`:

```
LOGGING = {
    "version": 1,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": "DEBUG"},
        "emotion_app": {"handlers": ["console"], "level": "DEBUG"},
    },
}
```

### **4. Cannot find name 'colorScheme'**

Use:

```
import { useColorScheme } from 'react-native';
const colorScheme = useColorScheme();
```

---

## 📱 Frontend Setup (React Native)

Install dependencies:

```
npm install
npx expo install expo-av
npm install axios
```

Run app:

```
npx expo start
```

---

## API Endpoints

### **Auth**

* `POST /auth/login/`
* `POST /auth/register/`

### **Emotion Prediction**

* `POST /recordings/upload/`

---

## Testing

Use Postman / Thunder Client to verify:

1. Login
2. Upload audio
3. Verify response

---

## License

MIT

---

## Contributing

Pull requests welcome. Open issues before major changes to discuss direction.
