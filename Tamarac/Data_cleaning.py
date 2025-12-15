import pandas as pd

pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 200)          # Wider output

Tamarac = pd.read_json('resultadosTamarac.json')

Tamarac_cleaned = Tamarac.rename(columns={
    'parcel_id': 'ParcelID',
    'general_contractor': 'Contractor',
    'tenant_name': 'WorkType',
    'application_status': 'Status',
    'application_date': 'Applied Date'
})[['ParcelID', 'WorkType', 'Contractor', 'Status', 'Applied Date']]

print(Tamarac_cleaned)

Tamarac_cleaned.to_csv('Tamarac_cleaned.csv', index=False)