import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        # validate if the directory is in working directory
        abs_wdir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))
        
        if not target_path.startswith(abs_wdir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        
        # Get the list of directory contents
        dir_contents = []
        for content in os.listdir(target_path):
            content_path = os.path.join(target_path, content)
            dir_contents.append(f"- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}")
        
        return "\n".join(dir_contents)
    
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
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