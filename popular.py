import argparse
from operator import index
from pathlib import Path
import pandas as pd

def get_popular(tsv_file: Path, total: int = 20):
    df = pd.read_csv(tsv_file, sep='\t')
    df_sorted = df.sort_values(by='rate_listened_total', ascending=False)
    print(df_sorted[:total])

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tsv_file', type=Path) 
    args = parser.parse_args()

    get_popular(args.tsv_file)