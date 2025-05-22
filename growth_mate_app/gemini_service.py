import google.generativeai as genai
from django.conf import settings
import os
from dotenv import load_dotenv
import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

load_dotenv()

# Configure the Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model with Flash version for better free tier limits
# Free tier limits for gemini-1.5-flash:
# - 15 RPM (Requests per minute)
# - 250,000 TPM (Tokens per minute)
# - 500 RPD (Requests per day)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')  # Using flash for better free tier limits
except Exception as e:
    logger.error(f"Error initializing Gemini model: {str(e)}")
    raise

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

def retry_with_backoff(max_retries=3, initial_delay=1, max_delay=32):
    """
    Decorator that implements exponential backoff for retrying functions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if "429" in str(e):  # Rate limit error
                        logger.warning(f"Rate limit hit, attempt {attempt + 1}/{max_retries}. Waiting {delay} seconds...")
                        time.sleep(delay)
                        delay = min(delay * 2, max_delay)  # Exponential backoff
                    else:
                        raise  # Re-raise if it's not a rate limit error
            
            # If we've exhausted all retries, raise the last exception
            raise last_exception
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, initial_delay=1, max_delay=32)
def get_bot_response(user_message, chat_history=None):
    """
    Get a response from the Gemini API based on user input and chat history
    """
    try:
        # Prepare context from chat history
        context = SYSTEM_CONTEXT + "\n\n"
        if chat_history:
            # Only include the last 5 messages to keep context relevant
            recent_history = list(chat_history)[-5:]
            for msg in recent_history:
                role = "Assistant" if msg.is_bot else "User"
                context += f"{role}: {msg.message}\n"
        
        # Prepare the prompt
        prompt = f"{context}User: {user_message}\nAssistant:"
        
        # Generate response with safety settings
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 1024,
            },
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "I apologize, but I couldn't generate a response at this time. Please try again."
            
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        if "429" in str(e):
            raise  # Let the retry decorator handle rate limits
        return "I apologize, but I encountered an error processing your request. Please try again in a moment." 