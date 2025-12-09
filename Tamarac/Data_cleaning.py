import pandas as pd

pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 200)          # Wider output

Tamarac = pd.read_json('resultadosTamarac.json')

Tamarac.columns = ['ApplicationNumber', 'Address', 'ParcelID', 'Contractor', 'WorkType', 'Status']

print(Tamarac.head())

Tamarac.to_csv('Tamarac_cleaned.csv', index=False)