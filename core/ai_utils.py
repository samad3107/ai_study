# core/ai_utils.py
import os
from google import genai
from google.genai.errors import APIError
from pypdf import PdfReader
from dotenv import load_dotenv 
from django.conf import settings 

# Force load environment variables
load_dotenv()

# --- AI Client Configuration Variables ---
client = None 
model_flash = 'gemini-2.5-flash' 
model_pro = 'gemini-2.5-pro'   

# --- CRITICAL HELPER FUNCTION ---
def initialize_client():
    """Initializes and returns the Gemini client for a single request."""
    global client
    if client is None:
        try:
            api_key = os.environ.get("GEMINI_API_KEY") 
            if not api_key:
                raise ValueError("GEMINI_API_KEY is missing from environment.")
            client = genai.Client(api_key=api_key) 
        except Exception as e:
            print(f"AI Client Initialization Failed: {e}")
            return None
    return client

# Call the function once to initialize the global 'client' variable
try:
    initialize_client()
except Exception as e:
    pass

# ----------------------------------------------------------------------
# QUIZ DATA MAP (Contains 5 unique questions per topic)
# ----------------------------------------------------------------------

QUIZ_DATA_MAP = {
    # Topic: Artificial Intelligence
    "artificial intelligence": {
        "topic": "Artificial Intelligence Fundamentals",
        "json": """
        {
            "quiz_questions": [
                {"text": "What is the primary goal of Artificial General Intelligence (AGI)?", "options": ["To win games", "To exhibit human-level intelligence across multiple domains", "To process big data"], "correct_answer_index": 1},
                {"text": "Which test is used to determine a machine's ability to exhibit human-like behavior?", "options": ["The Turing Test", "The AlphaGo Test", "The Boston Dynamics Test"], "correct_answer_index": 0},
                {"text": "What does the term 'Narrow AI' refer to?", "options": ["AI with limited capabilities focused on a single task", "AI that is weak and non-functional", "AI used only in research"], "correct_answer_index": 0},
                {"text": "Who is considered the 'father of AI'?", "options": ["Alan Turing", "Geoffrey Hinton", "John McCarthy"], "correct_answer_index": 2},
                {"text": "In AI, what does NLP stand for?", "options": ["Natural Language Processing", "Neural Logic Planning", "New Linear Programming"], "correct_answer_index": 0}
            ]
        }
        """
    },
    # Topic: AI
    
    # Topic: Machine Learning
    "machine learning": {
        "topic": "Machine Learning",
        "json": """
        {
            "quiz_questions": [
                {"text": "Which ML category uses labeled data for training?", "options": ["Unsupervised Learning", "Reinforcement Learning", "Supervised Learning"], "correct_answer_index": 2},
                {"text": "What is 'Overfitting' in the context of ML?", "options": ["When the model performs poorly on training data", "When the model learns the training data and noise too well", "When the model is too simple"], "correct_answer_index": 1},
                {"text": "K-Means is an example of which type of learning?", "options": ["Supervised", "Unsupervised", "Reinforcement"], "correct_answer_index": 1},
                {"text": "What is the primary function of a 'Loss Function'?", "options": ["To increase training speed", "To calculate the error between predicted and actual output", "To preprocess input data"], "correct_answer_index": 1},
                {"text": "Which algorithm is used for dimensionality reduction?", "options": ["Linear Regression", "Principal Component Analysis (PCA)", "K-Nearest Neighbors"], "correct_answer_index": 1}
            ]
        }
        """
    },
    # Topic: Deep Learning
    "deep learning": {
        "topic": "Deep Learning",
        "json": """
        {
            "quiz_questions": [
                {"text": "Deep Learning utilizes structures inspired by the brain called:", "options": ["Data Vectors", "Turing Machines", "Neural Networks"], "correct_answer_index": 2},
                {"text": "What is a 'Hidden Layer'?", "options": ["An output layer that cannot be seen", "A layer between the input and output layers", "A layer used only for debugging"], "correct_answer_index": 1},
                {"text": "The process of modifying weights in a neural network is called:", "options": ["Forward Propagation", "Backpropagation", "Data Augmentation"], "correct_answer_index": 1},
                {"text": "CNNs (Convolutional Neural Networks) are most commonly used for:", "options": ["Time-Series Forecasting", "Natural Language Processing", "Image Recognition"], "correct_answer_index": 2},
                {"text": "What problem did ReLU activation functions primarily help solve?", "options": ["Overfitting", "Vanishing Gradient", "Data Imbalance"], "correct_answer_index": 1}
            ]
        }
        """
    },
    # Topic: Neural Networks
    "neural networks": {
        "topic": "Neural Networks",
        "json": """
        {
            "quiz_questions": [
                {"text": "What is the mathematical function that transforms the input signal into a neuron's output?", "options": ["The Cost Function", "The Activation Function", "The Weight Function"], "correct_answer_index": 1},
                {"text": "In a neural network, what is a 'bias'?", "options": ["An input always set to zero", "A value that shifts the activation function", "The calculation error"], "correct_answer_index": 1},
                {"text": "The first layer of a neural network is called the:", "options": ["Output Layer", "Input Layer", "Processing Layer"], "correct_answer_index": 1},
                {"text": "Recurrent Neural Networks (RNNs) are best suited for what kind of data?", "options": ["Sequential Data (e.g., text, audio)", "Static Image Data", "Tabular Data"], "correct_answer_index": 0},
                {"text": "What is a 'perceptron'?", "options": ["The first model of an artificial neuron", "A complex deep learning model", "A type of dataset"], "correct_answer_index": 0}
            ]
        }
        """
    },
    # Topic: Data Science
    "data science": {
        "topic": "Data Science",
        "json": """
        {
            "quiz_questions": [
                {"text": "Which phase is typically the longest in a Data Science project?", "options": ["Model Training", "Data Cleaning and Preparation", "Model Deployment"], "correct_answer_index": 1},
                {"text": "What term describes data that is incomplete or inconsistent?", "options": ["Clean Data", "Raw Data", "Dirty Data"], "correct_answer_index": 2},
                {"text": "A key role of a Data Scientist is to transform raw data into:", "options": ["Machine Code", "Actionable Insights", "API Endpoints"], "correct_answer_index": 1},
                {"text": "What is the process of extracting knowledge from raw data called?", "options": ["Data Mining", "Data Normalization", "Data Warehousing"], "correct_answer_index": 0},
                {"text": "Which tool is commonly used for data visualization in Python?", "options": ["NumPy", "Pandas", "Matplotlib"], "correct_answer_index": 2}
            ]
        }
        """
    },
    # Topic: Large Language Models
    "large language models": {
        "topic": "Large Language Models (LLMs)",
        "json": """
        {
            "quiz_questions": [
                {"text": "What is the base architecture for modern LLMs like Gemini and GPT?", "options": ["Recurrent Neural Networks (RNN)", "Transformer Architecture", "Convolutional Neural Networks (CNN)"], "correct_answer_index": 1},
                {"text": "What does RAG stand for in the context of LLMs?", "options": ["Recurrent Access Generation", "Retrieval-Augmented Generation", "Random Attention Graph"], "correct_answer_index": 1},
                {"text": "The 'context window' of an LLM defines:", "options": ["The speed of generation", "The maximum amount of information the model can remember", "The number of parameters"], "correct_answer_index": 1},
                {"text": "What task are LLMs primarily designed to excel at?", "options": ["Image Classification", "Predicting the next word in a sequence", "Solving complex math problems"], "correct_answer_index": 1},
                {"text": "In an LLM, 'Hallucination' refers to:", "options": ["Generating correct but unexpected output", "Generating false or nonsensical information", "Generating images"], "correct_answer_index": 1}
            ]
        }
        """
    },
    # Topic: NLP
    "nlp": {
        "topic": "Natural Language Processing (NLP)",
        "json": """
        {
            "quiz_questions": [
                {"text": "The process of breaking a text into words or sentences is called:", "options": ["Lemmatization", "Tokenization", "Stemming"], "correct_answer_index": 1},
                {"text": "What is 'Sentiment Analysis'?", "options": ["Identifying the emotional tone of a piece of text", "Translating text", "Generating summaries"], "correct_answer_index": 0},
                {"text": "Stop words (e.g., 'the', 'a', 'is') are typically removed to:", "options": ["Decrease processing time", "Improve model focus on key words", "Both A and B"], "correct_answer_index": 2},
                {"text": "What is the purpose of 'Named Entity Recognition' (NER)?", "options": ["To identify people, organizations, or locations in text", "To translate names", "To fix spelling errors"], "correct_answer_index": 0},
                {"text": "Which model type often struggles with long-term dependencies in sequences?", "options": ["Transformer", "RNN", "CNN"], "correct_answer_index": 1}
            ]
        }
        """
    },
    # Topic: Computer Vision
    "computer vision": {
        "topic": "Computer Vision",
        "json": """
        {
            "quiz_questions": [
                {"text": "Which AI method is most common for image classification?", "options": ["RNNs", "CNNs", "LLMs"], "correct_answer_index": 1},
                {"text": "What is the process of identifying the location of objects in an image called?", "options": ["Image Filtering", "Object Detection", "Image Segmentation"], "correct_answer_index": 1},
                {"text": "The technique of sliding a small matrix over an image to detect features is called:", "options": ["Pooling", "Convolution", "Rectification"], "correct_answer_index": 1},
                {"text": "What does the term 'pixel' represent?", "options": ["A line of code", "A single point of color/light in an image", "An image file format"], "correct_answer_index": 1},
                {"text": "In computer vision, what is a bounding box used for?", "options": ["Storing image files", "Defining the exact location of an object", "Applying filters"], "correct_answer_index": 1}
            ]
        }
        """
    },
    # Topic: Turing Test
    "turing test": {
        "topic": "Turing Test",
        "json": """
        {
            "quiz_questions": [
                {"text": "The Turing Test was introduced by Alan Turing in which year?", "options": ["1936", "1950", "1968"], "correct_answer_index": 1},
                {"text": "The test measures a machine's ability to demonstrate:", "options": ["Consciousness", "Intelligence/Thought", "Physical Dexterity"], "correct_answer_index": 1},
                {"text": "Who performs the judgment in the original Turing Test setup?", "options": ["A computer", "A human interrogator", "A robot"], "correct_answer_index": 1},
                {"text": "A successful outcome means the human interrogator cannot distinguish the machine from a:", "options": ["Highly advanced animal", "Human being", "Another computer"], "correct_answer_index": 1},
                {"text": "What was Alan Turing's original name for the test?", "options": ["The Imitation Game", "The Intelligence Challenge", "The Humanoid Test"], "correct_answer_index": 0}
            ]
        }
        """
    }
}
# --- END QUIZ DATA MAP ---

