"""
Voice Emotion Detection Module
Uses MFCCs, pitch, tone, and Random Forest Classifier for emotion recognition
"""

import numpy as np
import librosa
from typing import Dict, Optional, Tuple, List
import io
import tempfile
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import json


class VoiceEmotionDetector:
    """
    Voice emotion detector using audio features:
    - Mel-Frequency Cepstral Coefficients (MFCCs)
    - Pitch (F0)
    - Tone/Energy features
    - Random Forest Classifier
    """
    
    # Emotion categories as per the paper
    EMOTIONS = ['happy', 'sad', 'angry', 'neutral']
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize voice emotion detector
        
        Args:
            model_path: Path to saved Random Forest model (if available)
        """
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = model_path
        
        # If model exists, load it; otherwise we'll train on-the-fly
        if model_path and os.path.exists(model_path):
            self._load_model(model_path)
        else:
            # Initialize with a default trained model (we'll create synthetic training data)
            self._initialize_model()
    
    def _initialize_model(self):
        """Initialize or create a Random Forest model"""
        # For production, you'd load a pre-trained model
        # For now, we'll create a model trained on synthetic/example features
        # In real implementation, this would be trained on a labeled emotion dataset
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
        
        # Train with synthetic baseline data
        # In production, replace with real training data
        self._train_with_synthetic_data()
    
    def _train_with_synthetic_data(self):
        """Train model with synthetic baseline features"""
        # Generate synthetic training examples based on known emotion patterns
        # In production, replace with real labeled audio dataset
        
        n_samples = 400  # 100 per emotion
        n_features = 50  # MFCCs (13) + pitch features (10) + energy (10) + statistics (17)
        
        X_train = []
        y_train = []
        
        # Emotion-specific feature patterns (synthetic)
        emotion_patterns = {
            'happy': {'pitch_mean': 220, 'pitch_std': 40, 'energy_mean': 0.7, 'mfcc_mean': 2.0},
            'sad': {'pitch_mean': 150, 'pitch_std': 20, 'energy_mean': 0.3, 'mfcc_mean': -1.5},
            'angry': {'pitch_mean': 250, 'pitch_std': 60, 'energy_mean': 0.9, 'mfcc_mean': 3.0},
            'neutral': {'pitch_mean': 180, 'pitch_std': 25, 'energy_mean': 0.5, 'mfcc_mean': 0.5}
        }
        
        np.random.seed(42)
        for emotion in self.EMOTIONS:
            pattern = emotion_patterns[emotion]
            for _ in range(n_samples // len(self.EMOTIONS)):
                # Generate synthetic feature vector
                features = self._generate_synthetic_features(pattern)
                X_train.append(features)
                y_train.append(emotion)
        
        # Fit scaler and model
        X_train = np.array(X_train)
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)
    
    def _generate_synthetic_features(self, pattern: Dict) -> List[float]:
        """Generate synthetic feature vector based on emotion pattern"""
        features = []
        
        # MFCC features (13 coefficients)
        mfcc_mean = pattern.get('mfcc_mean', 0)
        mfccs = np.random.normal(mfcc_mean, 1.0, 13)
        features.extend(mfccs.tolist())
        
        # Pitch features (10 features)
        pitch_mean = pattern.get('pitch_mean', 180)
        pitch_std = pattern.get('pitch_std', 30)
        pitches = np.random.normal(pitch_mean, pitch_std, 100)
        features.extend([
            np.mean(pitches),
            np.std(pitches),
            np.median(pitches),
            np.min(pitches),
            np.max(pitches),
            np.percentile(pitches, 25),
            np.percentile(pitches, 75),
            np.mean(np.diff(pitches)),
            np.std(np.diff(pitches)),
            len(pitches[pitches > pitch_mean]) / len(pitches)
        ])
        
        # Energy features (10 features)
        energy_mean = pattern.get('energy_mean', 0.5)
        energies = np.random.normal(energy_mean, 0.15, 100)
        features.extend([
            np.mean(energies),
            np.std(energies),
            np.median(energies),
            np.min(energies),
            np.max(energies),
            np.percentile(energies, 25),
            np.percentile(energies, 75),
            np.mean(np.diff(energies)),
            np.std(np.diff(energies)),
            len(energies[energies > energy_mean]) / len(energies)
        ])
        
        # Statistical features (17 features)
        from scipy import stats
        all_values = np.concatenate([mfccs, pitches, energies])
        
        # Compute skewness and kurtosis safely
        skew_val = 0
        kurt_val = 0
        if len(all_values) > 2:
            try:
                skew_val = float(stats.skew(all_values))
                kurt_val = float(stats.kurtosis(all_values))
            except:
                pass
        
        # Compute correlations safely
        corr1 = 0
        corr2 = 0
        try:
            if len(mfccs) >= 10 and len(pitches) >= 10:
                corr_matrix = np.corrcoef(mfccs[:10], pitches[:10])
                if corr_matrix.shape == (2, 2):
                    corr1 = float(corr_matrix[0, 1])
        except:
            pass
        
        try:
            if len(mfccs) >= 10 and len(energies) >= 10:
                corr_matrix = np.corrcoef(mfccs[:10], energies[:10])
                if corr_matrix.shape == (2, 2):
                    corr2 = float(corr_matrix[0, 1])
        except:
            pass
        
        features.extend([
            float(np.mean(all_values)),
            float(np.std(all_values)),
            float(np.median(all_values)),
            float(np.var(all_values)),
            float(np.min(all_values)),
            float(np.max(all_values)),
            float(np.percentile(all_values, 25)),
            float(np.percentile(all_values, 75)),
            skew_val,
            kurt_val,
            float(len(all_values[all_values > np.mean(all_values)]) / len(all_values)),
            float(np.sum(all_values > 0) / len(all_values)),
            float(np.mean(np.abs(np.diff(all_values)))),
            float(np.std(np.abs(np.diff(all_values)))),
            float(np.mean(np.diff(all_values) > 0)),
            corr1,
            corr2
        ])
        
        return features[:50]  # Ensure exactly 50 features
    
    def extract_features(self, audio_data: np.ndarray, sr: int = 22050) -> np.ndarray:
        """
        Extract audio features from audio signal
        
        Args:
            audio_data: Audio signal as numpy array
            sr: Sample rate (default 22050)
        
        Returns:
            Feature vector (50 features: 13 MFCCs + 10 pitch + 10 energy + 17 statistics)
        """
        features = []
        
        # Ensure audio is not empty
        if len(audio_data) == 0:
            return np.zeros(50)
        
        # Ensure minimum length for analysis
        if len(audio_data) < 1024:
            audio_data = np.pad(audio_data, (0, 1024 - len(audio_data)), mode='constant')
        
        # 1. Extract MFCCs (Mel-Frequency Cepstral Coefficients)
        try:
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
            mfccs_mean = np.mean(mfccs, axis=1)
            features.extend(mfccs_mean.tolist())
        except Exception as e:
            print(f"Error extracting MFCCs: {e}")
            features.extend([0.0] * 13)
        
        # 2. Extract Pitch (F0) features
        try:
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
            pitch_values = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch = pitches[index, t]
                if pitch > 0:
                    pitch_values.append(pitch)
            
            if len(pitch_values) > 0:
                pitch_array = np.array(pitch_values)
                features.extend([
                    np.mean(pitch_array),
                    np.std(pitch_array),
                    np.median(pitch_array),
                    np.min(pitch_array),
                    np.max(pitch_array),
                    np.percentile(pitch_array, 25),
                    np.percentile(pitch_array, 75),
                    np.mean(np.diff(pitch_array)) if len(pitch_array) > 1 else 0,
                    np.std(np.diff(pitch_array)) if len(pitch_array) > 1 else 0,
                    len(pitch_array[pitch_array > np.mean(pitch_array)]) / len(pitch_array) if len(pitch_array) > 0 else 0
                ])
            else:
                features.extend([0.0] * 10)
        except Exception as e:
            print(f"Error extracting pitch: {e}")
            features.extend([0.0] * 10)
        
        # 3. Extract Energy/Tone features
        try:
            # RMS energy
            rms = librosa.feature.rms(y=audio_data)[0]
            # Spectral centroid
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
            
            energy_combined = np.concatenate([rms, spectral_centroids, zcr])
            features.extend([
                np.mean(energy_combined),
                np.std(energy_combined),
                np.median(energy_combined),
                np.min(energy_combined),
                np.max(energy_combined),
                np.percentile(energy_combined, 25),
                np.percentile(energy_combined, 75),
                np.mean(np.diff(energy_combined)) if len(energy_combined) > 1 else 0,
                np.std(np.diff(energy_combined)) if len(energy_combined) > 1 else 0,
                len(energy_combined[energy_combined > np.mean(energy_combined)]) / len(energy_combined) if len(energy_combined) > 0 else 0
            ])
        except Exception as e:
            print(f"Error extracting energy features: {e}")
            features.extend([0.0] * 10)
        
        # 4. Statistical features across all features
        try:
            from scipy import stats
            
            all_features_list = []
            if len(mfccs_mean) > 0:
                all_features_list.append(mfccs_mean)
            if len(pitch_array) > 0:
                all_features_list.append(pitch_array)
            if len(energy_combined) > 0:
                all_features_list.append(energy_combined)
            
            if len(all_features_list) > 0:
                all_features = np.concatenate(all_features_list)
            else:
                all_features = np.zeros(33)
            
            # Compute skewness and kurtosis safely
            skew_val = 0
            kurt_val = 0
            if len(all_features) > 2:
                try:
                    skew_val = float(stats.skew(all_features))
                    kurt_val = float(stats.kurtosis(all_features))
                except:
                    pass
            
            # Compute correlation coefficients safely
            corr1 = 0
            corr2 = 0
            try:
                if len(mfccs_mean) >= 10 and len(pitch_array) >= 10:
                    corr_matrix = np.corrcoef(mfccs_mean[:10], pitch_array[:10])
                    if corr_matrix.shape == (2, 2):
                        corr1 = float(corr_matrix[0, 1])
            except:
                pass
            
            try:
                if len(mfccs_mean) >= 10 and len(energy_combined) >= 10:
                    corr_matrix = np.corrcoef(mfccs_mean[:10], energy_combined[:10])
                    if corr_matrix.shape == (2, 2):
                        corr2 = float(corr_matrix[0, 1])
            except:
                pass
            
            features.extend([
                float(np.mean(all_features)),
                float(np.std(all_features)),
                float(np.median(all_features)),
                float(np.var(all_features)),
                float(np.min(all_features)),
                float(np.max(all_features)),
                float(np.percentile(all_features, 25)),
                float(np.percentile(all_features, 75)),
                skew_val,
                kurt_val,
                float(len(all_features[all_features > np.mean(all_features)]) / len(all_features)) if len(all_features) > 0 else 0,
                float(np.sum(all_features > 0) / len(all_features)) if len(all_features) > 0 else 0,
                float(np.mean(np.abs(np.diff(all_features)))) if len(all_features) > 1 else 0,
                float(np.std(np.abs(np.diff(all_features)))) if len(all_features) > 1 else 0,
                float(np.mean(np.diff(all_features) > 0)) if len(all_features) > 1 else 0,
                corr1,
                corr2
            ])
        except Exception as e:
            print(f"Error computing statistical features: {e}")
            features.extend([0.0] * 17)
        
        # Ensure exactly 50 features
        while len(features) < 50:
            features.append(0.0)
        features = features[:50]
        
        return np.array(features)
    
    def detect_emotion(self, audio_data: np.ndarray, sr: int = 22050) -> Dict[str, float]:
        """
        Detect emotion from audio data
        
        Args:
            audio_data: Audio signal as numpy array
            sr: Sample rate (default 22050)
        
        Returns:
            Dictionary with emotion probabilities
        """
        if self.model is None:
            self._initialize_model()
        
        # Extract features
        features = self.extract_features(audio_data, sr)
        
        # Scale features
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Predict emotion
        emotion_probs = self.model.predict_proba(features_scaled)[0]
        
        # Get predicted emotion
        predicted_emotion_idx = np.argmax(emotion_probs)
        predicted_emotion = self.EMOTIONS[predicted_emotion_idx]
        confidence = emotion_probs[predicted_emotion_idx]
        
        # Map emotion to system moods (angry -> stressed, neutral -> relaxed)
        emotion_mapping = {
            'happy': 'happy',
            'sad': 'sad',
            'angry': 'stressed',
            'neutral': 'relaxed'
        }
        
        mapped_mood = emotion_mapping.get(predicted_emotion, 'happy')
        
        return {
            'emotion': predicted_emotion,
            'mood': mapped_mood,
            'confidence': float(confidence),
            'probabilities': {
                emotion: float(prob) for emotion, prob in zip(self.EMOTIONS, emotion_probs)
            }
        }
    
    def detect_emotion_from_file(self, audio_file_path: str) -> Dict[str, float]:
        """
        Detect emotion from audio file
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Dictionary with emotion probabilities
        """
        # Load audio file
        audio_data, sr = librosa.load(audio_file_path, sr=22050)
        return self.detect_emotion(audio_data, sr)
    
    def detect_emotion_from_bytes(self, audio_bytes: bytes, format: str = 'wav') -> Dict[str, float]:
        """
        Detect emotion from audio bytes
        
        Args:
            audio_bytes: Audio data as bytes
            format: Audio format (wav, mp3, etc.)
        
        Returns:
            Dictionary with emotion probabilities
        """
        # Save to temporary file and load
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{format}') as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
        
        try:
            # Load audio
            audio_data, sr = librosa.load(tmp_path, sr=22050)
            result = self.detect_emotion(audio_data, sr)
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        return result
    
    def _load_model(self, model_path: str):
        """Load pre-trained model from file"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.scaler = model_data['scaler']
        except Exception as e:
            print(f"Error loading model: {e}")
            self._initialize_model()
    
    def save_model(self, model_path: str):
        """Save trained model to file"""
        try:
            model_data = {
                'model': self.model,
                'scaler': self.scaler
            }
            with open(model_path, 'wb') as f:
                pickle.dump(model_data, f)
        except Exception as e:
            print(f"Error saving model: {e}")

