import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    
    try:
        # Validate if the file path is within permited working directory
        abs_wdir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))
        
        if not target_path.startswith(abs_wdir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        if not os.path.exists(target_path):
            return f'Error: File "{file_path}" not found.'
        if not target_path.endswith(".py"):
            return f'Error: "{file_path} is not a python file.'
        
        # Run python file
        result = subprocess.run(
            ["python", f"{target_path}"] + args, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        # Capture the ouput components
        stdout = f'STDOUT: {result.stdout}'
        stderr = f'STDERR: {result.stderr}'
        code = result.returncode
        
        # Configure the output
        output = stdout + '\n' + stderr
        if code != 0:
            return output + f'\nProcess exited with code {code}'
        if not stdout and not stderr:
            return "No ouput produced."
        return output
    
    except Exception as e:
        return f'Error: executing Python file: {e}'