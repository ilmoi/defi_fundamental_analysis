import json
import pprint
from typing import List, Dict

from requests import Session

from app.config import DEFIPULSE_API_KEY


def get_tvl_defipulse(token_results: List[Dict]):
    url = 'https://data-api.defipulse.com/api/v1/defipulse/api/GetProjects'

    parameters = {
        'api-key': DEFIPULSE_API_KEY,
    }

    session = Session()

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    # pprint.pprint(data)

    for token in data:
        for result in token_results:
            # todo could also mathc on symbol, but I've been getting false positives
            if result['name'].lower() == token['name'].lower():
                result['pulse_tvl'] = token['value']['total']['USD']['value']

    print('Successfully pulled defi pulse data.')
    return ['pulse_tvl']

# tokens = [{'name': 'Set Protocol'}]
# get_tvl_defipulse(tokens)
