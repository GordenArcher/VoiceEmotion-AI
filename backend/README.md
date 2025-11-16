# Voice Emotion Recognition - Backend API

Django REST Framework backend for Speech Emotion Recognition application with machine learning integration.

## Features

- **User Authentication** - JWT-based authentication with registration and login
- **Voice Recording Management** - Upload and store voice recordings
- **Real-time Emotion Analysis** - ML-powered emotion detection from audio
- **User Profiles** - Complete profile management with customization
- **Recording History** - Track and analyze emotion patterns over time
- **AI Responses** - Context-aware responses based on detected emotions
- **Statistics Dashboard** - Comprehensive emotion analytics

## Tech Stack

- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database (production) / SQLite (development)
- **TensorFlow 2.13+** - Deep learning model inference
- **Librosa** - Audio feature extraction
- **JWT Authentication** - djangorestframework-simplejwt
- **CORS Support** - django-cors-headers

## Project Structure

```
backend/
├── emoapp/                    # Main application
│   ├── models.py              # Database models
│   ├── views.py               # API endpoints
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   └── utils/
│       └── model_loader.py    # ML model utilities
├── ml_models/                 # Trained ML models
│   ├── emotion_recognition_model.h5
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── model_metadata.json
├── media/                     # User uploaded files
│   └── voice_recordings/
├── backend/                   # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- pip
- virtualenv (recommended)
- PostgreSQL (for production)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/GordenArcher/VoiceEmotionAI_model_training/tree/main/backend.git
cd backend
```

2. **Create virtual environment**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Collect static files (production)**
```bash
python manage.py collectstatic
```

## Running the Server

### Development
```bash
python manage.py runserver
```
Server will run at `http://localhost:8000`

### Production
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register/          - Register new user
POST   /api/v1/auth/login/             - Login user
POST   /api/v1/auth/logout/            - Logout user
POST   /api/v1/auth/token/refresh/     - Refresh access token
```

### User Profile
```
GET    /api/v1/profile/                - Get user profile
PUT    /api/v1/profile/update/         - Update profile
DELETE /api/v1/profile/delete/         - Delete account
```

### Voice Recordings
```
POST   /api/v1/recordings/upload/      - Upload & analyze audio
GET    /api/v1/recordings/             - List all recordings
GET    /api/v1/recordings/<id>/        - Get specific recording
DELETE /api/v1/recordings/<id>/delete/ - Delete recording
POST   /api/v1/recordings/<id>/reanalyze/ - Re-analyze emotion
GET    /api/v1/recordings/statistics/  - Get emotion statistics
```

### Emotion Analysis
```
GET    /api/v1/analyses/               - List all analyses
GET    /api/v1/analyses/<id>/          - Get specific analysis
```

### AI Responses
```
POST   /api/v1/ai-responses/generate/  - Generate AI response
GET    /api/v1/ai-responses/           - List AI responses
GET    /api/v1/ai-responses/<id>/      - Get specific response
```

## ML Model

### Supported Emotions
The model can detect 8 emotions:
- 😐 Neutral
- 😌 Calm
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😨 Fearful
- 🤢 Disgust
- 😲 Surprised

### Model Details
- **Architecture**: Deep Neural Network (512→256→128→64)
- **Input Features**: 193 audio features (MFCC, Chroma, Mel Spectrogram, etc.)
- **Framework**: TensorFlow/Keras
- **Training Dataset**: RAVDESS (1,440 audio samples)
- **Accuracy**: ~65% on test set

### Feature Extraction
The model extracts the following features from audio:
- **MFCC** (40 coefficients) - Mel-frequency cepstral coefficients
- **Chroma** (12 bins) - Pitch class profiles
- **Mel Spectrogram** (128 bins) - Frequency representation
- **Spectral Contrast** (7 bands) - Spectral peak and valley differences
- **Tonnetz** (6 features) - Tonal centroid features

## Database Models

### User Profile
```python
- username
- email
- first_name
- last_name
- display_name
- bio
- avatar
- total_recordings
```

### Voice Recording
```python
- user (ForeignKey)
- audio_file
- uploaded_at
```

### Emotion Analysis
```python
- recording (ForeignKey)
- emotion
- confidence
- analyzed_at
```

### AI Response
```python
- recording (ForeignKey)
- response_text
- created_at
```

## Testing

### Run tests
```bash
python manage.py test
```

### Test ML model
```bash
python diagnose_model.py
```

### API testing with cURL
```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Upload audio
curl -X POST http://localhost:8000/api/v1/recordings/upload/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio_file=@recording.wav"
```

## Security

- **JWT Authentication** - Secure token-based auth
- **CORS Protection** - Configured allowed origins
- **File Upload Validation** - Size and type restrictions
- **SQL Injection Protection** - Django ORM
- **XSS Protection** - Built-in Django security
- **CSRF Protection** - Enabled for web forms

## Configuration

### settings.py
```python
# Audio file settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_AUDIO_FORMATS = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']

# ML Model paths
ML_MODELS_DIR = BASE_DIR / 'ml_models'

# CORS settings (adjust for production)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:19006",  # Expo
]
```


## Troubleshooting

### Model not loading
```bash
# Verify model files exist
ls -la ml_models/

# Check file permissions
chmod 644 ml_models/*.h5 ml_models/*.pkl

# Test model loading
python manage.py shell
>>> from emoapp.utils.model_loader import EmotionRecognitionModel
>>> model = EmotionRecognitionModel()
>>> model.is_ready()
```

### Audio processing errors
```bash
# Install audio dependencies
pip install librosa soundfile audioread resampy

# For macOS
brew install ffmpeg

# For Ubuntu
sudo apt-get install ffmpeg libsndfile1
```

### Database errors
```bash
# Reset database
python manage.py flush
python manage.py migrate

# Or delete and recreate
rm db.sqlite3
python manage.py migrate
```

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [Librosa Documentation](https://librosa.org/doc/latest/index.html)
- [RAVDESS Dataset](https://zenodo.org/record/1188976)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Gorden Archer - [GitHub](https://github.com/GordenArcher)

## 🙏 Acknowledgments

- RAVDESS dataset creators
- TensorFlow team
- Django community
- Librosa developers

---

Made with ❤️ for emotion recognition research and development