import requests, json, lxml, re, time, pandas as pd, argparse, os, logging
from tqdm import tqdm
from bs4 import BeautifulSoup
from random import random

logging.getLogger().setLevel(logging.INFO)

def get_supplier_desc(supplier: str) -> str:
    # setting the right header values make search more human-like; helps prevent ip suspension from website
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
    query = re.sub(r'[^\w\s]', '', supplier) # remove all punctuation
    query = re.sub(' +', ' ', query) # replace multiple white spaces with single white space
    query = query.replace(' ', '+') # replace white space with '+'
    response = requests.get(url=f"https://www.google.com/search?q=Description+of+company+{query}", headers=headers, timeout=30)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        # results = soup.find_all('span', {'class' : 'ILfuVd'})
        # results = soup.find_all('span', {'class': 'hgKElc'})
        results = soup.find_all('div', {'class': 'LGOjhe'})
        links = soup.find_all('span', {'jsaction': re.compile('click:*')})
        if len(results) > 0:
            supplier_desc = results[0].contents[0].text
            supplier_desc = supplier_desc.replace('Hear this out loudPause', '')
            supplier_desc = supplier_desc.replace('COMPANY DESCRIPTION', '').replace('Company Description', '').replace('Company description', '')
            for link in links:
                link_text = link.contents[0].text
                supplier_desc = supplier_desc.replace(link_text, '')
        else:
            supplier_desc = supplier
        tqdm.write(str({supplier: supplier_desc}))
        time.sleep(random()*5 + 2) # set random delay to make search more human-like
    else:
        logging.error(f'Response: {response.status_code}. Content: {response.text}')
        
    return supplier_desc

def main(supplier_filepath: str):
    if not os.path.isfile(supplier_filepath):
        logging.warning(f'Filepath {supplier_filepath} does not exist.')
        return
    
    parentfolder = os.path.dirname(supplier_filepath)
    filename, ext = os.path.splitext(os.path.basename(supplier_filepath))
    export_filename = os.path.join(parentfolder, filename + '_processed' + ext)
    company_names_df = pd.read_csv(supplier_filepath, header=0)
    for index, row in tqdm(company_names_df.iterrows(), total=company_names_df.shape[0]):
        company_names_df.at[index,'desc'] = get_supplier_desc(row['name'])

        if index % 10.0 == 0:
            company_names_df.to_csv(export_filename, index=False)
    company_names_df.to_csv(export_filename, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape supplier descriptions from internet. Results will be exported to parent folder of the input file.')
    parser.add_argument('--supplierfile', metavar='', required=True, help='filepath containing a list of supplier names; must contain a column called "name".')
    args = parser.parse_args()
    main(supplier_filepath=args.supplierfile)
    # main(supplier_filepath=r'D:\cmingyi\A2) SRO Work\Company Name Matching\20240606_to be deleted\companies_test_to be deleted.csv')
    pass
