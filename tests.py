# Import function
from functions.write_file import write_file

# Define the test cases 
test_cases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed")
]

def test(input1, input2, input3):
    # Handle output for files
    print(f"Result for '{input2}' file:")
    
    # Handle the result output for valid and invalid inputs
    result = write_file(input1, input2, input3)
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