"""
Model Diagnostic Script - Find out why it's always "calm"
Run this in your Django shell: python manage.py shell
"""

import numpy as np
import librosa
import pickle
from tensorflow import keras
import os

# Load model and preprocessing tools
model_path = 'ml_models/emotion_recognition_model.h5'
scaler_path = 'ml_models/scaler.pkl'
encoder_path = 'ml_models/label_encoder.pkl'

print("="*70)
print("MODEL DIAGNOSTIC - Finding the 'Always Calm' Issue")
print("="*70)

# 1. Check if files exist
print("\n[1] Checking model files...")
for path, name in [(model_path, 'Model'), (scaler_path, 'Scaler'), (encoder_path, 'Encoder')]:
    exists = os.path.exists(path)
    print(f"   {name:12s}: {'✓ Found' if exists else '✗ Missing'} - {path}")

# 2. Load model components
print("\n[2] Loading model components...")
model = keras.models.load_model(model_path)
with open(scaler_path, 'rb') as f:
    scaler = pickle.load(f)
with open(encoder_path, 'rb') as f:
    label_encoder = pickle.load(f)

print(f"   Model input shape: {model.input_shape}")
print(f"   Model output shape: {model.output_shape}")
print(f"   Available emotions: {list(label_encoder.classes_)}")
print(f"   Scaler expects {scaler.n_features_in_} features")

# 3. Test feature extraction with a sample file
print("\n[3] Testing feature extraction...")
# You need to provide a test audio file path
test_audio_path = "media/voice_recordings/recording.wav"  # Change this to your actual file

if os.path.exists(test_audio_path):
    try:
        # Extract features the SAME WAY as training
        audio, sr = librosa.load(test_audio_path, sr=22050, duration=3)
        
        # Pad or trim
        target_length = 22050 * 3
        if len(audio) < target_length:
            audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
        elif len(audio) > target_length:
            audio = audio[:target_length]
        
        print(f"   Audio loaded: {len(audio)} samples, {sr} Hz")
        
        # Extract features
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(y=audio, sr=sr).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sr).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(y=audio, sr=sr).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(audio), sr=sr).T, axis=0)
        
        features = np.hstack([mfccs, chroma, mel, contrast, tonnetz])
        
        print(f"   ✓ Extracted {len(features)} features")
        print(f"   Feature breakdown:")
        print(f"      MFCCs:     {len(mfccs)} features")
        print(f"      Chroma:    {len(chroma)} features")
        print(f"      Mel:       {len(mel)} features")
        print(f"      Contrast:  {len(contrast)} features")
        print(f"      Tonnetz:   {len(tonnetz)} features")
        
        # 4. Check feature statistics
        print(f"\n[4] Feature statistics:")
        print(f"   Min:    {np.min(features):.4f}")
        print(f"   Max:    {np.max(features):.4f}")
        print(f"   Mean:   {np.mean(features):.4f}")
        print(f"   Std:    {np.std(features):.4f}")
        print(f"   Has NaN: {np.isnan(features).any()}")
        print(f"   Has Inf: {np.isinf(features).any()}")
        
        # 5. Test scaling
        print(f"\n[5] Testing scaler...")
        features_reshaped = features.reshape(1, -1)
        print(f"   Features shape before scaling: {features_reshaped.shape}")
        
        features_scaled = scaler.transform(features_reshaped)
        print(f"   Features shape after scaling: {features_scaled.shape}")
        print(f"   Scaled min:  {np.min(features_scaled):.4f}")
        print(f"   Scaled max:  {np.max(features_scaled):.4f}")
        print(f"   Scaled mean: {np.mean(features_scaled):.4f}")
        
        # 6. Test prediction
        print(f"\n[6] Testing prediction...")
        prediction = model.predict(features_scaled, verbose=0)
        print(f"   Raw prediction shape: {prediction.shape}")
        print(f"   Raw prediction probabilities:")
        
        sorted_indices = np.argsort(prediction[0])[::-1]
        for idx in sorted_indices:
            emotion = label_encoder.classes_[idx]
            prob = prediction[0][idx] * 100
            bar = "█" * int(prob / 2)
            print(f"      {emotion:12s} {bar:50s} {prob:5.1f}%")
        
        predicted_class = np.argmax(prediction[0])
        predicted_emotion = label_encoder.classes_[predicted_class]
        confidence = prediction[0][predicted_class] * 100
        
        print(f"\n   🎯 Final Prediction: {predicted_emotion.upper()} ({confidence:.1f}%)")
        
        # 7. Analyze why it might be "calm"
        print(f"\n[7] Diagnosis:")
        
        if predicted_emotion == "calm":
            print("   ❌ ISSUE: Predicting 'calm'")
            
            # Check if all probabilities are similar
            prob_std = np.std(prediction[0])
            if prob_std < 0.05:
                print("   ⚠️  All probabilities are very similar - model is uncertain")
                print("   💡 This suggests the model isn't confident in any emotion")
            
            # Check if calm has highest probability
            calm_prob = prediction[0][list(label_encoder.classes_).index('calm')]
            if calm_prob > 0.5:
                print(f"   ⚠️  'Calm' has very high probability ({calm_prob*100:.1f}%)")
                print("   💡 The model strongly believes this is calm")
            
            # Check feature values
            if np.mean(features) < 0.1:
                print("   ⚠️  Features have very low values")
                print("   💡 Audio might be too quiet or silent")
            
        else:
            print(f"   ✓ Model predicted: {predicted_emotion}")
            
    except Exception as e:
        print(f"   ✗ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print(f"   ✗ Test audio file not found: {test_audio_path}")
    print("   💡 Please record a new audio file and update the path above")

# 8. Check training data distribution
print(f"\n[8] Recommendations:")
print("   1. Check if your training data had balanced emotions")
print("   2. Verify the scaler was fit on the correct training data")
print("   3. Try recording louder/clearer audio")
print("   4. Check if the model was trained correctly (accuracy > 60%)")
print("   5. Consider retraining with data augmentation")

print("\n" + "="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

# 9. Quick fix suggestions
print("\n[9] Quick fixes to try:")
print("""
# Option 1: Retrain the model with your current setup
cd /path/to/notebook
# Run the training script again

# Option 2: Check your training accuracy
# If training accuracy was low, the model didn't learn properly

# Option 3: Test with different audio files
# Try recordings with clear emotions (shouting = angry, laughing = happy)

# Option 4: Add confidence threshold
# In your view, only accept predictions with confidence > 50%
if confidence < 50:
    predicted_emotion = "uncertain"
""")