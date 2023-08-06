from __future__ import absolute_import, division, print_function, unicode_literals
import inspect

from amaascore.transactions.cash_transaction import CashTransaction
from amaascore.transactions.enums import CASH_TRANSACTION_TYPES
from amaascore.transactions.position import Position
from amaascore.transactions.transaction import Transaction
from amaascore.transactions.mtm_result import MTMResult
from amaascore.transactions.transaction_pnl import TransactionPNL
from amaascore.transactions.position_pnl import PositionPNL
from amaascore.transactions.book_report import BookReport
from amaascore.transactions.pnl import Pnl

def json_to_position(json_position):
    position = Position(**json_position)
    return position


def json_to_transaction(json_transaction):
    # Iterate through the Transaction children, converting the various JSON attributes into the relevant class type
    for (collection_name, clazz) in Transaction.children().items():
        children = json_transaction.pop(collection_name, {})
        collection = {}
        for (child_type, child_json) in children.items():
            # Handle the case where there are multiple children for a given type - e.g. links
            if isinstance(child_json, list):
                child = set()
                for child_json_in_list in child_json:
                    child.add(clazz(**child_json_in_list))
            else:
                child = clazz(**child_json)
            collection[child_type] = child
        json_transaction[collection_name] = collection
    transaction_type = json_transaction.get('transaction_type')
    clazz = CashTransaction if transaction_type in CASH_TRANSACTION_TYPES else Transaction
    args = inspect.getargspec(clazz.__init__)
    # Some fields are always added in, even though they're not explicitly part of the constructor
    clazz_args = args.args + clazz.amaas_model_attributes()
    # is not None is important so it includes zeros and False
    constructor_dict = {arg: json_transaction.get(arg) for arg in clazz_args
                        if json_transaction.get(arg) is not None and arg != 'self'}
    transaction = clazz(**constructor_dict)
    return transaction


def json_to_mtm_result(mtm_result_json):
    args = inspect.getfullargspec(MTMResult.__init__)
    mandatory = set(args.args[1:len(args.args) - len(args.defaults)])
    missing = mandatory - \
        set([attr for attr in mandatory if mtm_result_json.get(attr) is not None])
    if not missing:
        return MTMResult(**mtm_result_json)
    else:
        raise ValueError("Missing Fields: %s in class: MTMResult" %
                         ",".join(missing))

    
def json_to_transaction_pnl(transaction_pnl_json):
    args = inspect.getfullargspec(TransactionPNL.__init__)
    mandatory = set(args.args[1:len(args.args) - len(args.defaults)])
    missing = mandatory - \
        set([attr for attr in mandatory if transaction_pnl_json.get(attr) is not None])
    if not missing:
        return TransactionPNL(**transaction_pnl_json)
    else:
        raise ValueError("Missing Fields: %s in class: TransactionPNL" %
                         ",".join(missing))


def json_to_position_pnl(position_pnl_json):
    args = inspect.getfullargspec(PositionPNL.__init__)
    mandatory = set(args.args[1:len(args.args) - len(args.defaults)])
    missing = mandatory - \
        set([attr for attr in mandatory if position_pnl_json.get(attr) is not None])
    if not missing:
        return PositionPNL(**position_pnl_json)
    else:
        raise ValueError("Missing Fields: %s in class: PositionPNL" %
                         ",".join(missing))

def json_to_pnl(pnl_json):
    args = inspect.getfullargspec(Pnl.__init__)
    mandatory = set(args.args[1:len(args.args) - len(args.defaults)])
    missing = mandatory - set([attr for attr in mandatory if pnl_json.get(attr) is not None])
    if not missing:
        return Pnl(**pnl_json)
    else:
        raise ValueError("Missing Fields: %s in class: Pnl" % ",".join(missing))

def json_to_book_report(book_report_json):
    args = inspect.getfullargspec(BookReport.__init__)
    mandatory = set(args.args[1:len(args.args) - len(args.defaults)])
    missing = mandatory - \
        set([attr for attr in mandatory if book_report_json.get(attr) is not None])
    if not missing:
        return BookReport(**book_report_json)
    else:
        raise ValueError("Missing Fields: %s in class: BookReport" %
                         ",".join(missing))