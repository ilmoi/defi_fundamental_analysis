import json
from typing import Dict, List

from dateutil import parser
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from app.config import CMC_API_KEY


# ------------------------------------------------------------------------------ meta

def get_metadata(token_slugs: str) -> (List[Dict], List[str]):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

    top_level_fieldnames = ['id', 'slug', 'name', 'symbol', 'twitter_username', 'date_added', 'platform', 'urls']
    actual_fieldnames = ['id', 'slug', 'name', 'symbol', 'twitter_username', 'date_added', 'platform', 'website', 'source_code', 'technical_doc', 'chat', 'reddit', 'twitter']

    parameters = {
        'slug': token_slugs,
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)['data']
        # pprint.pprint(data)

        keys = data.keys()

        results = []

        for key in keys:
            token = data[key]
            result = {}
            for (k, v) in token.items():
                # print(f'>> {k}, {v}')
                if k in top_level_fieldnames and v is not None:
                    if k == 'date_added':
                        # print(v)
                        result['date_added'] = parser.parse(v).strftime('%Y-%m-%d')
                    elif k == 'platform':
                        result['platform'] = v.get('slug', '')
                    elif k == 'urls':
                        result['website'] = ''.join(v.get('website', [''])).strip("[]'")
                        result['source_code'] = ''.join(v.get('source_code', [''])).strip("[]'")
                        result['technical_doc'] = ''.join(v.get('technical_doc', [''])).strip("[]'")
                        result['chat'] = ''.join(v.get('chat', [''])).strip("[]'")
                        result['reddit'] = ''.join(v.get('reddit', [''])).strip("[]'")
                        result['twitter'] = ''.join(v.get('twitter', [''])).strip("[]'")
                    else:
                        result[k] = v
            results.append(result)

        print(f'Successfully pulled CMC metadata. Total: {len(results)}')
        return results, actual_fieldnames

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"FAILED TO FETCH METADATA FOR TOKENS {token_slugs}: {e}")


# ------------------------------------------------------------------------------ listings data

def get_listings_data(token_slugs: str) -> (List[Dict], List[str]):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    top_level_fieldnames = ['id', 'cmc_rank', 'circulating_supply', 'total_supply', 'max_supply', 'quote']
    actual_fieldnames = ['id', 'cmc_rank', 'circulating_supply', 'total_supply', 'max_supply', 'price', 'percent_change_60d']

    parameters = {
        'limit': '5000',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)['data']
        # pprint.pprint(data)

        results = []

        for token in data:
            if token['slug'] in token_slugs:
                result = {}
                for (k, v) in token.items():
                    # print(f'>> {k}, {v}')
                    if k in top_level_fieldnames and v is not None:
                        if k == 'quote':
                            result['price'] = v['USD']['price']
                            result['percent_change_60d'] = v['USD']['percent_change_60d']
                        else:
                            result[k] = v
                results.append(result)

        print(f'Successfully pulled CMC listings data. Total: {len(results)}')
        return results, actual_fieldnames

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"FAILED TO FETCH LISTING DATA FOR TOKENS {token_slugs}: {e}")
