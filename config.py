from google.genai import types
from functions.get_files_info import get_files_info

# client code attributes
MAX_CHARS=10000

# model attributes
MODEL_NAME="gemini-2.0-flash-001"
SYSTEM_PROMPT="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# create a list of all available functions
SCHEMA_GET_FILES_INFO = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists in the working directory itself.",
            )
        },
    ),
)

AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        SCHEMA_GET_FILES_INFO,
    ]
)