import pandas as pd

excel_file = 'Launch Sites.xlsx'
df = pd.read_excel(excel_file)

json_data = df.to_json(orient='records', indent=4)

with open('output.json', 'w') as f:
    f.write(json_data)