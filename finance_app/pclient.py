from plaid import Client
from plaid_django.settings import PLAID_CLIENT_ID, PLAID_SECRET

class Pclient:
    __instance = None

    @staticmethod 
    def getInstance():
        if Pclient.__instance == None:
            Pclient()
        return Pclient.__instance

    def __init__(self):
        if Pclient.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Pclient.__instance = Client(
                client_id=PLAID_CLIENT_ID,
                secret=PLAID_SECRET,
                environment='sandbox'
            )
