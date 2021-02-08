# plaid_django
Finance app on Django rest framework using plaid apis

## Django rest Apis for signup, login and logout

`api/register/` - Create user using username, email and password

`api/login/` - Login using username and password

`api/logout/` - Logout using knox token

## Fetch and store data from Plaid Apis

`get_public_token/` - Get public token from Plaid

`get_access_token/` - Exchange public token with access token

`get_transactions/` - Get transactions from plaid api

`get_transactions_from_db/` - Get transactions saved in db

`get_account_balance/` - Get account details from plaid api

`get_account_balance_from_db/` - Get account details saved in db


## Webhooks
    
`webhook_test/` - Fire a test sandbox webhook 

`webhook_transactions/` - Transactions Webhook 



- Async tasks handled by celery usig RabbitMQ broker
- Localhost exposed using ngrox

