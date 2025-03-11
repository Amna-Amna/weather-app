import os
from openai import OpenAI
from django.conf import settings

def create_openai_client():
    """
    Create and return an initialized OpenAI client using the API key
    from Django settings or environment variables.
    """
    api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
    
    if not api_key:
        raise ValueError("OpenAI API key not found in settings or environment variables")
    
    return OpenAI(api_key=api_key) 