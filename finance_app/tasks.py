from datetime import datetime
from datetime import timedelta
from celery import shared_task

from .models import Item, Transaction, Account
from .serializers import AccountSerializer, TransactionSerializer
from .pclient import Pclient
from .utils import clean_accounts_data

client = Pclient.getInstance()

@shared_task
def delete_transactions_from_db(item_id, removed_transactions):

    for trans_id in removed_transactions:
        Transaction.objects.filter(transaction_id=trans_id).delete()
    
    return "Transactions removed"

@shared_task
def save_transactions_to_db(item_id, new_transactions):
    item = Item.objects.filter(item_id=item_id)
    access_token = item[0].access_token

    # fetching all the transactions of last 2 years
    start_dt = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    end_dt = datetime.now().strftime("%Y-%m-%d")

    response = client.Transactions.get(access_token, start_date=start_dt, end_date=end_dt, count=new_transactions)
    
    accounts = clean_accounts_data(item[0].pk, response['accounts'])
    # print("accounts", accounts)
    accnts = Account.objects.filter(item_id=item)

    # Update records in accounts table
    for acc in accnts:
        account_value = next((elem for elem in accounts if elem["account_id"] == acc.account_id), None)
        
        # print("account_value", account_value)
        if account_value:
            accnts.filter(account_id=acc.account_id).update(
                available_balance=account_value['available_balance'],
                current_balace=account_value['current_balace'],
                name=account_value['name'],
                account_type=account_value['account_type'],
                account_subtype=account_value['account_subtype']
            )
    
    # Save new records in accounts table
    save_accounts = []
    for acc in accounts:
        
        if not accnts.filter(account_id=acc['account_id']).exists():
            save_accounts.append(acc)
    
    # print("save_accounts", save_accounts)

    acc_serializer = AccountSerializer(data=save_accounts, many=True)
    acc_serializer.is_valid(raise_exception=True)
    acc_serializer.save()

    
    transactions = response['transactions']
    # print("transactions", transactions)
    trans_id = [trans['transaction_id'] for trans in transactions]

    trans = Transaction.objects.filter(transaction_id__in=trans_id)

    # Update records in transactions table
    for tran in trans:
        trans_value = next((elem for elem in transactions if elem["transaction_id"] == tran.transaction_id), None)
        # print("trans_value", trans_value)
        if trans_value:
            trans.filter(transaction_id=tran.transaction_id).update(
                amount=trans_value['amount'],
                date=trans_value['date'],
                name=trans_value['name'],
                payment_channel=trans_value['payment_channel']
            )

    # Save new records in transactions table
    save_transactions = []
    for tran in transactions:

        if not trans.filter(transaction_id=tran['transaction_id']).exists():
            tran['account_id'] = Account.objects.filter(account_id=tran['account_id'])[0].pk
            # print("tran",tran)
            save_transactions.append(tran)

    # print("save_transactions", save_transactions)

    tr_serializer = TransactionSerializer(data=save_transactions, many=True)
    tr_serializer.is_valid(raise_exception=True)
    tr_serializer.save()

    print("DB entries updated")

    return "DB entries saved and updated"