from __future__ import absolute_import, division, print_function, unicode_literals

CASH_TRANSACTION_TYPES = {'Cashflow', 'Coupon', 'Dividend', 'Payment'}
TRANSACTION_TYPES = {'Allocation', 'Block', 'Exercise', 'Expiry', 'Journal', 'Maturity', 'Net',
                     'Novation', 'Split', 'Trade', 'Transfer', 'Settlement'} | CASH_TRANSACTION_TYPES
TRANSACTION_INVESTOR_ACTIONS = {'Subscription', 'Redemption'}
TRANSACTION_LIFECYCLE_ACTIONS = {'Acquire', 'Remove'}
TRANSACTION_ACTIONS = {'Buy', 'Sell', 'Short Sell', 'Short Cover', 'Deliver', 'Receive'} | \
                      TRANSACTION_LIFECYCLE_ACTIONS | TRANSACTION_INVESTOR_ACTIONS
TRANSACTION_ACQUIRE_ACTIONS = {'Buy', 'Short Cover', 'Receive', 'Acquire', 'Redemption'}
TRANSACTION_REMOVE_ACTIONS = {'Sell', 'Short Sell', 'Deliver', 'Remove', 'Subscription'}
TRANSACTION_CANCEL_STATUSES = {'Cancelled', 'Netted', 'Novated'}
TRANSACTION_STATUSES = {'New', 'Amended', 'Superseded'} | TRANSACTION_CANCEL_STATUSES
ACCOUNTING_TYPES = {'Transaction Date', 'Settlement Date'}
