import json
import csv

# Load JSON data from a file
with open('your_json_file.json', 'r') as file:
    data = json.load(file)

# Prepare CSV file
with open('transformations.csv', 'w', newline='') as csvfile:
    fieldnames = ['type', 'name', 'description', 'output', 'inputs']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
        # Extract transformation details
        transformation = item.get('transformation', {})
        transformation_type = transformation.get('type', '')
        transformation_name = transformation.get('name', '')
        transformation_description = transformation.get('description', '')

        # Construct output string
        output = item.get('output', {})
        output_str = f"{output.get('object_database', '')}.{output.get('object_schema', '')}.{output.get('object', '')}.{output.get('name', '')}"

        # Construct inputs string
        inputs = item.get('inputs', [])
        inputs_str = ', '.join([f"{input.get('object_database', '')}.{input.get('object_schema', '')}.{input.get('object', '')}.{input.get('name', '')}" for input in inputs])

        # Write row to CSV
        writer.writerow({
            'type': transformation_type,
            'name': transformation_name,
            'description': transformation_description,
            'output': output_str,
            'inputs': inputs_str
        })
