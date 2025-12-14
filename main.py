import pandas as pd

# I import and configure pandas display options
pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 200)          # Wider output
pd.set_option("display.precision", 2)
pd.set_option('display.float_format', '{:,.2f}'.format)

# main function to read and process the data
def main():
    broward = pd.read_csv('broward_parcels.csv')
    miami = pd.read_csv('miamidade_parcels.csv')

    # i add county identifier
    miami['county'] = 'Miami-Dade'
    broward['county'] = 'Broward'

    # merge into a single dataframe
    florida_df = pd.concat([broward, miami], ignore_index=True)

    ''' filter for residential properties (DOR_UC codes 1-4):
    1 - Single Family Residential
    2 - Mobile Home
    3 - Condominium
    4 - Cooperative
        '''

    florida_residential = florida_df[florida_df['property_use'] <= 4]
    tamarac_permits = pd.read_csv(r'./Tamarac/Tamarac_cleaned.csv')
    hallandale_beach_permits = pd.read_csv('Hallandale_beach.csv')
    hallandale_cleaned = hallandale_beach_permits.rename(columns={
        'Main Parcel': 'ParcelID',
        'Type': 'WorkType',
        'Company Name': 'Contractor'

    '''
    Tamarac has the following variables:
    -ApplicationNumber-, -Address-, ParcelID, Contractor, WorkType, Status

    Hallandale Beach has the following variables:
    Case Number,Type,Status,Project Name,Issued Date,Applied Date,Expiration Date,Finalized Date,Module Name,Company Name,Company Type,Address,Main Parcel,Description,DBA

    The Application Number is not consistent across the datasets
    We will merge on ParcelID

    Status is similar across both datasets, but not identical
    Address is not necessary thanks to florida_residential having situs_address
    Contractor is very useful
    WorkType/Type is very useful and similar
    '''

    merged_df = pd.merge(tamarac_permits, florida_residential, left_on='ParcelID', right_on='parcel_id', how='inner')

    # print the parcels with multiple permits
    # print(merged_df["parcel_id"].value_counts()[merged_df["parcel_id"].value_counts() > 1])



main()