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
    
    # Iteratively call the generate content function 20 times
    try:
        for i in range(20):
            generated_response = generate_content(client, messages, verbose)
            if generated_response:
                print(generated_response)
                break
    except Exception as e:
        print(f"Error: {e}")
        


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
    
    # Add list of response variations to the messages
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    # Return the LLM text response if no function was called
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:    
        function_call_result = call_function(function_call_part, verbose)
        
        function_call_message = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result":f"{function_call_result}"}
                )  
            ],
        )
        
        messages.append(function_call_message)
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception(f"error: {function_call_part.name} did not execute as intended.")
    
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


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
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    if function_name in function_map:
        function_call = function_map[function_name]
        args_dict = function_call_part.args.copy()
        args_dict["working_directory"] = "./calculator"
        function_result = function_call(**args_dict)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
   
    
if __name__ == "__main__":
    main()
