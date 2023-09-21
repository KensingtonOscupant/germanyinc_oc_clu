import csv
import sys
import termios
import tty
import os
import pyperclip

def getch():
    """Get a single character from the user without the need to press enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def translate_entity():
    if row["legal_type"] == 0:
        return "natural person"
    elif row["legal_type"] == 1.0:
        return "legal entity"

# Prompt the user for the data file path
data_file_path = input("Enter the path to the project folder (e.g. /Users/gisbertgurke/Documents/Projekte/germanyinc_oc_clu/build/exe.macosx-10.9-universal2-3.10 ): ")

os.chdir(data_file_path)

# Open the CSV file and read the data
csv_file = "df_cleaned.csv"  # Replace with your CSV file path
with open(csv_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

# Initialize a variable to store the next unique ID
next_id = 1

# Print a welcome message
print("Welcome to the company data utility!")
print("Press 'a' to classify the notfying party as a natural person.")
print("Press 'd' to classify the notfying party as a legal entity.")
print("Press 'b' to go back to the previous question.")
print("Press 'q' to quit the utility.")

# Keep track of the current question index
current_index = 0

# Find the first empty company_id
for i, row in enumerate(data):
    if row["legal_type"] == "":
        current_index = i
        break

while current_index < len(data):
    row = data[current_index]
    notifying_party = row["notifying_party"]
    legal_type = row["legal_type"]
    open_corporates_url = row["OpenCorporates URL"]

    # Print a newline for spacing
    print("\n")

    # Print the notifying party and ask the user for input
    print(f"Notifying Party: {notifying_party}")
    print(f"Legal Type: {translate_entity()}")
    print(f"OpenCorporates URL: {open_corporates_url}")
    print("Press 'a' to classify as a natural person, 'd' to classify as a legal entity, or 'b' to go back to the previous question:")

    while True:
        user_input = getch().lower()
        if user_input in ["a", "d", "1", "\n"]:
            break
        elif user_input == "b":
            if current_index > 0:
                current_index -= 2
                break
            else:
                print("Cannot go back, already at the first question.")
        elif user_input == "q":
            sys.exit("Exit the script")
        else:
            print("Invalid input. Please enter 'a', 'd', or 'q'")

    # Update the 'legal_type' based on the user input
    if user_input == "a":
        row["legal_type"] = 0
    elif user_input == "d":
        row["legal_type"] = 1.0

        # Copy the notifying_party to clipboard when 'd' is pressed
        pyperclip.copy(notifying_party)
        print(f"'notifying_party' copied to clipboard: {notifying_party}")

        url_input = input("Enter OpenCorporates URL (or press Enter to leave it blank): ")
        row["OpenCorporates URL"] = url_input

    current_index += 1

    # Write the updated data to the CSV file
    with open(csv_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)
