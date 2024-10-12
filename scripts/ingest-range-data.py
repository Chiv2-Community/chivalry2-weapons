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
    "Alt Overhead",
    "Special",
]


# Function to check if a value is "null" or "undefined" in a way that shouldn't update JSON
def is_valid_value(value):
    return value is not None and not (isinstance(value, float) and math.isnan(value))


# Function to update the JSON file with new range data
def update_json_with_ranges(json_file_path, ranges):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

        # Update the relevant attack range fields only if the CSV value is valid
        if "attacks" in data:
            attacks = data["attacks"]

            if "slash" in attacks:
                if is_valid_value(ranges["Slash"]):
                    attacks["slash"]["range"] = ranges["Slash"]
                if is_valid_value(ranges["Alt Slash"]):
                    attacks["slash"]["altRange"] = ranges["Alt Slash"]

            if "stab" in attacks:
                if is_valid_value(ranges["Stab"]):
                    attacks["stab"]["range"] = ranges["Stab"]
                if is_valid_value(ranges["Alt Stab"]):
                    attacks["stab"]["altRange"] = ranges["Alt Stab"]

            if "overhead" in attacks:
                if is_valid_value(ranges["Overhead"]):
                    attacks["overhead"]["range"] = ranges["Overhead"]
                if is_valid_value(ranges["Alt Overhead"]):
                    attacks["overhead"]["altRange"] = ranges["Alt Overhead"]

            if "special" in attacks and is_valid_value(ranges["Special"]):
                attacks["special"]["range"] = ranges["Special"]

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
                    "Special": row["Special"],
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
    if len(sys.argv) != 3:
        script_name = sys.argv[0]
        print(f"Usage: {script_name} <path_to_csv_file> <path_to_json_dir>")
        sys.exit(1)

    # Get the CSV file path and JSON directory path from the command-line arguments
    csv_file_path = sys.argv[1]
    json_dir = sys.argv[2]

    # Process the CSV and update the JSON files
    process_csv_and_update_json(csv_file_path, json_dir)
