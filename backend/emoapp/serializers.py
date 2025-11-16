from rest_framework import serializers
from .models import VoiceRecording, EmotionAnalysis, AIResponse, UserProfile


class EmotionAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for EmotionAnalysis model"""
    class Meta:
        model = EmotionAnalysis
        fields = ['id', 'recording', 'emotion', 'confidence', 'analyzed_at']
        read_only_fields = ['analyzed_at']


class AIResponseSerializer(serializers.ModelSerializer):
    """Serializer for AIResponse model"""
    class Meta:
        model = AIResponse
        fields = ['id', 'recording', 'response_text', 'created_at']
        read_only_fields = ['created_at']


class VoiceRecordingSerializer(serializers.ModelSerializer):
    """Serializer for VoiceRecording model with nested relationships"""
    emotion_analyses = EmotionAnalysisSerializer(many=True, read_only=True)
    ai_responses = AIResponseSerializer(many=True, read_only=True)
    latest_emotion = serializers.SerializerMethodField()
    
    class Meta:
        model = VoiceRecording
        fields = [
            'id', 
            'user', 
            'audio_file', 
            'uploaded_at', 
            'emotion_analyses', 
            'ai_responses',
            'latest_emotion'
        ]
        read_only_fields = ['uploaded_at', 'user']
    
    def get_latest_emotion(self, obj):
        """Get the most recent emotion analysis"""
        latest = obj.emotion_analyses.order_by('-analyzed_at').first()
        if latest:
            return {
                'emotion': latest.emotion,
                'confidence': latest.confidence,
                'analyzed_at': latest.analyzed_at
            }
        return None