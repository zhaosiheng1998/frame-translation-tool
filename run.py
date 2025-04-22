"""
Frame-based English-Japanese Translation Tool Startup Script
"""
import os
from dotenv import load_dotenv
from backend.app import app

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Ensure Frame file exists
    if not os.path.exists('commerce-buy-frame.json'):
        print("Warning: Default Frame file commerce-buy-frame.json does not exist")
    
    # Check API keys
    if 'DEEPSEEK_API_KEY' not in os.environ:
        print("Warning: DEEPSEEK_API_KEY environment variable is not set")
        print("Please set the DEEPSEEK_API_KEY in your .env file")
    
    # Start application
    print("Starting Frame-based English-Japanese Translation Tool...")
    print("Access http://localhost:5000 to use the application")
    app.run(debug=True, port=5000)
