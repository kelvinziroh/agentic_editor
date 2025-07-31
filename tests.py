# Import function
from functions.run_python import run_python_file

# Define the test cases 
test_cases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py")
]

def test(input1, input2, input3=[]):
    # Handle output for files
    print(f"Result for '{input2}' file:")
    
    # Handle the result output for valid and invalid inputs
    result = run_python_file(input1, input2, input3)
    if result.startswith("Error"):
        print(f"\t{result}")
    else:
        print(result)       

def main():
    # Run the test cases
    for test_case in test_cases:
        test(*test_case)
        print("\n")
    
if __name__ == "__main__":
    main()