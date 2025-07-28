# Import function
from functions.get_files_info import get_files_info

# Define the test cases 
test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../")
]

def test(input1, input2):
    # Handle output for current and other directories
    if input2 == ".":
        print(f"Result for current directory")
    else:
        print(f"Result for '{input2}' directory")
    
    # Handle the result output for valid and invalid ouputs
    result = get_files_info(input1, input2)
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