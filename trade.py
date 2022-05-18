from tda import auth, client
import json
import config

try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome() as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

# r = c.get_price_history('AAPL',
#        period_type=client.Client.PriceHistory.PeriodType.YEAR,
#        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
#        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
#        frequency=client.Client.PriceHistory.Frequency.DAILY)
#assert r.status_code == 200, r.raise_for_status()
#print(json.dumps(r.json(), indent=4))

