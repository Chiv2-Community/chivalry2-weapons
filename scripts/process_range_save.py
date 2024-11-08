import json
import os
import statistics
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict

# Names from the save data are not consistent with
# names from abilities override. This helps.
name_changes = {
    'SLEDGE HAMMER': 'SLEDGEHAMMER',
    'CANDELABRA': 'CARRYABLE  CANDELABRA',
    'FIST': 'FISTS',
    'MALLET': 'THROWING MALLET',
    'PICK AXE': 'PICKAXE',
    'Lions Bane': 'greatsword__malric',
    'Argon\'s Sword': 'longsword__argon__citadel',
}

def adapt_name(name: str) -> str:
    """Adapt weapon name to match the JSON file name."""
    return name_changes[name] if name in name_changes else name

@dataclass
class AttackStats:
    """Class to hold statistics for a weapon's attack."""
    raw_measurements: List[float]
    
    @property
    def average_range_measurement(self) -> float:
        return statistics.mean(self.raw_measurements)
    
    @property
    def std_deviation(self) -> float:
        return statistics.stdev(self.raw_measurements) if len(self.raw_measurements) > 1 else 0.0
    
    @property
    def min_measurement(self) -> float:
        return min(self.raw_measurements)
    
    @property
    def max_measurement(self) -> float:
        return max(self.raw_measurements)
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary format."""
        return {
            "averageRangeMeasurement": self.average_range_measurement,
            "rawMeasurements": self.raw_measurements,
            "stdDeviation": self.std_deviation,
            "min": self.min_measurement,
            "max": self.max_measurement
        }

def process_json_file(file_path: str) -> Dict[str, Dict[str, float]]:
    """Process a single JSON file and extract weapon-attack pairs."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    try:
        str_props = data["properties"]["WeaponData"]["str_props"]
        return {key: value["value"] for key, value in str_props.items()}
    except KeyError:
        print(f"Warning: File {file_path} does not have the expected structure")
        return {}

def parse_weapon_attack(key: str) -> Optional[tuple[str, str]]:
    """Parse a weapon-attack key into separate components."""
    try:
        weapon, attack = key.split('-', 1)
        return adapt_name(weapon.strip()), attack.strip()
    except ValueError:
        print(f"Warning: Invalid key format: {key}")
        return None

def process_directory(directory_path: str) -> Dict:
    """Process all JSON files in the directory and compute statistics."""
    # Dictionary to store all measurements for each weapon-attack pair
    measurements: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
    
    # Process each JSON file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            weapon_data = process_json_file(file_path)
            
            # Group measurements by weapon and attack
            for key, value in weapon_data.items():
                parsed = parse_weapon_attack(key)
                if parsed:
                    weapon, attack = parsed
                    measurements[weapon][attack].append(value)
    
    # Compute statistics for each weapon-attack pair
    result = {"rangeData": {}}
    for weapon, attacks in measurements.items():
        result["rangeData"][weapon] = {}
        for attack, values in attacks.items():
            result["rangeData"][weapon][attack] = AttackStats(values).to_dict()
    
    return result

def generate_csv(range_data: Dict, output_file: str):
    """Generate CSV file with average range values for each attack type."""
    import csv
    
    # Define the headers
    headers = ['Name', 'Slash', 'Alt Slash', 'Stab', 'Alt Stab', 'Overhead', 'Alt Overhead']
    
    # Prepare rows
    rows = []
    for weapon, attacks in range_data["rangeData"].items():
        row = {
            'Name': weapon,
            'Slash': None,
            'Alt Slash': None,
            'Stab': None,
            'Alt Stab': None,
            'Overhead': None,
            'Alt Overhead': None
        }
        
        # Fill in the values we have
        for attack_name, stats in attacks.items():
            # Normalize attack names to match our headers
            normalized_name = attack_name.replace('AltSlash', 'Alt Slash')\
                                      .replace('AltStab', 'Alt Stab')\
                                      .replace('AltOverhead', 'Alt Overhead')
            
            if normalized_name in headers:
                row[normalized_name] = stats['averageRangeMeasurement']
        
        rows.append(row)
    
    # Sort rows by weapon name
    rows.sort(key=lambda x: x['Name'])
    
    # Write to CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def main():
    """Main function to run the script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process weapon range test data')
    parser.add_argument('input_dir', help='Directory containing JSON test files')
    parser.add_argument('output_json', help='Output JSON file path')
    parser.add_argument('output_csv', help='Output CSV file path')
    
    args = parser.parse_args()
    
    # Process the directory
    result = process_directory(args.input_dir)
    
    # Write the results to a JSON file
    with open(args.output_json, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Generate CSV file
    generate_csv(result, args.output_csv)
    
    print(f"Processing complete. Results written to:")
    print(f"  JSON: {args.output_json}")
    print(f"  CSV: {args.output_csv}")

if __name__ == "__main__":
    main()