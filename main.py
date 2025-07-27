import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # Exit the program without prompt as command-line arg
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <prompt> [--verbose]")
        sys.exit(1)
    
    # Capture the user's prompt
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    # Read the gemini api key from the env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Instantiate a new Gemini client
    client = genai.Client(api_key=api_key)

    # Prompt the client instance
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )            
    
    # Displaly optional content based on command-line arguments
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            print(f"{response.text}\n")
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(f"{response.text}")

if __name__ == "__main__":
    main()
