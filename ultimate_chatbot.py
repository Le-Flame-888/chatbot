from datetime import datetime
import json
import logging
import os
from typing import Dict, List, Optional
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import wikipedia
import wolframalpha
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, BertForTokenClassification
from langdetect import detect
import warnings
import random

warnings.filterwarnings('ignore')
    
class UltimateChatbot:
    def __init__(self):
        """
        Initialize the UltimateChatbot with necessary components and configurations.
        """
        self.name = "UltimateBot"
        # Ensure NLTK data is downloaded
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')

        self.setup_logging()
        self.setup_components()
        self.conversation_history: List[Dict] = []
        self.knowledge_base: Dict = self.load_knowledge_base()
        
        # Expanded greeting patterns
        self.greeting_patterns = [
            # Basic greetings
            'hello', 'hi', 'hey', 'greetings', 'howdy', 'yo', 'hiya', 
            # Time-specific greetings
            'good morning', 'good afternoon', 'good evening', 'good day',
            # Casual greetings
            'what\'s up', 'sup', 'how\'s it going', 'how are you',
            # Welcome back patterns
            'im back', 'i\'m back', 'back again',
            # Formal greetings
            'pleased to meet you', 'nice to meet you', 'pleasure to meet you',
            # Other variations
            'hi there', 'hello there', 'heya', 'aloha', 'bonjour', 'hola'
        ]
        
        # Expanded greeting responses
        self.greeting_responses = [
            # Friendly greetings
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "Hey! Great to see you. What's on your mind?",
            "Greetings! How may I assist you?",
            "Hello! I'm here to help. What do you need?",
            
            # Casual responses
            "Hey there! Ready to help with whatever you need!",
            "Hi! Always good to chat. What's up?",
            "Hello! Looking forward to our conversation!",
            
            # Welcoming responses
            "Welcome! How can I make your day better?",
            "Great to see you! What shall we work on?",
            "Hello! I'm excited to help you today!",
            
            # Professional responses
            "Greetings! How may I be of assistance today?",
            "Hello! I'm at your service. What can I help you with?",
            "Hi there! Ready to tackle any questions you might have!"
        ]

    def get_time_specific_greeting(self) -> str:
        """Return a time-appropriate greeting based on the current hour."""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good morning! How can I help you today?"
        elif 12 <= hour < 17:
            return "Good afternoon! What can I do for you?"
        elif 17 <= hour < 22:
            return "Good evening! How may I assist you?"
        else:
            return "Hello! How can I help you at this hour?"

    def is_greeting(self, text: str) -> bool:
        """
        Check if the input text is a greeting.
        Now handles more complex greeting patterns.
        """
        text_lower = text.lower()
        # Direct pattern matching
        if any(pattern in text_lower for pattern in self.greeting_patterns):
            return True
        
        # Check for question-style greetings
        question_greetings = [
            "how are you",
            "how're you",
            "how you doing",
            "how do you do",
            "what's new",
            "what's going on"
        ]
        if any(pattern in text_lower for pattern in question_greetings):
            return True
            
        return False

    def get_greeting_response(self) -> str:
        """
        Return an appropriate greeting response.
        Now includes time-specific responses.
        """
        responses = self.greeting_responses.copy()
        # Always include a time-specific greeting in the possible responses
        responses.append(self.get_time_specific_greeting())
        return random.choice(responses)

    def process_input(self, user_input: str) -> str:
        """Process user input and generate response."""
        try:
            # Check for greeting first
            if self.is_greeting(user_input):
                response = self.get_greeting_response()
            else:
                # Extract named entities
                entities = self.extract_entities(user_input)

                # Get sentiment
                sentiment = self.sentiment_analyzer.polarity_scores(user_input)

                # Process input
                response = self.get_answer(user_input)

            # Save conversation
            self.conversation_history.append({
                'user_input': user_input,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            return response
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            return "I encountered an error processing your request. Please try again."

    # ... [rest of the class implementation remains the same]
    def setup_logging(self):
        """Configure logging for the chatbot."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('chatbot.log'),
                logging.StreamHandler()
            ]
        )

    def setup_components(self):
        """Initialize AI components with error handling."""
        logging.info("Initializing AI components...")
        try:
            self.qa_model = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')
            self.generator = pipeline('text-generation', model='gpt2')
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.ner_model = pipeline('ner', model='dslim/bert-base-NER')
            logging.info("AI components initialized successfully!")
        except Exception as e:
            logging.error(f"Error initializing AI components: {e}")
            raise

    def load_knowledge_base(self) -> Dict:
        """Load the knowledge base from file or return empty structure."""
        try:
            with open("knowledge_base.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"general_knowledge": {}}

    def load_all_resources(self):
        """Load all necessary resources and setup embeddings."""
        self.load_subject_databases()
        self.setup_embeddings()

    def setup_embeddings(self):
        """Initialize and create TF-IDF embeddings for the knowledge base."""
        self.vectorizer = TfidfVectorizer()
        texts = list(self.knowledge_base.get("general_knowledge", {}).keys())
        if texts:
            try:
                self.embeddings = self.vectorizer.fit_transform(texts)
            except Exception as e:
                logging.error(f"Error creating embeddings: {e}")
                self.embeddings = None

    def load_subject_databases(self):
        """Load subject-specific databases with error handling."""
        self.subject_data = {}
        database_files = {
            "science": "science_database.json",
            "history": "history_database.json",
            "technology": "technology_database.json",
            "culture": "culture_database.json"
        }

        for subject, filename in database_files.items():
            self.subject_data[subject] = self.load_json_data(filename)

    def load_json_data(self, filename: str) -> Dict:
        """Load JSON data from file with error handling."""
        try:
            filepath = os.path.join('databases', filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning(f"Database file not found: {filename}")
            return {}
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in file: {filename}")
            return {}

    def get_answer(self, question: str) -> str:
        """Get answer using Wikipedia."""
        try:
            wiki_response = wikipedia.summary(question, sentences=3)
            return wiki_response
        except Exception as e:
            logging.error(f"Error getting answer: {e}")
            return "I couldn't find a specific answer to your query. Try rephrasing or asking something else."

    def process_input(self, user_input: str) -> str:
        """Process user input and generate response."""
        try:
            # Extract named entities
            entities = self.extract_entities(user_input)

            # Get sentiment
            sentiment = self.sentiment_analyzer.polarity_scores(user_input)

            # Process input
            answer = self.get_answer(user_input)

            # Save conversation
            self.conversation_history.append({
                'user_input': user_input,
                'entities': entities,
                'sentiment': sentiment,
                'response': answer,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            return answer
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            return "I encountered an error processing your request. Please try again."

    def extract_entities(self, text: str) -> List:
        """Extract named entities from text."""
        try:
            return self.ner_model(text)
        except Exception as e:
            logging.error(f"NER error: {e}")
            return []

    def save_conversation(self):
        """Save conversation history to file with error handling."""
        try:
            with open("conversation_history.json", "w", encoding="utf-8") as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=4)
            logging.info("Conversation saved successfully!")
        except Exception as e:
            logging.error(f"Error saving conversation: {e}")

def main():
    """Main function to run the chatbot."""
    logging.info("Initializing UltimateBot...")

    try:
        chatbot = UltimateChatbot(wolfram_app_id=os.getenv("WOLFRAM_API_KEY", "YOUR_WOLFRAM_ALPHA_ID"))
    except Exception as e:
        logging.error(f"Failed to initialize chatbot: {e}")
        return

    print("\nUltimateBot: Hello! I'm your AI assistant. I can:")
    print("- Answer questions on various topics")
    print("- Perform sentiment analysis")
    print("- Extract named entities")
    print("- Generate creative responses")
    print("- Respond to greetings with context-aware responses")
    print("\nType 'bye' to exit.")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'bye':
                print("\nUltimateBot: Goodbye! Saving our conversation...")
                chatbot.save_conversation()
                break

            if user_input:
                response = chatbot.process_input(user_input)
                print("\nUltimateBot:", response)

    except KeyboardInterrupt:
        print("\nUltimateBot: Saving conversation and shutting down...")
        chatbot.save_conversation()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print("\nUltimateBot: An unexpected error occurred. Saving conversation and shutting down...")
        chatbot.save_conversation()

if __name__ == "__main__":
    main()