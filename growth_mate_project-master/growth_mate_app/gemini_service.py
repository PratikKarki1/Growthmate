import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key="AIzaSyA2sCXOXbnsSx4LRiQ7h9-byTwa1Y80fR8")

# Initialize the model with the new version
model = genai.GenerativeModel('gemini-1.5-flash')

# System context about our LMS platform
SYSTEM_CONTEXT = """You are an AI assistant for Growth Mate, a Learning Management System (LMS) for retail training.
Key features of our platform:
- Users can enroll in multiple courses
- Courses contain various content types (text, images, videos)
- User roles include admin, retail manager, and retail employee
- Each course has a duration and due date
- Users can track their course progress
- Content is organized into sections within courses
- Both employees and managers can enroll in courses 

Please provide helpful and accurate information about our platform's features and capabilities."""

def get_bot_response(user_message, chat_history=None):
    """
    Get a response from the Gemini API based on user input and chat history
    """
    try:
        # Prepare context from chat history
        context = SYSTEM_CONTEXT + "\n\n"
        if chat_history:
            for msg in chat_history:
                prefix = "Assistant: " if msg.is_bot else "User: "
                context += f"{prefix}{msg.message}\n"
        
        # Prepare the prompt
        prompt = f"{context}User: {user_message}\nAssistant:"
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            return "I apologize, but I couldn't generate a response at this time."
            
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}" 