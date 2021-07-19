from app.data_providers.pull_defipulse import get_tvl_defipulse
from data_providers.pull_cmc import get_metadata, get_listings_data
from data_providers.pull_defillama import get_tvl_defillama
from utils import merge_two_lists_of_dicts, save_data

token_slugs = [
# '0x',
# '88mph',
# 'aave',
# 'alchemix',
# 'axie-infinity',
# 'balancer',
# 'bancor',
# 'barnbridge',
# 'basketdao',
# 'centrifuge',
# 'compound',
# 'cream-finance',
# 'curve-dao-token',
# 'dhedge-dao',
# 'dodo',
# 'ellipsis',
# 'enzyme',
# 'fei-protocol',
# 'futureswap',
# 'harvest-finance',
# 'hegic',
# 'idle',
# 'index-cooperative',
# 'indexed-finance',
# 'instadapp',
# 'keeperdao',
# 'keep-network',
# 'kyber-network-crystal-legacy',
# 'lido-dao',
# 'liquity',
# 'loopring',
# 'maker',
# 'mirror-protocol',
# 'meta',
# 'pancakeswap',
# 'pangolin',
# 'perpetual-protocol',
# 'piedao-dough-v2',
# 'pooltogether',
# 'powerpool',
# 'quickswap',
# 'rarible',
# 'reflexer-ungovernance-token',
# 'ren',
# 'siren',
# 'stake-dao',
# 'sushiswap',
# 'swerve',
# 'synthetix-network-token',
# 'tokenlon-network-token',
# 'uma',
# 'uniswap',
# 'unit-protocol',
# 'venus',
# 'vesper',
# 'visor-finance',
# 'yearn-finance',
# 'raydium',
# 'serum',
# 'solfarm',
# 'mercurial-finance',
# 'mango-finance',
# 'oxygen',
# 'convex-finance',
# 'shiba-inu',
# 'mdex',
# 'alpaca-finance',
# 'anchor-protocol',
# 'iron-finance',
# 'belt',
# 'pancakebunny',
# 'badger-dao',
# 'beefy-finance',
# 'alpha-finance-lab',
# 'torn',
# 'armor',
# 'wault-finance-new',
# 'frax-share',
# 'bonfida',
# '1inch',
'bitcoin',
'ethereum',
'binance-coin',
'polkadot-new',
'cosmos',
'solana',
'ftx-token',
'handshake',
'thorchain',
'helium',
'arweave',
'bonfida',
'serum',
'cope',
# 'samoyedcoin',
'hxro',
'mercurial-finance',
'step-finance',
'audius',
'aave',
'compound',
'balancer',
'bancor',
'synthetix-network-token',
'yearn-finance',
'instadapp',
'keeperdao',
'pancakeswap',
'sushiswap',
]


def pull_data(token_slugs):

    (meta_results, meta_fieldnames) = get_metadata(token_slugs)
    (listing_results, listing_fieldnames) = get_listings_data(token_slugs)

    results = merge_two_lists_of_dicts(meta_results, listing_results)
    meta_fieldnames.extend(listing_fieldnames[1:])  # [1:] because we don't want to add the id twice

    tvl_fieldnames = get_tvl_defillama(results)
    meta_fieldnames.extend(tvl_fieldnames)

    # The only reason I'm doing defipulse next to defillama is to crossverify the data
    pulse_tvl_fieldnames = get_tvl_defipulse(results)
    meta_fieldnames.extend(pulse_tvl_fieldnames)

    save_data(results, meta_fieldnames)


if __name__ == '__main__':
    print(len(token_slugs))

    pull_data(','.join(token_slugs))
