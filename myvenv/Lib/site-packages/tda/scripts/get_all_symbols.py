import json
import time

from tda import auth


def get_client(token_path):
    api_key = 'X5MUWQRRG9SMBQROM8I8FYAESQNJKHNP@AMER.OAUTHAP'
    redirect_uri = 'http://127.0.0.1:8000/td-example/callback'
    try:
        c = auth.client_from_token_file(token_path, api_key)
    except FileNotFoundError:
        from selenium import webdriver
        with webdriver.Firefox() as driver:
            c = auth.client_from_login_flow(
                driver, api_key, redirect_uri, token_path)

    return c


def chunks(lst, num_elts):
    for i in range(0, len(lst), num_elts):
        yield lst[i:i + num_elts]


c = get_client('/Volumes/alexgolec/token.json')
all_data = sorted(c.search_instruments(
    '[a-zA-Z.$]+', c.Instrument.Projection.SYMBOL_REGEX).json().items(),
    key=lambda t: t[0])
all_symbols = [t[0] for t in all_data]

with open('/tmp/data.json', 'w') as f:
    for symbol_block in chunks(all_symbols, 250):
        status = None
        while True:
            res = c.search_instruments(
                symbol_block, c.Instrument.Projection.FUNDAMENTAL)
            if res.status_code == 429:
                print('sleeping...')
                time.sleep(5)
            else:
                break

        f.write(json.dumps(res.json(), indent=4))
        print(json.dumps(res.json(), indent=4))
