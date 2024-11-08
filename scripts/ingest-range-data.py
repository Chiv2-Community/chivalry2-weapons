#!/usr/bin/env python3

import json
import math
import os
import sys

import pandas as pd

# Required headers in the CSV (with "Right " prefix removed)
REQUIRED_HEADERS = [
    "Name",
    "Alt Slash",
    "Slash",
    "Stab",
    "Alt Stab",
    "Overhead",
    "Alt Overhead"
]

# Function to check if a value is "null" or "undefined" in a way that shouldn't update JSON
def is_valid_value(value):
    return value is not None and not (isinstance(value, float) and math.isnan(value))

changelog = {}

def add_changelog_entry(weapon_name, field_name, old_value, new_value):
    """
    Add an entry to the changelog directory for a value change
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    changelog_dir = "changelog"
    
    # Create changelog directory if it doesn't exist
    if not os.path.exists(changelog_dir):
        os.makedirs(changelog_dir)
    
    # Create changelog entry
    changelog[weapon_name + "." + field_name] = {
        "old_value": old_value,
        "new_value": new_value
    }
    
    # Write to changelog file
    changelog_file = f"{changelog_dir}/change_{timestamp}.json"
    with open(changelog_file, "w") as f:
        json.dump(entry, f, indent=2)

# Function to update the JSON file with new range data
def update_json_with_ranges(json_file_path, ranges):
    """
    Update JSON file with new range data and track changes in changelog
    """
    # Read the current data
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
        
    # Get weapon name from the file
    weapon_name = os.path.splitext(os.path.basename(json_file_path))[0]
    
    # Update the relevant attack range fields and track changes
    if "attacks" in data:
        attacks = data["attacks"]
        
        # Define attack types and their corresponding range fields
        attack_types = {
            "slash": ("Slash", "Alt Slash"),
            "stab": ("Stab", "Alt Stab"),
            "overhead": ("Overhead", "Alt Overhead")
        }
        
        # Process each attack type
        for attack_type, (normal_range, alt_range) in attack_types.items():
            if attack_type in attacks:
                # Normal range update
                if is_valid_value(ranges[normal_range]):
                    old_value = attacks[attack_type].get("range")
                    new_value = ranges[normal_range]
                    
                    if old_value != new_value:
                        attacks[attack_type]["range"] = new_value
                        add_changelog_entry(
                            weapon_name,
                            f"{attack_type}_range",
                            old_value,
                            new_value
                        )
                
                # Alt range update
                if is_valid_value(ranges[alt_range]):
                    old_value = attacks[attack_type].get("altRange")
                    new_value = ranges[alt_range]
                    
                    if old_value != new_value:
                        attacks[attack_type]["altRange"] = new_value
                        add_changelog_entry(
                            weapon_name,
                            f"{attack_type}_alt_range",
                            old_value,
                            new_value
                        )
    
    # Save the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)

# Function to validate the CSV file
def validate_csv_headers(df):
    if not all(header in df.columns for header in REQUIRED_HEADERS):
        missing_headers = [
            header for header in REQUIRED_HEADERS if header not in df.columns
        ]
        raise ValueError(
            f"CSV is missing the following required headers: {', '.join(missing_headers)}"
        )


# Main function to process the CSV and JSON files
def process_csv_and_update_json(csv_file_path, json_dir):
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(csv_file_path)

        # Validate the headers
        validate_csv_headers(df)

        # Iterate over each row in the CSV and update the corresponding JSON file
        for _, row in df.iterrows():
            # Construct the expected JSON file name
            weapon_name = row["Name"].lower().replace(" ", "_") + ".json"
            json_file_path = os.path.join(json_dir, weapon_name)

            # If the JSON file exists, update it with range data
            if os.path.exists(json_file_path):
                range_data = {
                    "Alt Slash": row["Alt Slash"],
                    "Slash": row["Slash"],
                    "Stab": row["Stab"],
                    "Alt Stab": row["Alt Stab"],
                    "Overhead": row["Overhead"],
                    "Alt Overhead": row["Alt Overhead"],
                }
                update_json_with_ranges(json_file_path, range_data)
                print(f"Updated {weapon_name} with new range data.")
            else:
                print(f"Warning: JSON file for {weapon_name} not found.")

    except FileNotFoundError:
        print(
            f"Error: CSV file '{csv_file_path}' or JSON directory '{json_dir}' not found."
        )
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Ensure CSV file path and JSON directory path are provided as input
    if len(sys.argv) != 4:
        script_name = sys.argv[0]
        print(f"Usage: {script_name} <path_to_csv_file> <path_to_json_dir> <path_to_changelog_file>")
        sys.exit(1)

    # Get the CSV file path and JSON directory path from the command-line arguments
    csv_file_path = sys.argv[1]
    json_dir = sys.argv[2]
    changelog_path = sys.argv[3]

    # Process the CSV and update the JSON files
    process_csv_and_update_json(csv_file_path, json_dir)

    # Write the changelog to a file
    changelog_string = ""
    for key, v in changelog.items():
        changelog_string += f"{key}: {v.old_value} -> {v.new_value}\n"

    with open(changelog_path, "w") as changelog_file:
        changelog_file.write(changelog_string)

