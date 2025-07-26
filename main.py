import os
from dotenv import load_dotenv
from google import genai


def main():
    # Read the gemini api key from the env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Instantiate a new Gemini client
    client = genai.Client(api_key=api_key)

    # Prompt the client instance
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents="How does the number 42 relate to Douglas Adam's Hitchhikers Guide to the Galaxy Sci-fi novel?"
    )            
    
    print(f"{response.text}\n")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
