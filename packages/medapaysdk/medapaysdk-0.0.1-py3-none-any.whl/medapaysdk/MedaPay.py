from medapaysdk import AmolePayment
import requests
import json
from medapaysdk.tokens import  randomToken

config = {}

def getBillDetails(billref,bearerToken, isSandBox) -> (str, str, str, int, str, str, str):
    url = "https://api"+(".sandbox" if(isSandBox) else "")+".pay.meda.chat/v1/bills/" + billref
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearerToken
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text.encode('utf8'))
    if "statusCode" in json_response:
        if json_response["statusCode"] == 404:
            raise exec("Bill not found, use a valid reference number.")
    return json_response.get("referenceNumber"), \
           json_response.get("accountNumber"), \
           json_response.get("status"), \
           json_response.get("amount"), \
           json_response.get("customerName"), \
           json_response.get("createdAt"), \
           json_response.get("description")        



def createBill(phoneNumber: str, name: str, amount: float, merchantBearerToken: str = None, method = None, description = None, isSandBox = True) -> (str, str):
    orderId = "order_" + randomToken()
    url = "https://api"+(".sandbox" if(isSandBox) else "")+".pay.meda.chat/v1/bills"
    payload = json.dumps({
        'purchaseDetails': {
            'orderId': orderId,
            'description': description if(description != None) else f"Buy {amount} birr worth of materials for {name}",
            'amount': (amount) + 0.0,
            'customerName': name,
            'customerPhoneNumber': phoneNumber
        },
        'redirectUrls': {
            'returnUrl': "NaN",
            'cancelUrl': "NaN",
            'callbackUrl': "NaN" if(config['current_url'] == None) else config['current_url']+f"payment?verification={config['verificationToken']}&type={method}&orderId={orderId}&status=CALLBACK",
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': merchantBearerToken
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text.encode('utf8'))
    if "billReferenceNumber" not in json_response:
        raise exec(f"Bill Error :{json_response}")
    return orderId, json_response.get("billReferenceNumber")


class MedaPay:

    def __init__(self, isSandBox=True,merchantBearerToken=None, callbackWebhook:str =None, callbackVerifyToken:str= None ):
        if(merchantBearerToken==None):
            raise Exception('Merchant bearer token should be specified') 
        self.merchantBearerToken = merchantBearerToken
        self.isSandBox = isSandBox
        config["current_url"] = callbackWebhook
        config["verificationToken"] = callbackVerifyToken

    def getBillDetails(self, billref: str) -> (str,str,str,int, str, str, str):
        return getBillDetails(billref, self.merchantBearerToken, self.isSandBox)

    # This is used to initiate a amole instance
    def amole(self, name: str, clientPhone: str, amount: float,
              description=None,otp_sent_callback=None) -> (str,str,AmolePayment):
        orderId, billref = createBill(clientPhone, name, amount, method= "Amole",description=description, merchantBearerToken=self.merchantBearerToken, isSandBox=self.isSandBox)
        return orderId, billref, AmolePayment.AmolePayment(clientPhone=clientPhone, amount=amount, billref=billref,
                                         otp_sent_callback=otp_sent_callback,merchantBearerToken=self.merchantBearerToken,isSandBox=self.isSandBox)

    # This is used to initiate a amole instance for a bill
    def amoleBill(self, billref: str, phoneNumber,otp_sent_callback=None) -> AmolePayment:
        referenceNumber, accountNumber, status, amount, issuerName, createdAt, description = getBillDetails(billref, self.merchantBearerToken, self.isSandBox)
        if status == "PENDING":
            return AmolePayment.AmolePayment(
                clientPhone=phoneNumber, amount=amount,
                billref=billref,
                otp_sent_callback=otp_sent_callback,
                merchantBearerToken=self.merchantBearerToken
                ,isSandBox=self.isSandBox
                                             )
        else:
            raise exec("Status isn't PENDING it's already paid or canceled")
    
    def createBill(self, clientPhone: str, amount: float, name: str, method = None, description=None):
        orderId, billref = createBill(clientPhone, name, amount, self.merchantBearerToken, method=method,description=description,isSandBox=self.isSandBox)
        return  orderId, billref 
                                                          

        


   # def mBirrBill(self, name: str, clientPhone: str, amount: float, type: str,
    #          otp_sent_callback=None, toPhoneNumber: str = None):