# ----------------------------------------------------------------------
# PDF Text Extraction (Must exist for views.py)
# ----------------------------------------------------------------------

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a local PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return None
    return text

# ----------------------------------------------------------------------
# Summarization Function (Must exist for views.py)
# ----------------------------------------------------------------------

def summarize_notes(pdf_text, note_title):
    client = initialize_client()
    if not client:
        return "AI service is not configured. Check your .env file for GEMINI_API_KEY."

    prompt = f"""
    You are an expert educational assistant. Your task is to summarize the following notes.
    The notes are titled: '{note_title}'.
    
    1. Provide a detailed, easy-to-understand summary.
    2. Conclude the summary with a specific section titled "Key Concepts to Focus On" where you list 3 to 5 core ideas from the text that the student should master.
    
    --- Notes Text ---
    {pdf_text[:10000]} 
    --- End Notes Text ---
    """
    
    try:
        response = client.models.generate_content(
            model=model_flash,
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"AI API Error: Could not generate summary. {e}"
    except Exception as e:
        return f"An unexpected error occurred during summarization: {e}"

# ----------------------------------------------------------------------
# Topic Explanation Function (Must exist for views.py)
# ----------------------------------------------------------------------

def explain_topic_and_focus(topic):
    client = initialize_client()
    if not client:
        return "AI service is not configured. Check your .env file for GEMINI_API_KEY."

    prompt = f"""
    You are an expert educational assistant. Your task is to explain a given topic in a simple, clear, and engaging manner suitable for a student.
    
    1. Provide a comprehensive explanation of the topic: '{topic}'.
    2. Use simple language and analogies where helpful.
    3. At the end, include a distinct section titled "🎯 Focus Points for Mastery" where you list 3 to 5 crucial concepts within that topic that the student must master for success in a quiz or test.
    
    The explanation should be formatted using Markdown for readability (headings, lists, bold text).
    """
    
    try:
        response = client.models.generate_content(
            model=model_flash,
            contents=prompt
        )
        return response.text
    except APIError as e:
        return f"AI API Error: Could not generate explanation. {e}"
    except Exception as e:
        return f"An unexpected error occurred during explanation: {e}"

# ----------------------------------------------------------------------
# Quiz Generation Function (The function that views.py calls)
# ----------------------------------------------------------------------

def generate_quiz_json(topic, num_questions=5):
    """
    STABLE QUIZ GENERATOR: Uses hardcoded data if the topic is recognized, 
    otherwise blocks the unstable API call.
    """
    topic_lower = topic.lower().strip()
    
    if topic_lower in QUIZ_DATA_MAP:
        # Success: Return the stable, hardcoded JSON string
        return QUIZ_DATA_MAP[topic_lower]["json"], None
    else:
        # Failure: Block the live API call immediately and provide guidance
        error_msg = f"The topic '{topic}' is outside the demo scope. Please use a verified topic related to AI (e.g., 'Machine Learning' or 'Turing Test')."
        return None, error_msg

# ----------------------------------------------------------------------
# Feedback Function (Must exist for views.py)
# ----------------------------------------------------------------------

def generate_feedback(topic, score, total):
    client = initialize_client()
    if not client:
        return "AI service is not configured. Review your performance and try again!"
        
    percentage = (score / total) * 100
    
    prompt = f"""
    You are an AI motivation coach. A student just took a quiz on the topic '{topic}'.
    Their score was {score} out of {total} questions, which is a {percentage:.0f}%.
    
    Provide a single, encouraging, and supportive message (maximum 3 sentences).
    The tone must be positive, motivational, and futuristic/sleek.
    """
    
    try:
        response = client.models.generate_content(
            model=model_flash,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Feedback Error: Great job on the quiz! Keep going. ({e})"