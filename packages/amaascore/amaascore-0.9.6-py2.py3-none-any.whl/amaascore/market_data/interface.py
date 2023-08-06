from __future__ import absolute_import, division, print_function, unicode_literals

import json
import logging

from amaascore.core.amaas_model import json_handler
from amaascore.core.interface import Interface
from amaascore.market_data.utils import json_to_eod_price, json_to_fx_rate, json_to_curve, json_to_corporate_action


class MarketDataInterface(Interface):

    def __init__(self, environment=None, logger=None, endpoint=None, username=None, 
                 password=None, session_token=None):
        self.logger = logger or logging.getLogger(__name__)
        super(MarketDataInterface, self).__init__(endpoint=endpoint, endpoint_type='market_data', session_token=session_token,
                                                  environment=environment, username=username, password=password)

    def persist_eod_prices(self, asset_manager_id, business_date, eod_prices, update_existing_prices=True):
        """

        :param asset_manager_id:
        :param business_date: The business date for which these are rates.  Not really needed, could be derived...
        :param eod_prices:
        :param update_existing_prices:
        :return:
        """
        self.logger.info('Persist EOD Prices - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/eod-prices/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'update_existing_prices': update_existing_prices}
        eod_prices_json = [eod_price.to_interface() for eod_price in eod_prices]
        response = self.session.post(url, params=params, json=eod_prices_json)
        if response.ok:
            eod_prices = [json_to_eod_price(eod_price) for eod_price in response.json()]
            return eod_prices
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def retrieve_eod_prices(self, asset_manager_id, business_date, asset_ids=None, last_available=False):
        self.logger.info('Retrieve EOD Prices - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/eod-prices/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'asset_ids': ','.join(asset_ids)} if asset_ids else {}
        # setting last_available to True will return the latest price of the asset as of business
        # date (or latest prior price if price found on the date)
        if last_available:
            params.update({'last_available':True})
        response = self.session.get(url=url, params=params)
        if response.ok:
            eod_prices = [json_to_eod_price(eod_price) for eod_price in response.json()]
            self.logger.info('Returned %s EOD Prices.', len(eod_prices))
            return eod_prices
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def roll_prices(self, asset_manager_id, previous_date, asset_ids, update_existing_prices=False):
        url = '%s/roll-prices/%s' % (self.endpoint, asset_manager_id)
        params = {'update_existing_prices': update_existing_prices}
        json_body = json.loads(json.dumps({'previous_date': previous_date,
                                           'asset_ids': ','.join(asset_ids)}, default=json_handler))
        response = self.session.post(url=url, params=params, json=json_body)
        if response.ok:
            prices = [json_to_eod_price(price) for price in response.json()]
            self.logger.info('Rolled %s Prices.', len(prices))
            return prices
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def persist_fx_rates(self, asset_manager_id, business_date, fx_rates, update_existing_rates=True):
        """

        :param asset_manager_id:
        :param business_date: The business date for which these are rates.  Not really needed, could be derived...
        :param fx_rates:
        :param update_existing_rates:
        :return:
        """
        self.logger.info('Persist FX Rates - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/fx-rates/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'update_existing_rates': update_existing_rates}
        fx_rates_json = [fx_rate.to_interface() for fx_rate in fx_rates]
        response = self.session.post(url, params=params, json=fx_rates_json)
        if response.ok:
            fx_rates = [json_to_fx_rate(fx_rate) for fx_rate in response.json()]
            return fx_rates
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def retrieve_fx_rates(self, asset_manager_id, business_date, asset_ids=None):
        self.logger.info('Retrieve FX Rates - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/fx-rates/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'asset_ids': ','.join(asset_ids)} if asset_ids else {}
        response = self.session.get(url=url, params=params)
        if response.ok:
            fx_rates = [json_to_fx_rate(fx_rate) for fx_rate in response.json()]
            self.logger.info('Returned %s FX Rates.', len(fx_rates))
            return fx_rates
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def search_fx_rates(self, asset_manager_id, client_ids=None,
                        asset_ids=None, rate_types=None, rate_statuses=None,
                        business_date_start=None, business_date_end=None,
                        rate_timestamp_start=None, rate_timestamp_end=None):
        self.logger.info('Search FX Rates - Asset Manager: %s', asset_manager_id)
        url = '%s/fx-rates/%s' % (self.endpoint, asset_manager_id)

        params = {}
        if client_ids:
            params['client_ids'] = ','.join(client_ids)
        if asset_ids:
            params['asset_ids'] = ','.join(asset_ids)
        if rate_types:
            params['rate_types'] = ','.join(rate_types)
        if rate_statuses:
            params['rate_statuses'] = ','.join(rate_statuses)
        if business_date_start:
            params['business_date_start'] = business_date_start.date().isoformat()
        if business_date_end:
            params['business_date_end'] = business_date_end.date().isoformat()
        if rate_timestamp_start:
            params['rate_timestamp_start'] = rate_timestamp_start.strftime('%H:%m:%s')
        if rate_timestamp_end:
            params['rate_timestamp_end'] = rate_timestamp_end.strftime('%H:%m:%s')

        response = self.session.get(url=url, params=params)
        if response.ok:
            fx_rates = [json_to_fx_rate(fx_rate) for fx_rate in response.json()]
            self.logger.info('Returned %s FX Rates.', len(fx_rates))
            return fx_rates
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def retrieve_corporate_action(self, asset_manager_id, business_date, asset_ids):
        self.logger.info('Retrieve corporate action - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/corporate_actions/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'asset_ids': ','.join(asset_ids)}
        response = self.session.get(url=url, params=params)
        if response.ok:
            corporate_actions = [json_to_corporate_action(corporate_action) 
                                 for corporate_action in response.json()]
            self.logger.info('Returned %s corporate actions.', len(corporate_actions))
            return corporate_actions
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def persist_corporate_actions(self, asset_manager_id, business_date, corporate_actions):
        self.logger.info('Persist corporate actions - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/corporate_actions/%s' % (self.endpoint, asset_manager_id)
        corporate_action_json = [corporate_action.to_interface() for corporate_action in corporate_actions]
        response = self.session.post(url, json=corporate_action_json)
        if response.ok:
            corporate_actions = [json_to_corporate_action(corporate_action) for corporate_action in response.json()]
            return corporate_actions
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def retrieve_curve(self, asset_manager_id, business_date, asset_ids = None):
        self.logger.info('Retrieve curve - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/curves/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'asset_ids': ','.join(asset_ids)} if asset_ids else {}
        response = self.session.get(url = url, params = params)
        if response.ok:
            curves = [json_to_curve(curve) for curve in response.json() ]
            self.logger.info('Returned %s curves.', len(curves))
            return curves
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def persist_curves(self, asset_manager_id, business_date, curves, update_existing_curves=True):
        """
        :param asset_manager_id:
        :param business_date:
        :param curves:
        :param update_existing_rates:
        :return:
        """
        self.logger.info('Persist curves - Asset Manager: %s - Business Date: %s', asset_manager_id, business_date)
        url = '%s/curves/%s/%s' % (self.endpoint, asset_manager_id, business_date.isoformat())
        params = {'update_existing_curves': update_existing_curves}
        curves_json = [curve.to_interface() for curve in curves]
        response = self.session.post(url, params = params, json=curves_json)
        if response.ok:
            curves = [json_to_curve(curve) for curve in response.json()]
            return curves
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def clear(self, asset_manager_id):
        """ This method deletes all the data for an asset_manager_id.
            It should be used with extreme caution.  In production it
            is almost always better to Inactivate rather than delete. """
        self.logger.info('Clear Market Data - Asset Manager: %s', asset_manager_id)
        url = '%s/clear/%s' % (self.endpoint, asset_manager_id)
        response = self.session.delete(url)
        if response.ok:
            eod_price_count = response.json().get('eod_price_count', 'Unknown')
            self.logger.info('Deleted %s EOD Prices.', eod_price_count)
            fx_rate_count = response.json().get('fx_rate_count', 'Unknown')
            self.logger.info('Deleted %s FX Rates.', fx_rate_count)
            return response.json()
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def get_brokendate_fx_forward_rate(self, asset_manager_id,  asset_id, price_date, value_date):
        """
        This method takes calculates broken date forward FX rate based on the passed in parameters
        """
        self.logger.info('Calculate broken date FX Forward - Asset Manager: %s - Asset (currency): %s - Price Date: %s - Value Date: %s', asset_manager_id, asset_id, price_date, value_date)
        url = '%s/brokendateforward/%s' % (self.endpoint, asset_manager_id)
        params = {'value_date': value_date, 'asset_id':asset_id, 'price_date': price_date}
        response = self.session.get(url=url, params = params)
        if response.ok:
            forward_rate = response.json()
            self.logger.info('Retrieved broken date FX forward rate %s - %s: %s', asset_id, price_date, value_date)
            return forward_rate
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def market_data_retrieve(self, asset_manager_id, market_data_set):
        self.logger.info('Retrieving custom market data set')
        url = '%s/market-data/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=market_data_set)
        if response.ok:
            self.logger.info('Recieved %s custom market data points', str(len(response.json())))
            return response.json()
        else:
            self.logger.error(response.text)
            response.raise_for_status()


    def last_available_business_date(self, asset_manager_id, asset_ids, page_no=None, page_size=None):
        """
        Returns the last available business date for the assets so we know the 
        starting date for new data which needs to be downloaded from data providers.
        
        This method can only be invoked by system user
        """
        self.logger.info('Retrieving last available business dates for assets')
        url = '%s/last-available-business-date' % self.endpoint
        params = {'asset_manager_ids': [asset_manager_id],
                  'asset_ids': ','.join(asset_ids)}
        if page_no:
            params['page_no'] = page_no
        if page_size:
            params['page_size'] = page_size
        response = self.session.get(url, params=params)
        if response.ok:
            self.logger.info("Received %s assets' last available business date", len(response.json()))
            return response.json()
        else:
            self.logger.error(response.text)
            response.raise_for_status()