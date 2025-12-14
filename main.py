import pandas as pd

# I import and configure pandas display options
pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 120)          # Wider output
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
    florida_df.rename(columns={'parcel_id': 'ParcelID'}, inplace=True)

    ''' filter for residential properties (DOR_UC codes 1-4):
    1 - Single Family Residential
    2 - Mobile Home
    3 - Condominium
    4 - Cooperative
        '''

    florida_residential = florida_df[florida_df['property_use'] <= 4]
    tamarac_permits = pd.read_csv(r'./Tamarac/Tamarac_cleaned.csv')
    tamarac_cleaned = tamarac_permits[['ParcelID', 'WorkType', 'Contractor', 'Status']]
    hallandale_beach_permits = pd.read_csv('Hallandale_beach.csv')
    hallandale_cleaned = hallandale_beach_permits.rename(columns={
        'Main Parcel': 'ParcelID',
        'Type': 'WorkType',
        'Company Name': 'Contractor'
    })[['ParcelID', 'WorkType', 'Contractor', 'Status', 'Applied Date']]

    permits = pd.concat([tamarac_cleaned, hallandale_cleaned], ignore_index=True)

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

    Tamarac does not have any date information, while Hallandale Beach does.
    It may be necessary to add date information to Tamarac from another source later on.
    '''

    merged_df = pd.merge(permits, hallandale_cleaned, left_on='ParcelID', right_on='ParcelID', how='inner')

    # print the parcels with multiple permits
    duplicated_permits = merged_df["ParcelID"].value_counts()[merged_df["ParcelID"].value_counts() > 1]
    
    final_df = merged_df[merged_df['ParcelID'].isin(duplicated_permits.index)]
    final_df['Applied Date_y'] = pd.to_datetime(final_df['Applied Date_y'], format='%m/%d/%Y')
    final_df = final_df.sort_values(by='Applied Date_y')
    final_df['Time Since Last Permit'] = final_df.groupby('ParcelID')['Applied Date_y'].diff().dt.days

    avg_time = final_df.loc[final_df['Time Since Last Permit'].notna() & (final_df['Time Since Last Permit'] != 0),
                            'Time Since Last Permit'].mean()

    print(f"Average time since last permit (days): {avg_time:.2f}")

    print(final_df.dtypes)

    miamidade_residential_parcels = florida_residential[florida_residential['county'] == 'Miami-Dade']

    

main()