import json
import os

# Define the database structures
knowledge_base = {
    "general_knowledge": {
        "what_is_ai": "Artificial Intelligence (AI) is the simulation of human intelligence by machines.",
        "what_is_machine_learning": "Machine Learning is a subset of AI that enables systems to learn from data.",
        "what_is_deep_learning": "Deep Learning is a subset of machine learning using neural networks with multiple layers.",
        "what_is_python": "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        "what_is_chatbot": "A chatbot is a software application that conducts conversations with users through text or voice."
    }
}

science_database = {
    "physics": {
        "newton_laws": {
            "first_law": "An object will remain at rest or in uniform motion unless acted upon by an external force.",
            "second_law": "Force equals mass times acceleration (F = ma).",
            "third_law": "For every action, there is an equal and opposite reaction."
        },
        "einstein_theories": {
            "special_relativity": "The laws of physics are the same for all non-accelerating observers.",
            "general_relativity": "Gravity is a consequence of the curvature of spacetime."
        }
    },
    "chemistry": {
        "periodic_table": {
            "hydrogen": "Atomic number 1, lightest element",
            "oxygen": "Atomic number 8, essential for life",
            "carbon": "Atomic number 6, basis for organic chemistry"
        },
        "chemical_bonds": {
            "covalent": "Sharing of electrons between atoms",
            "ionic": "Transfer of electrons between atoms",
            "hydrogen": "Special type of bond involving hydrogen atoms"
        }
    }
}

history_database = {
    "ancient_civilizations": {
        "egypt": {
            "period": "c. 3100 BCE - 30 BCE",
            "achievements": ["Pyramids", "Hieroglyphs", "Calendar system"],
            "notable_figures": ["Tutankhamun", "Cleopatra", "Ramesses II"]
        },
        "rome": {
            "period": "753 BCE - 476 CE",
            "achievements": ["Road systems", "Aqueducts", "Legal system"],
            "notable_figures": ["Julius Caesar", "Augustus", "Constantine"]
        }
    },
    "modern_history": {
        "industrial_revolution": {
            "period": "1760 - 1840",
            "innovations": ["Steam engine", "Factory system", "Mass production"],
            "impacts": ["Urbanization", "Economic growth", "Social change"]
        }
    }
}

technology_database = {
    "programming_languages": {
        "python": {
            "created": "1991",
            "creator": "Guido van Rossum",
            "features": ["Readable syntax", "Large standard library", "Dynamic typing"]
        },
        "javascript": {
            "created": "1995",
            "creator": "Brendan Eich",
            "features": ["Web interactivity", "Asynchronous programming", "Object-oriented"]
        }
    },
    "artificial_intelligence": {
        "machine_learning": {
            "types": ["Supervised", "Unsupervised", "Reinforcement"],
            "applications": ["Image recognition", "Natural language processing", "Recommendation systems"]
        }
    }
}

culture_database = {
    "art_movements": {
        "renaissance": {
            "period": "14th-17th centuries",
            "characteristics": ["Realism", "Perspective", "Humanism"],
            "notable_artists": ["Leonardo da Vinci", "Michelangelo", "Raphael"]
        },
        "impressionism": {
            "period": "19th century",
            "characteristics": ["Light effects", "Visible brushstrokes", "Modern subjects"],
            "notable_artists": ["Claude Monet", "Pierre-Auguste Renoir", "Edgar Degas"]
        }
    },
    "music_genres": {
        "classical": {
            "period": "1730-1820",
            "characteristics": ["Complex compositions", "Orchestral", "Formal structure"],
            "notable_composers": ["Mozart", "Beethoven", "Bach"]
        },
        "jazz": {
            "period": "Early 20th century-present",
            "characteristics": ["Improvisation", "Syncopation", "Blue notes"],
            "notable_artists": ["Louis Armstrong", "Miles Davis", "Duke Ellington"]
        }
    }
}

greeting_database = {
    "greetings": {
        "casual": [
            "Hey!",
            "Hi there!",
            "What's up?",
            "Yo!",
            "Hello!"
        ],
        "formal": [
            "Good day!",
            "Greetings!",
            "How do you do?",
            "It is a pleasure to meet you."
        ],
        "morning": [
            "Good morning!",
            "Rise and shine!",
            "Morning! Have a great day ahead.",
            "Wishing you a bright and cheerful morning!"
        ],
        "evening": [
            "Good evening!",
            "Hope you had a great day.",
            "Evening! Relax and enjoy your night."
        ],
        "farewell": [
            "Goodbye!",
            "See you later!",
            "Take care!",
            "Farewell, my friend.",
            "Catch you soon!"
        ],
        "languages": {
            "english": "Hello!",
            "spanish": "¡Hola!",
            "french": "Bonjour!",
            "german": "Hallo!",
            "italian": "Ciao!",
            "japanese": "こんにちは (Konnichiwa)",
            "chinese": "你好 (Nǐ hǎo)",
            "hindi": "नमस्ते (Namaste)"
        }
    }
}


# Function to save database to JSON file
def save_database(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Successfully created {filename}")
    except Exception as e:
        print(f"Error creating {filename}: {e}")

# Create database directory if it doesn't exist
os.makedirs('databases', exist_ok=True)

# Save all databases
databases = {
    'knowledge_base.json': knowledge_base,
    'science_database.json': science_database,
    'history_database.json': history_database,
    'technology_database.json': technology_database,
    'culture_database.json': culture_database,
    'greeting_database.json': greeting_database
}

for filename, data in databases.items():
    filepath = os.path.join('databases', filename)
    save_database(data, filepath)

print("\nAll database files have been created in the 'databases' directory.")