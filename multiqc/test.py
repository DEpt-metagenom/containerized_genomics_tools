import json
from bs4 import BeautifulSoup

# Load the HTML files
with open('./test/ref/multiqc_report.html', 'r') as ref_file:
    ref_content = ref_file.read()
with open('./test/output/multiqc_report_1.html', 'r') as gen_file:
    gen_content = gen_file.read()

# Parse the HTML to extract JSON data
ref_soup = BeautifulSoup(ref_content, 'html.parser')
gen_soup = BeautifulSoup(gen_content, 'html.parser')

# Extract JSON data from the script tag in both files
ref_json_data = json.loads(ref_soup.find('script', type='application/json').string)
gen_json_data = json.loads(gen_soup.find('script', type='application/json').string)

# Remove timestamp lines if present, e.g., from JSON data
if 'timestamp' in ref_json_data:
    del ref_json_data['timestamp']
if 'timestamp' in gen_json_data:
    del gen_json_data['timestamp']

# Compare the JSON data
if ref_json_data == gen_json_data:
    print("The reports are identical after removing timestamps.")
else:
    print("Differences found in the reports:")
    print("\nReference Report JSON:")
    print(json.dumps(ref_json_data, indent=2))
    print("\nGenerated Report JSON:")
    print(json.dumps(gen_json_data, indent=2))
