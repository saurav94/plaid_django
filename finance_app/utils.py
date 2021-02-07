
def clean_accounts_data(item_id, accounts):
    accounts_data = []

    for acc in accounts:
        data = {}
        data['item_id'] = item_id
        data['account_id'] = acc['account_id']

        if not 'balances' in acc:
            acc['balances'] = {}
            acc['balances']['available'] = 0
            acc['balances']['current'] = 0

        if acc['balances']['available'] is None:
            acc['balances']['available'] = 0
        if acc['balances']['current'] is None:
            acc['balances']['current'] = 0

        if not 'name' in acc or acc['name'] is None:
            acc['name'] = ""
        if not 'type' in acc or acc['type'] is None:
            acc['type'] = ""
        if not 'subtype' in acc or acc['subtype'] is None:
            acc['subtype'] = ""

        data['available_balance'] = acc['balances']['available']
        data['current_balace'] = acc['balances']['current']
        data['name'] = acc['name']
        data['account_type'] = acc['type']
        data['account_subtype'] = acc['subtype']

        accounts_data.append(data)
    
    return accounts_data