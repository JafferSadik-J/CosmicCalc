import os
import json
import logging
from flask import request, jsonify, render_template
from app import app
from openai import OpenAI

# Set up OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests to OpenAI API."""
    try:
        data = request.json
        user_message = data.get('message', '')
        message_history = data.get('history', [])
        
        # Create messages array for OpenAI
        messages = [
            {"role": "system", "content": "You are an educational assistant focused exclusively on astronomy and our solar system. "
                                         "Provide accurate, informative, and engaging responses about planets, moons, the sun, "
                                         "asteroids, comets, and other objects within our solar system. "
                                         "Include interesting facts and educational content in your responses. "
                                         "If asked about topics outside of astronomy and our solar system, politely explain that "
                                         "you can only provide information about astronomy and our solar system, and suggest they "
                                         "ask an astronomy-related question instead. "
                                         "Your responses should be educational and suitable for all ages."}
        ]
        
        # Add message history
        for msg in message_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        ai_response = response.choices[0].message.content
        
        return jsonify({
            "response": ai_response,
            "success": True
        })
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            "response": "I'm sorry, but I encountered an error while processing your request. Please try again later.",
            "success": False,
            "error": str(e)
        }), 500