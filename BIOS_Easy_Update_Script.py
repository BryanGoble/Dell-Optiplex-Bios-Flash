# Big thanks to ChatGPT for helping me save some time writing this script

import os

def read_characters_from_offset(file_path, start_offset, end_offset):
    """
    Reads characters from the specified offset range in the binary file.
    """
    with open(file_path, 'rb') as file:
        file.seek(start_offset)
        data = file.read(end_offset - start_offset + 1)
        characters = ''.join(chr(byte) for byte in data)
        return characters

def update_characters(file_path, start_offset, new_characters):
    """
    Updates characters at the specified offset range in the binary file.
    """
    with open(file_path, 'r+b') as file:
        file.seek(start_offset)
        file.write(new_characters.encode('utf-8'))

if __name__ == "__main__":
    # Get the file path from the user input and strip quotes if present
    file_path = input(r"Enter the path to the binary file: ").strip('"')
    
    # Check if the provided path is a valid file
    if not os.path.isfile(file_path):
        print("Invalid file path.")
    else:
        start_offset = 0x0078002A
        end_offset = 0x00780030  # Adjusted end offset
        
        # Read characters from the specified offset range
        characters = read_characters_from_offset(file_path, start_offset, end_offset)
        print("Characters found in the specified hex offset range:")
        print(characters)
        
        # Prompt user for new characters and update the file if provided
        user_input = input("Press Enter to proceed without changes, or enter new 7 alphanumeric characters: ")
        if user_input:
            if len(user_input) != 7:
                print("Please enter exactly 7 characters.")
            elif not user_input.isalnum():
                print("Please enter only alphanumeric characters.")
            else:
                update_characters(file_path, start_offset, user_input)
                print("File updated with new characters.")
        else:
            print("No changes made.")