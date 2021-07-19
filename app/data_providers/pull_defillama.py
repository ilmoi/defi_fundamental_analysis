import json
from typing import Dict, List

import requests
from app.utils import calc_avg_over_period


def get_tvl_defillama(token_results: List[Dict]) -> List[str]:
    """
    Augments token_results in place, returns newly added labels.
    """
    # this returns all 294 protocols
    response = requests.get('https://api.llama.fi/protocols')
    data = json.loads(response.text)
    # pprint.pprint(data)

    # [::-1] is a bit of a hack - some projects might have an old + a new version up (eg uni v2, uni v3) - by going backwards, the most recent update will be the project nearer the top of the list, which is the one we probably care about
    # I'm just too fucking lazy to write proper logic to handle cases like this
    for i, token in enumerate(data[::-1]):
        print(f"Processing token {i+1} out of {len(data)}")
        for result in token_results:
            # todo could also mathc on symbol, but I've been getting false positives
            if result['id'] == token['cmcId'] \
                    or result['slug'].lower() == token['slug'].lower() \
                    or result['website'].lower() == token['url'].lower() \
                    or result['name'].lower() == token['name'].lower():
                result['category'] = token.get('category', '')
                result['chain'] = token.get('chains', '')
                result['address'] = token.get('address', '')
                result['description'] = token.get('description', '')
                result['gecko_id'] = token.get('gecko_id', '')
                result['tvl'] = token.get('tvl', '')
                # result['change_7d'] = token.get('change_7d','')

                # historical tvl
                response = requests.get(f"https://api.llama.fi/protocol/{token['slug']}")
                historic_tvl = json.loads(response.text)['tvl']

                # average out over 2 weeks just before
                year_ago_tvl = calc_avg_over_period(365 + 14, 365, historic_tvl)
                six_months_ago_tvl = calc_avg_over_period(182 + 14, 182, historic_tvl)
                three_months_ago_tvl = calc_avg_over_period(90 + 14, 90, historic_tvl)
                one_month_ago_tvl = calc_avg_over_period(30 + 14, 30, historic_tvl)

                result['12m_ago'] = year_ago_tvl
                result['6m_ago'] = six_months_ago_tvl
                result['3m_ago'] = three_months_ago_tvl
                result['1m_ago'] = one_month_ago_tvl

    print('Successfully pulled defi llama data.')
    return ['category', 'chain', 'address', 'description', 'gecko_id', 'tvl', '12m_ago', '6m_ago', '3m_ago', '1m_ago']
