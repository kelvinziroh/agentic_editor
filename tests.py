# Import function
from functions.get_file_content import get_file_content

# Define the test cases 
test_cases = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py")
]

def test(input1, input2):
    # Handle output for files
    print(f"Result for '{input2}' file:")
    
    # Handle the result output for valid and invalid inputs
    result = get_file_content(input1, input2)
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