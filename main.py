import pandas as pd

pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 200)          # Wider output

def main():
    florida_df = pd.read_csv('florida_parcels_broward_miamidade.csv')

    print(florida_df)

main()