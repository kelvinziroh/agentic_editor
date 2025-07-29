import os
from config import *

def get_file_content(working_directory, file_path):
    try:
        # Validate that file path is within permitted working directory
        abs_wdir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if not target_path.startswith(abs_wdir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Open and read the file
        with open(target_path, "r") as file_obj:
            content = file_obj.read()
        
        if len(content) > MAX_CHARS:
            trunc_content = content[:MAX_CHARS]
            trunc_content += f'[...File "{target_path}" truncated at {MAX_CHARS} characters]'
            return trunc_content
        return content
    except Exception as e:
        return f"Error: {e}"