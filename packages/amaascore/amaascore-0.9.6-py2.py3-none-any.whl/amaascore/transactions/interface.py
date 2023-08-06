from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import json

from amaascore.core.amaas_model import json_handler
from amaascore.core.interface import Interface
from amaascore.transactions.utils import (
    json_to_transaction, json_to_position, json_to_mtm_result,
    json_to_transaction_pnl, json_to_position_pnl,
    json_to_book_report, json_to_pnl
)


class TransactionsInterface(Interface):

    def __init__(self, environment=None, logger=None, endpoint=None, username=None,
                       password=None, session_token=None):
        self.logger = logger or logging.getLogger(__name__)
        super(TransactionsInterface, self).__init__(endpoint=endpoint, endpoint_type='transactions', session_token=session_token,
                                                    environment=environment, username=username, password=password)

    def new(self, transaction):
        self.logger.info('New Transaction - Asset Manager: %s - Transaction ID: %s', transaction.asset_manager_id,
                         transaction.transaction_id)
        url = '%s/transactions/%s' % (self.endpoint, transaction.asset_manager_id)
        response = self.session.post(url, json=transaction.to_interface())
        if response.ok:
            transaction = json_to_transaction(response.json())
            return transaction
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def create_many(self, transactions):
        if type(transactions) is not list:
            raise ValueError('Error - create_many takes in a list of transactions instead of single transaction')
        transactions_json = []
        # check to ensure all transactions have the same asset_manager_id
        asset_manager_id = transactions[0].asset_manager_id
        for transaction in transactions:
            transactions_json.append(transaction.to_interface())
            if transaction.asset_manager_id != asset_manager_id:
                raise AttributeError('Check failed - Not all transactions have the same asset manager ID.')
        self.logger.info('Multple new Transactions - Asset Manager: %s', asset_manager_id)
        url = '%s/transactions/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=transactions_json)
        if response.ok:
            transactions = []
            for transaction_json in response.json():
                transactions.append(json_to_transaction(transaction_json))
            return transactions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def amend(self, transaction):
        self.logger.info('Amend Transaction - Asset Manager: %s - Transaction ID: %s', transaction.asset_manager_id,
                         transaction.transaction_id)
        url = '%s/transactions/%s/%s' % (self.endpoint, transaction.asset_manager_id, transaction.transaction_id)
        response = self.session.put(url, json=transaction.to_interface())
        if response.ok:
            transaction = json_to_transaction(response.json())
            return transaction
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def partial(self, asset_manager_id, transaction_id, updates):
        self.logger.info('Partial Amend Transaction - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/transactions/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        response = self.session.patch(url, data=json.dumps(updates, default=json_handler), headers=self.json_header)
        if response.ok:
            transaction = json_to_transaction(response.json())
            return transaction
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve(self, asset_manager_id, transaction_id, version=None):
        self.logger.info('Retrieve Transaction - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/transactions/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        if version:
            url += '?version=%d' % int(version)
        response = self.session.get(url)
        if response.ok:
            return json_to_transaction(response.json())
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def transactions_by_asset_manager(self, asset_manager_id):
        self.logger.info('Retrieve Transactions by Asset Manager: %s', asset_manager_id)
        url = '%s/transactions/%s' % (self.endpoint, asset_manager_id)
        response = self.session.get(url)
        if response.ok:
            transactions = [json_to_transaction(json_transaction) for json_transaction in response.json()]
            self.logger.info('Returned %s Transactions.', len(transactions))
            return transactions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def cancel(self, asset_manager_id, transaction_id):
        self.logger.info('Cancel Transaction - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/transactions/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        response = self.session.delete(url)
        if response.ok:
            self.logger.info('Successfully Cancelled - Asset Manager: %s - Transaction ID: %s.', asset_manager_id,
                             transaction_id)
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def search(self, asset_manager_id, transaction_ids=[], transaction_statuses=[],
               asset_book_ids=[], counterparty_book_ids=[], asset_ids=[], transaction_date_start=None,
               transaction_date_end=None, code_types=[], code_values=[], link_types=[], linked_transaction_ids=[],
               party_types=[], party_ids=[], reference_types=[], reference_values=[], client_ids=[],
               child_types=[], page_no=None, page_size=None):
        self.logger.info('Search Transactions - Asset Manager: %s', asset_manager_id)
        search_params = {}
        # Potentially roll this into a loop through args rather than explicitly named - depends on additional validation
        if transaction_ids:
            search_params['transaction_ids'] = ','.join(transaction_ids)
        if transaction_statuses:
            search_params['transaction_statuses'] = ','.join(transaction_statuses)
        if asset_book_ids:
            search_params['asset_book_ids'] = ','.join(asset_book_ids)
        if counterparty_book_ids:
            search_params['counterparty_book_ids'] = ','.join(counterparty_book_ids)
        if asset_ids:
            search_params['asset_ids'] = ','.join(asset_ids)
        if transaction_date_start:
            search_params['transaction_date_start'] = transaction_date_start
        if transaction_date_end:
            search_params['transaction_date_end'] = transaction_date_end
        if code_types:
            search_params['code_types'] = ','.join(code_types)
        if code_values:
            search_params['code_values'] = ','.join(code_values)
        if link_types:
            search_params['link_types'] = ','.join(link_types)
        if linked_transaction_ids:
            search_params['linked_transaction_ids'] = ','.join(linked_transaction_ids)
        if party_types:
            search_params['party_types'] = ','.join(party_types)
        if party_ids:
            search_params['party_ids'] = ','.join(party_ids)
        if reference_types:
            search_params['reference_types'] = ','.join(reference_types)
        if reference_values:
            search_params['reference_values'] = ','.join(reference_values)
        if client_ids:
            search_params['client_ids'] = ','.join(client_ids)
        if child_types:
            search_params['child_types'] = ','.join(child_types)
        if page_no is not None:
            search_params['page_no'] = page_no
        if page_size:
            search_params['page_size'] = page_size
        url = '%s/transactions/%s' % (self.endpoint, asset_manager_id)
        response = self.session.get(url, params=search_params)
        if response.ok:
            transactions = [json_to_transaction(json_transaction) for json_transaction in response.json()]
            self.logger.info('Returned %s Transactions.', len(transactions))
            return transactions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def new_mtm_results(self, asset_manager_id, mtm_results):
        self.logger.info('Marking to market Positions - Asset Manager: %s', asset_manager_id)
        if not isinstance(mtm_results, list):
            mtm_results = [mtm_results]
        mtm_result_json = []
        for mtm_result in mtm_results:
            mtm_result_json.append(mtm_result.to_interface())
        url = '%s/mtm/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=mtm_result_json, params={'upsert': False})
        if response.ok:
            mtm_results = []
            for mtm_result_json in response.json():
                mtm_results.append(json_to_mtm_result(mtm_result_json))
            return mtm_results
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def upsert_mtm_results(self, asset_manager_id, mtm_results):
        self.logger.info('Upserting Marking to market Positions - Asset Manager: %s', asset_manager_id)
        if not isinstance(mtm_results, list):
            mtm_results = [mtm_results]
        mtm_result_json = []
        for mtm_result in mtm_results:
            mtm_result_json.append(mtm_result.to_interface())
        url = '%s/mtm/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=mtm_result_json, params={'upsert': True})
        if response.ok:
            mtm_results = []
            for mtm_result_json in response.json():
                mtm_results.append(json_to_mtm_result(mtm_result_json))
            return mtm_results
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def amend_mtm_results(self, asset_manager_id, mtm_results):
        self.logger.info('Amending mtm Positions - Asset Manager: %s', asset_manager_id)
        if not isinstance(mtm_results, list):
            mtm_results = [mtm_results]
        mtm_result_json = []
        for mtm_result in mtm_results:
            mtm_result_json.append(mtm_result.to_interface())
        url = '%s/mtm/%s' % (self.endpoint, asset_manager_id)
        response = self.session.put(url, json=mtm_result_json)
        if response.ok:
            mtm_results = []
            for mtm_result_json in response.json():
                mtm_results.append(json_to_mtm_result(mtm_result_json))
            return mtm_results
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_mtm_results(self, book_id, asset_manager_id, paramaters):
        """
        parameters is a dictionary of all the mtm result filter parameters
        """
        self.logger.info('Retrieving mtm Positions - Asset Manager: %s', asset_manager_id)
        url = '%s/mtm/%s' % (self.endpoint, asset_manager_id)
        paramaters.update({'book_id': book_id})
        response = self.session.get(url, params = paramaters)
        if response.ok:
            mtm_results = [json_to_mtm_result(json_mtm_result) for json_mtm_result in response.json()]
            self.logger.info('Returned %s mtm results.', len(mtm_results))
            return mtm_results
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_aggregate_pnls(self, asset_manager_id, book_ids, business_date, currency):
        self.logger.info('Retrieving Aggregate PnL result - Asset Manager: %s - Book IDs: (%s) - Business Date: %s - Currency: %s' % \
                        (asset_manager_id, ', '.join(book_ids), business_date, currency))
        url = '%s/aggregate_pnls/%s' % (self.endpoint, asset_manager_id)
        search_params = {'business_date': business_date,
                         'book_ids': book_ids,
                         'currency': currency}
        response = self.session.get(url, params=search_params)
        if response.ok:
            return response.json()
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def upsert_book_reports(self, asset_manager_id, book_reports, report_type):
        self.logger.info('Insert book report for -Asset Manager: %s', asset_manager_id)
        if not isinstance(book_reports, list):
            book_reports = [book_reports]
        book_report_json = []
        for book_report in book_reports:
            book_report_json.append(book_report.to_interface())
        url = '%s/book-report/%s/%s' % (self.endpoint, asset_manager_id, report_type)
        response = self.session.post(url, json=book_report_json, params={'upsert': True})
        if response.ok:
            book_reports = []
            for book_report_json in response.json():
                book_reports.append(json_to_book_report(book_report_json))
            self.logger.info('Created %s Book Report', len(book_reports))
            return book_reports
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def new_transaction_pnls(self, asset_manager_id, transaction_pnls):
        self.logger.info('Insert Transaction PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(transaction_pnls, list):
            transaction_pnls = [transaction_pnls]
        transaction_pnl_json = []
        for transaction_pnl in transaction_pnls:
            transaction_pnl_json.append(transaction_pnl.to_interface())
        url = '%s/transaction_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=transaction_pnl_json, params={'upsert': False})
        if response.ok:
            transaction_pnls = []
            for transaction_pnl_json in response.json():
                transaction_pnls.append(json_to_transaction_pnl(transaction_pnl_json))
            self.logger.info('Created %s Transaction PnL records', len(transaction_pnls))
            return transaction_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def upsert_transaction_pnls(self, asset_manager_id, transaction_pnls):
        self.logger.info('Upsert Transaction PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(transaction_pnls, list):
            transaction_pnls = [transaction_pnls]
        transaction_pnl_json = []
        for transaction_pnl in transaction_pnls:
            transaction_pnl_json.append(transaction_pnl.to_interface())
        url = '%s/transaction_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=transaction_pnl_json, params={'upsert': True})
        if response.ok:
            transaction_pnls = []
            for transaction_pnl_json in response.json():
                transaction_pnls.append(json_to_transaction_pnl(transaction_pnl_json))
            self.logger.info('Upserted %s Transaction PnL records', len(transaction_pnls))
            return transaction_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def amend_transaction_pnls(self, asset_manager_id, transaction_pnls):
        self.logger.info('Amend Transaction PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(transaction_pnls, list):
            transaction_pnls = [transaction_pnls]
        transaction_pnl_json = []
        for transaction_pnl in transaction_pnls:
            transaction_pnl_json.append(transaction_pnl.to_interface())
        url = '%s/transaction_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.put(url, json=transaction_pnl_json)
        if response.ok:
            transaction_pnls = []
            for transaction_pnl_json in response.json():
                transaction_pnls.append(json_to_transaction_pnl(transaction_pnl_json))
            self.logger.info('Amended %s Transaction PnL records', len(transaction_pnls))
            return transaction_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_book_reports(self, asset_manager_id, book_ids, report_type,
                              report_date_start=None, report_date_end=None, period=None):
        self.logger.info("""Retrieve Book %s Reports for - Asset Manager: %s""", \
                            report_type, asset_manager_id)
        url = '%s/book-report/%s/%s' % (self.endpoint, asset_manager_id, report_type)
        params = {'book_ids': book_ids}
        if period:
            params['period'] = period
        if report_date_start:
            params['report_date_start'] = report_date_start
        if report_date_end:
            params['report_date_end'] = report_date_end

        response = self.session.get(url, params=params)
        if response.ok:
            book_reports = [json_to_book_report(json_book_report) for json_book_report in response.json()]
            self.logger.info('Returned %s Book Reports.', len(book_reports))
            return book_reports
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_transaction_pnls(self, book_ids, asset_manager_id,
                                  business_date, periods=None,
                                  page_no=None, page_size=None):
        self.logger.info('Retrieving Transaction PnL result - Asset Manager: %s - Book IDs: (%s) - Business Date: %s' % \
                        (asset_manager_id, ', '.join(book_ids), business_date))
        url = '%s/transaction_pnls/%s' % (self.endpoint, asset_manager_id)
        search_params = {'business_date': business_date,
                         'book_ids': book_ids}
        if periods:
            search_params['periods'] = periods
        if page_no:
            search_params['page_no'] = page_no
        if page_size:
            search_params['page_size'] = page_size

        response = self.session.get(url, params=search_params)
        if response.ok:
            transaction_pnls = [json_to_transaction_pnl(json_transaction_pnl) for json_transaction_pnl in response.json()]
            self.logger.info('Returned %s Transaction PnL results.', len(transaction_pnls))
            return transaction_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def new_position_pnls(self, asset_manager_id, position_pnls):
        self.logger.info('Insert Position PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(position_pnls, list):
            position_pnls = [position_pnls]
        position_pnl_json = []
        for position_pnl in position_pnls:
            position_pnl_json.append(position_pnl.to_interface())
        url = '%s/position_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=position_pnl_json, params={'upsert': False})
        if response.ok:
            position_pnls = []
            for position_pnl_json in response.json():
                position_pnls.append(json_to_position_pnl(position_pnl_json))
            self.logger.info('Created %s Position PnL records', len(position_pnls))
            return position_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def upsert_position_pnls(self, asset_manager_id, position_pnls):
        self.logger.info('Upsert Position PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(position_pnls, list):
            position_pnls = [position_pnls]
        position_pnl_json = []
        for position_pnl in position_pnls:
            position_pnl_json.append(position_pnl.to_interface())
        url = '%s/position_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.post(url, json=position_pnl_json, params={'upsert': True})
        if response.ok:
            position_pnls = []
            for position_pnl_json in response.json():
                position_pnls.append(json_to_position_pnl(position_pnl_json))
            self.logger.info('Upserted %s Position PnL records', len(position_pnls))
            return position_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def amend_position_pnls(self, asset_manager_id, position_pnls):
        self.logger.info('Amend Position PnL results for - Asset Manager: %s', asset_manager_id)
        if not isinstance(position_pnls, list):
            position_pnls = [position_pnls]
        position_pnl_json = []
        for position_pnl in position_pnls:
            position_pnl_json.append(position_pnl.to_interface())
        url = '%s/position_pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.put(url, json=position_pnl_json)
        if response.ok:
            position_pnls = []
            for position_pnl_json in response.json():
                position_pnls.append(json_to_position_pnl(position_pnl_json))
            self.logger.info('Amended %s Position PnL records', len(position_pnls))
            return position_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_position_pnls(self, book_ids, asset_manager_id,
                               business_date, periods=None,
                               page_no=None, page_size=None):
        self.logger.info('Retrieving Position PnL result - Asset Manager: %s - Book IDs: (%s) - Business Date: %s' % \
                        (asset_manager_id, ', '.join(book_ids), business_date))
        url = '%s/position_pnls/%s' % (self.endpoint, asset_manager_id)
        search_params = {'business_date': business_date,
                         'book_ids': book_ids}
        if periods:
            search_params['periods'] = periods
        if page_no:
            search_params['page_no'] = page_no
        if page_size:
            search_params['page_size'] = page_size

        response = self.session.get(url, params=search_params)
        if response.ok:
            position_pnls = [json_to_position_pnl(json_position_pnl) for json_position_pnl in response.json()]
            self.logger.info('Retrieved %s Position PnL results.', len(position_pnls))
            return position_pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def get_pnl_transactions(self, book_id, asset_manager_id, start_date, end_date):
        self.logger.info('Retrieving transactions for PnL - Asset Manager: %s - Book ID: %s'%(asset_manager_id, book_id))
        url = '%s/pnl_transactions/%s' % (self.endpoint, asset_manager_id)
        search_params = {'asset_manager_id': asset_manager_id,
                         'start_date': start_date,
                         'book_id': book_id,
                         'end_date': end_date}
        response = self.session.get(url, params=search_params)
        if response.ok:
            transactions = [json_to_transaction(json_transaction) for json_transaction in response.json()]
            self.logger.info('Returned %s Transactions.', len(transactions))
            return transactions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def position_search(self, asset_manager_id, book_ids=None, account_ids=None,
                        accounting_types=None, asset_ids=None,
                        position_date=None, include_cash=False,
                        page_no=None, page_size=None):
        self.logger.info('Search Positions - Asset Manager: %s', asset_manager_id)
        search_params = {}
        # Potentially roll into a loop
        if book_ids:
            search_params['book_ids'] = ','.join(book_ids)
        if account_ids:
            search_params['account_ids'] = ','.join(account_ids)
        if accounting_types:
            search_params['accounting_types'] = ','.join(accounting_types)
        if asset_ids:
            search_params['asset_ids'] = ','.join(asset_ids)
        if position_date:
            search_params['position_date'] = position_date
        if include_cash:
            search_params['include_cash'] = include_cash
        if page_no is not None:
            search_params['page_no'] = page_no
        if page_size:
            search_params['page_size'] = page_size
        url = '%s/positions/%s' % (self.endpoint, asset_manager_id)
        response = self.session.get(url, params=search_params)
        if response.ok:
            positions = [json_to_position(json_position) for json_position in response.json()]
            self.logger.info('Returned %s Positions.', len(positions))
            return positions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    # Should this method just be collapsed into positions_by_asset_manager?
    def positions_by_asset_manager_book(self, asset_manager_id, book_id):
        self.logger.info('Retrieve Positions by Asset Manager: %s and Book: %s', asset_manager_id, book_id)
        url = '%s/positions/%s/%s' % (self.endpoint, asset_manager_id, book_id)
        response = self.session.get(url)
        if response.ok:
            positions = [json_to_position(json_position) for json_position in response.json()]
            self.logger.info('Returned %s Positions.', len(positions))
            return positions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def positions_by_asset_manager(self, asset_manager_id, book_ids=None):
        self.logger.info('Retrieve Positions by Asset Manager: %s', asset_manager_id)
        url = '%s/positions/%s' % (self.endpoint, asset_manager_id)
        params = {'book_ids': ','.join(book_ids)} if book_ids else {}
        response = self.session.get(url, params=params)
        if response.ok:
            positions = [json_to_position(json_position) for json_position in response.json()]
            self.logger.info('Returned %s Positions.', len(positions))
            return positions
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def pnl_search(self, asset_manager_id, pnl_type, business_date,
                   **kwargs):
        """
        Search pnl records.

        Args:
            asset_manager_id (int): id of asset manager owning the pnl records
            pnl_type (str): either "Position" or "Transaction
            business_date (date): date of the pnl records to return
            book_ids (list): book id filter on pnl records
            asset_ids (list): asset id filter on pnl records
            transaction_ids (list): transactino id filter on pnl records
            next_hash_key (str): continuation hash key for paging the results
            next_range_key (str): continuation range key for paging the results
            page_size (int): the number of results to return
        """
        self.logger.info('Retrieving Pnls - Asset Manager: %s - Business Date: %s' % \
                        (asset_manager_id, business_date))
        url = '%s/pnls/%s' % (self.endpoint, asset_manager_id)
        search_params = {'pnl_type': pnl_type,
                         'business_date': business_date.isoformat()}

        for param_key, param_val in kwargs.items():
            if not param_val:
                continue
            search_params[param_key] = ','.join(param_val) if isinstance(param_val, list) else param_val

        response = self.session.get(url, params=search_params)
        if response.ok:
            json_body = response.json()
            results = json_body.get('items')
            next_hash_key = json_body.get('next_hash_key')
            next_range_key = json_body.get('next_range_key')
            pnls = [json_to_pnl(pnl_json) for pnl_json in results]
            self.logger.info('Retrieved %s Pnl records.', len(pnls))
            return next_hash_key, next_range_key, pnls
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def pnl_upsert(self, asset_manager_id, pnls):
        """
        Upsert a list of pnls. Note: this performs a full update
        of existing records with matching keys, so the passed in
        pnl objects should be complete.

        Args:
            asset_manager_id (int): the id of the asset manager owning the pnl
            pnls (list): list of pnl objects to upsert
        """
        self.logger.info('Upsert PnL for - Asset Manager: %s', asset_manager_id)
        pnls = [pnls] if not isinstance(pnls, list) else pnls

        json_pnls = [pnl.to_interface() for pnl in pnls]
        url = '%s/pnls/%s' % (self.endpoint, asset_manager_id)
        response = self.session.put(url, json=json_pnls)
        if response.ok:
            results = []
            for pnl_result in response.json():
                results.append(json_to_pnl(pnl_result))
            self.logger.info('Upserted %s PnL records', len(results))
            return results
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def pnl_cancel(self, asset_manager_id, pnl_type,
                   business_date, book_id,
                   next_hash_key=None, next_range_key=None,
                   page_size=None):
        """
        Cancel the PNL records matching the request

        Args:
            asset_manager_id (int): id of asset manager owning the pnl records
            pnl_type (str): either "Position" or "Transaction
            business_date (date): date of the pnl records to return
            book_id (str): book id filter on pnl records
            next_hash_key (str): continuation hash key for paging the results
            next_range_key (str): continuation range key for paging the results
            page_size (int): the number of results to return
        """
        self.logger.info('Cancelling %s Pnls - Asset Manager: %s - Business Date: %s - Book: %s' % \
                        (pnl_type, asset_manager_id, business_date, book_id))
        url = '%s/pnls/%s' % (self.endpoint, asset_manager_id)
        params = {'pnl_type': pnl_type,
                  'business_date': business_date.isoformat(),
                  'book_id': book_id}

        if next_hash_key:
            params['next_hash_key'] = next_hash_key
        if next_range_key:
            params['next_range_key'] = next_range_key
        if page_size:
            params['page_size'] = page_size

        response = self.session.delete(url, params=params)
        if response.ok:
            json_body = response.json()
            next_hash_key = json_body.get('next_hash_key')
            next_range_key = json_body.get('next_range_key')
            count = json_body.get('count')
            self.logger.info('Cancelled %s Pnl records.', count)
            return next_hash_key, next_range_key, count
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def allocate_transaction(self, asset_manager_id, transaction_id, allocation_type, allocation_dicts):
        """

        :param asset_manager_id:
        :param transaction_id:
        :param allocation_type:
        :param allocation_dicts:
        :return:
        """
        self.logger.info('Allocate Transaction - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/allocations/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        params = {'allocation_type': allocation_type}
        response = self.session.post(url, params=params, data=json.dumps(allocation_dicts, default=json_handler),
                                     headers=self.json_header)
        if response.ok:
            allocations = [json_to_transaction(json_allocation) for json_allocation in response.json()]
            allocation_ids = [allocation.transaction_id for allocation in allocations]
            self.logger.info('%s Allocations Created - Transactions: %s', len(allocations), allocation_ids)
            return allocations
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_transaction_allocations(self, asset_manager_id, transaction_id):
        """

        :param asset_manager_id:
        :param transaction_id:
        :return:
        """
        self.logger.info('Retrieve Allocations - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/allocations/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        response = self.session.get(url)
        if response.ok:
            allocations = [json_to_transaction(json_allocation) for json_allocation in response.json()]
            self.logger.info('Returned %s Allocations.', len(allocations))
            return allocations
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def net_transactions(self, asset_manager_id, transaction_ids, netting_type='Net'):
        """

        :param asset_manager_id: The asset_manager_id of the netting set owner
        :param transaction_ids:  A list of transaction_ids to net
        :param netting_type:
        :return:
        """
        self.logger.info('Net Transactions - Asset Manager: %s - Transaction IDs: %s', asset_manager_id,
                         transaction_ids)
        url = '%s/netting/%s' % (self.endpoint, asset_manager_id)
        params = {'netting_type': netting_type}
        response = self.session.post(url, params=params, json=transaction_ids)
        if response.ok:
            net_transaction = json_to_transaction(response.json())
            self.logger.info('Net Created - Transaction: %s', net_transaction.transaction_id)
            return net_transaction
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def retrieve_netting_set(self, asset_manager_id, transaction_id):
        """
        Returns all the transaction_ids associated with a single netting set.  Pass in the ID for any transaction in
        the set.
        :param asset_manager_id:  The asset_manager_id for the netting set owner.
        :param transaction_id: A transaction_id of an entry within the netting set.
        :return:
        """
        self.logger.info('Retrieve Netting Set - Asset Manager: %s - Transaction ID: %s', asset_manager_id,
                         transaction_id)
        url = '%s/netting/%s/%s' % (self.endpoint, asset_manager_id, transaction_id)
        response = self.session.get(url)
        if response.ok:
            net_transaction_id, netting_set_json = next(iter(response.json().items()))
            netting_set = [json_to_transaction(net_transaction) for net_transaction in netting_set_json]
            self.logger.info('Returned %s Transactions in Netting Set.', len(netting_set))
            return net_transaction_id, netting_set
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def book_transfer(self, asset_manager_id, asset_id, source_book_id, target_book_id, wash_book_id, quantity, price,
                      currency):
        """
        A method for moving between books.  The convention is always *from* the source, *to* the target.

        Two transactions are booked -  one against each

        :param asset_manager_id: The owning asset manager id.
        :param asset_id: The asset being transferred.
        :param source_book_id: The book id of the source.
        :param target_book_id:  The book id of the target.
        :param wash_book_id:  The book id of the wash book which will be the counterparty for the two sides.
        :param quantity: The quantity to transfer.
        :param price:  The price at which to make the transfer.  Typically T-1 EOD price or current market price.
        :param currency: The currency for the transfer price.
        :return:
        """
        url = '%s/book_transfer/%s' % (self.endpoint, asset_manager_id)
        body = {'asset_id': asset_id, 'source_book_id': source_book_id, 'target_book_id': target_book_id,
                'wash_book_id': wash_book_id, 'quantity': quantity, 'price': price, 'currency': currency}
        response = self.session.post(url, data=json.dumps(body, default=json_handler), headers=self.json_header)
        if response.ok:
            deliver_json, receive_json = response.json()
            return json_to_transaction(deliver_json), json_to_transaction(receive_json),
        else:
            self.logger.error(response.text)
            response.raise_for_status()

    def depot_transfer(self, asset_manager_id, asset_id, source_account_id, target_account_id, quantity):
        raise NotImplementedError("""This is not yet supported.  The concept is similar to a
                                  book transfer, except it requires an external message to a
                                  custodian to instruct them to move the stock to a
                                   different depot account.""")

    def clear(self, asset_manager_id, book_ids=None):
        """ This method deletes all the data for an asset_manager_id
            and option book_ids.
            It should be used with extreme caution.  In production it
            is almost always better to Inactivate rather than delete. """
        self.logger.info('Clear Transactions & Positions - Asset Manager: %s', asset_manager_id)
        url = '%s/clear/%s' % (self.endpoint, asset_manager_id)
        params = {'asset_manager_ids': ','.join(book_ids)} if book_ids else {}
        response = self.session.delete(url, params=params)
        if response.ok:
            tran_count = response.json().get('transaction_count', 'Unknown')
            self.logger.info('Deleted %s Transactions.', tran_count)
            pos_count = response.json().get('position_count', 'Unknown')
            self.logger.info('Deleted %s Positions.', pos_count)
            return response.json()
        else:
            self.logger.error(response.text)
            response.raise_for_status()
