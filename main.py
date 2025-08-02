import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file


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
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[AVAILABLE_FUNCTIONS],
            system_instruction=SYSTEM_PROMPT
        )
    )            
    
    # Set metadata string
    metadata_str = f"""
    User prompt: '{user_prompt}'\n
    Prompt tokens: {response.usage_metadata.prompt_token_count}\n
    Response tokens: {response.usage_metadata.candidates_token_count}
    """
    
    # Check if there were any function calls
    function_calls = response.function_calls
    
    # Displaly optional content based on command-line arguments
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        if function_calls:
            print(f"Calling function: {function_calls[0].name}({function_calls[0].args})\n")
            print(metadata_str)
        else:
            print(f"{response.text}\n")
            print(metadata_str)
    else:
        if function_calls:
            print(f"Calling function: {function_calls[0].name}({function_calls[0].args})\n")
        else:
            print(f"{response.text}")

if __name__ == "__main__":
    main()
