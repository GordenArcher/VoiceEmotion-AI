def _generate_response(emotion, confidence):
    """
    Generate contextual response based on emotion
    You can integrate with Claude API or other LLMs here
    """
    responses = {
        'happy': f"I can hear the joy in your voice! (Confidence: {confidence:.1f}%) It's wonderful to see you in such a positive mood. What's bringing you happiness today?",
        'sad': f"I sense some sadness in your voice (Confidence: {confidence:.1f}%). Remember, it's okay to feel this way. Would you like to talk about what's bothering you?",
        'angry': f"I detect frustration in your tone (Confidence: {confidence:.1f}%). Take a deep breath. What's causing you to feel this way?",
        'neutral': f"You sound calm and composed (Confidence: {confidence:.1f}%). How are things going for you today?",
        'fearful': f"I hear some anxiety in your voice (Confidence: {confidence:.1f}%). Remember, you're safe. What's making you feel uneasy?",
        'disgust': f"I sense some discomfort (Confidence: {confidence:.1f}%). What's bothering you?",
        'surprised': f"You sound surprised! (Confidence: {confidence:.1f}%) Something unexpected happened?",
        'calm': f"You sound very peaceful (Confidence: {confidence:.1f}%). That's great to hear!"
    }
    
    return responses.get(emotion, f"I detected a {emotion} emotion with {confidence:.1f}% confidence. How can I help you today?")

