import argparse
import csv
from os import sep
from pathlib import Path
from more_itertools import grouper
from requests import get
import pandas as pd
from tqdm import tqdm

PREFIX = 'track_'

def get_playcounts(tsv_file: Path, client_id: str, output_file: Path, batch: int = 50) -> None:
    with tsv_file.open() as fp:
        csv_reader = csv.reader(fp, delimiter='\t')
        next(csv_reader)
        all_ids = [line[0].removeprefix('track_') for line in csv_reader]

    playcounts = {}
    for group_ids in tqdm(grouper(all_ids, batch, fillvalue='')):
        response = get('https://api.jamendo.com/v3.0/tracks', params={
            'client_id': client_id,
            'limit': batch,
            'include': 'stats',
            'id': ' '.join(group_ids)
        })
        if response.status_code == 200:
            response_json = response.json()
            # print(response_json['headers'])
            playcounts.update({f'{PREFIX}{int(result["id"]):07}': result['stats'] for result in response_json['results']})
        else:
            raise RuntimeError(f'Response not ok: {response}')

    df = pd.DataFrame.from_dict(playcounts, orient='index')
    df.to_csv(output_file, sep='\t', index_label='track')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tsv_file', type=Path) 
    parser.add_argument('client_id', type=str)
    parser.add_argument('output_file', type=Path) 
    args = parser.parse_args()

    get_playcounts(args.tsv_file, args.client_id, args.output_file)
