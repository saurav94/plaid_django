from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from datetime import timedelta

from .models import Item, Transaction, Account
from .serializers import TransactionSerializer, AccountSerializer
from .pclient import Pclient
from .utils import clean_accounts_data
from .webhook_tasks import save_transactions_to_db, delete_transactions_from_db
from plaid_django.settings import NGROK_ID

client = Pclient.getInstance()

def home(request):
    return HttpResponse('<h1>Finance app on Django rest framework using plaid apis</h2>')


class PublicTokenCreate(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # institution_id = ins_109512
        institution_id = request.data['institution_id']

        res = client.Sandbox.public_token.create(
            institution_id=institution_id,
            initial_products=['transactions'],
            webhook="http://" + NGROK_ID + ".ngrok.io/webhook_transactions/"
        )
        
        public_token = res['public_token']
        print(public_token)
        
        data = {
            "public_token": public_token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class AccessTokenCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        global access_token, item_id
        public_token = request.data['public_token']

        response = client.Item.public_token.exchange(public_token)
        access_token = response['access_token']
        item_id = response['item_id']
        print(access_token, item_id)
        
        item = Item.objects.create(user=self.request.user, item_id=item_id, access_token=access_token)
        item.save()

        data = {
            "access_token": access_token,
            "item_id": item_id
        }
        return Response(data, status=status.HTTP_201_CREATED)


class TransactionsGet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Item.objects.filter(user=self.request.user)
        access_token = item[0].access_token

        start_dt = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        end_dt = datetime.now().strftime("%Y-%m-%d")

        response = client.Transactions.get(access_token, start_date=start_dt, end_date=end_dt)
        transactions = response['transactions']

        for trans in transactions:
            trans['account_id'] = Account.objects.filter(account_id = trans['account_id'])[0].pk

        serializer = TransactionSerializer(data=transactions, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountBalance(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Item.objects.filter(user=self.request.user)
        access_token = item[0].access_token

        # Pull real-time balance information for each account associated with the Item
        response = client.Accounts.balance.get(access_token)

        accounts = clean_accounts_data(item[0].pk, response['accounts'])
        
        serializer = AccountSerializer(data=accounts, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class WebhookTransactions(APIView):
    def post(self, request):
        data = request.data

        webhook_type = data['webhook_type']
        webhook_code = data['webhook_code']

        print(f"{webhook_type} Webhook received. Type {webhook_code}")

        if webhook_type == "TRANSACTIONS":
            item_id = data['item_id']
            if webhook_code == "TRANSACTIONS_REMOVED":
                removed_transactions = data['removed_transactions']
                delete_transactions_from_db(item_id, removed_transactions)
            else:
                new_transactions = data['new_transactions']
                print("New transaction: ", new_transactions)

                if new_transactions == 0: new_transactions=50
                save_transactions_to_db(item_id, new_transactions)
        
        return HttpResponse("Webhook received", status=status.HTTP_202_ACCEPTED)


class WebhookTest(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        item = Item.objects.filter(user=self.request.user)
        access_token = item[0].access_token

        # fire a DEFAULT_UPDATE webhook for an item
        res = client.Sandbox.item.fire_webhook(access_token, 'DEFAULT_UPDATE')

        print("Webhook fired: ", res['webhook_fired'])

        return Response({"message": "Webhook fired"}, status=status.HTTP_200_OK)

