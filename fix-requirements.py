import re

def remove_after_delimiter(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        modified_lines = [re.sub(r'==.*$', '', line) for line in lines]

        with open(file_path, 'w') as file:
            file.writelines(modified_lines)

        print("Lines after '==' delimiter removed successfully.")
    except Exception as e:
        print("An error occurred:", e)

# Replace 'input.txt' with the path to your text file
remove_after_delimiter('requirements.txt')
