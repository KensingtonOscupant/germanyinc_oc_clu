import csv
import sys
import termios
import tty

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

# Open the CSV file and read the data
csv_file = "df_cleaned.csv"  # Replace with your CSV file path
with open(csv_file, "r") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

# Initialize a variable to store the next unique ID
next_id = 1

# Print a welcome message
print("Welcome to the company data utility!")
print("Press 'a' to insert 0 in the 'legal_type' column.")
print("Press 'd' to insert 1 in the 'legal_type' column.")
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
    print(f"Legal Type: {legal_type}")
    print(f"OpenCorporates URL: {open_corporates_url}")
    print("Press 'a' to insert 0, 'd' to insert 1, '1' to edit URL, or press Enter: ")

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
        url_input = input("Enter OpenCorporates URL (or press Enter to leave it blank): ")
        row["OpenCorporates URL"] = url_input

    current_index += 1

    # Write the updated data to the CSV file
    with open(csv_file, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print("Data written to file.")
