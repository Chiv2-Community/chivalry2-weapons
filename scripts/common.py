import csv

VALID_ATTACKS = ["slash", "slashHeavy", "overhead","overheadHeavy", "stab", "stabHeavy", "throw", "special", "sprintAttack", "sprintCharge"]

def write_dicts_to_csv(data, csv_file_path, keys = None):
    with open(csv_file_path, 'w', newline='') as f:
        writer = None
        for d in data:
            flat_d = flatten_dict(d)
            if writer is None:
                if keys is None:
                    keys = flat_d.keys()
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
            writer.writerow(flat_d)

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
