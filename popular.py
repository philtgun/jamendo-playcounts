import argparse
from operator import index
from pathlib import Path
import pandas as pd

def get_popular(tsv_file: Path, out_file: Path):
    df = pd.read_csv(tsv_file, sep='\t')
    df_sorted = df.sort_values(by='rate_listened_total', ascending=False)
    df_sorted.to_csv(out_file, sep='\t')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tsv_file', type=Path) 
    parser.add_argument('out_file', type=Path) 
    args = parser.parse_args()

    get_popular(args.tsv_file, args.out_file)