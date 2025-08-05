import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_function import available_functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

def main():
    # Read the gemini api key from the env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Instantiate a new Gemini client
    client = genai.Client(api_key=api_key)
    
    # Exit the program without prompt as command-line arg
    if len(sys.argv) < 2:
        print("Usage: uv run main.py \"your prompt\" [--verbose]")
        print("Example: uv run main.py \"Run tests on the calculator program\"")
        sys.exit(1)
    
    # Capture the user's prompt
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    verbose = "--verbose" in sys.argv
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    
    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    # Prompt the client instance
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT
        )
    )
    
    # Print extra information when verbose is one of the arguments
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # Return the LLM text response if no function was called
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


def call_function(function_call_part, verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    # Create dictionary mapping function names to function objects
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    function_name = function_call_part.name
    
    if function_name in function_map:
        function_call = function_map[function_name]
        args_dict = function_call_part.args.copy()
        args_dict["working_directory"] = "./calculator"
        result = function_call(**args_dict)

    
    
if __name__ == "__main__":
    main()
