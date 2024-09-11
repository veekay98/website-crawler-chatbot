import json

# Load the JSON file
with open('knowledge-base.json', 'r') as f:
    data = json.load(f)

# Print the structure of the first few items in the list
for i, item in enumerate(data[:1]):  # Adjust the range as needed
    print(f"Item {i}: {item}")
