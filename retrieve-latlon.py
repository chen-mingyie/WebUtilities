import requests, pandas as pd, os, time, argparse, logging
from tqdm import tqdm
from typing import List, Tuple
from random import random

def GetLatLon(searchtext: str) -> List[Tuple[float, float, str]]:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        # "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        "Sec-Ch-Ua": r"\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-65449c78-5fdd62e928bc0dc46e7d980d",
    }
    query = f"http://nominatim.openstreetmap.org/search?q={searchtext.replace(' ', '+')}&format=json&polygon=1&addressdetails=0"
    response = requests.get(query, headers=headers, timeout=30)
    
    results = []
    if response.status_code == 200:
        searchtexts = []
        lat = []
        lon = []
        address = []
        json_response = response.json()
        if len(json_response) > 0:
            for output in response.json():
                searchtexts.append(searchtext)
                lat.append(output['lat'])
                lon.append(output['lon'])
                address.append(output['display_name'])
        else:
            searchtexts.append(searchtext)
            lat.append(0.0)
            lon.append(0.0)
            address.append('NOT_FOUND')
        results = list(zip(searchtexts, lat, lon, address))
        # time.sleep(random()*5 + 2) # set random delay to make search more human-like
    else:
        logging.error(f'Response: {response.status_code}. Content: {response.text}')
    return results

def main(searches_filepath: str) -> List[Tuple[str, float, float, str]]:
    parentfolder = os.path.dirname(searches_filepath)
    filename, ext = os.path.splitext(os.path.basename(searches_filepath))
    export_filename = os.path.join(parentfolder, filename + '_processed' + ext)

    searches_df = pd.read_csv(searches_filepath, header=0)
    results = []
    df_columns = ['searchtext', 'lat', 'lon', 'address']
    # searches_df.apply(lambda searchtext: results.extend(GetLatLon(searchtext)))
    for index, row in tqdm(searches_df.iterrows(), total=searches_df.shape[0]):
        if isinstance(row['searchtext'], str) and len(row['searchtext']) > 0:
            results.extend(GetLatLon(row['searchtext']))
        if index % 10.0 == 0:
            results_df = pd.DataFrame(results, columns=df_columns)
            results_df.to_csv(export_filename, index=False)
    results_df = pd.DataFrame(results, columns=df_columns)
    results_df.to_csv(export_filename, index=False)
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Call Open Stream Map API to retrieve lat, lon, address of a search query. Results will be exported to parent folder of the input file.')
    parser.add_argument('--searchtextsfile', metavar='', required=True, help='filepath containing a list of search queries; must contain a column called "searchtext".')
    args = parser.parse_args()
    main(args.searchtextsfile)
    # main(r'D:\cmingyi\A2) SRO Work\Knowledge Graph\INGENIO_Automation Open Steet Map_2.csv')
    pass