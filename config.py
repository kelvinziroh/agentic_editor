from google.genai import types

# client code attributes
MAX_CHARS=10000

# model attributes
MODEL_NAME="gemini-2.0-flash-001"
SYSTEM_PROMPT="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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
            ),
        },
    ),
)

SCHEMA_GET_FILE_CONTENT = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specified file path to the file to read content from.",
            ),
        },
    ),
)

SCHEMA_RUN_PYTHON_FILE = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python files in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specified file path to the python file that should be run.",
            ),
            # "args": types.Schema(
            #     type=types.Type.STRING,
            #     description="The directory to list files from, relative to the working directory. If not provided, lists in the working directory itself.",
            # ),
        },
    ),
)

SCHEMA_WRITE_FILE = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content to the specified file at the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The specified file path with the file to write the contents to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to be written or added into the file at the specified file path.",
            ),
        },
    ),
)

AVAILABLE_FUNCTIONS = types.Tool(
    function_declarations=[
        SCHEMA_GET_FILES_INFO,
        SCHEMA_GET_FILE_CONTENT,
        SCHEMA_RUN_PYTHON_FILE,
        SCHEMA_WRITE_FILE
    ]
)