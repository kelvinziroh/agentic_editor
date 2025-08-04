import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        # Validate if file path is in permitted working directory
        abs_wdir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if not target_path.startswith(abs_wdir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_path):
            new_dir = "/".join(target_path.split("/")[:-1])
            os.makedirs(new_dir, exist_ok=True)
        
        with open(target_path, "w") as file_obj:
            file_obj.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration(
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
