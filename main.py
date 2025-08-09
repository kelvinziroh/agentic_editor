import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_function import available_functions, call_function

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
    
    # Allow model to iteratively call functions and cap the no. of iterations
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")
        

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
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
    
    # Return the LLM text response if no function was called
    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:    
        function_call_result = call_function(function_call_part, verbose)
        
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    
    messages.append(types.Content(role="tool", parts=function_responses))
   
    
if __name__ == "__main__":
    main()
