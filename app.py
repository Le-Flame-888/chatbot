from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from ultimate_chatbot import UltimateChatbot

app = Flask(__name__)
CORS(app)  # This is important for handling the requests

# Initialize the chatbot
chatbot = UltimateChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Simple response logic
        if any(word in message.lower() for word in ['hello', 'hi', 'hey']):
            response = "Hello! How can I help you today?"
        else:
            response = f"You said: {message}. How can I assist you with that?"

        response = chatbot.process_input(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)