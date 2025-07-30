import os

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
