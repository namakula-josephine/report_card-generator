import pandas as pd

# Test data
data = '''Name,English,Math,Science,Student ID
Alice Kintu,61,95,53,1
Brian Mugisha,46,48,95,2
Carol Nakato,63,57,48,3
David Ssewankambo,50,98,71,4
Esther Aine,72,86,87,5
Fred Tumwine,98,73,55,6
Grace Kobusingye,48,49,58,7
Henry Okello,67,82,68,8
Irene Namaganda,63,92,83,9
James Byaruhanga,84,81,82,10'''

# Save as CSV first
with open('test_data.csv', 'w') as f:
    f.write(data)

# Read CSV and convert to Excel
df = pd.read_csv('test_data.csv')
df.to_excel('student_marks.xlsx', index=False)

print("Test file created successfully!")
