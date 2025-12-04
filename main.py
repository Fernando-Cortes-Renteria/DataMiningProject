import pandas as pd

pd.set_option('display.max_columns', None)   # Show all columns
pd.set_option('display.width', 200)          # Wider output

def main():
    df = pd.read_csv('Search Results.csv')

    for fol in df['Folio Number']:
        print(fol)
main()