import requests
import json


def sendOTP(phoneNumber: str,merchantBearerToken:str, isSandBox:bool = False):
    url = "https://api"+(".sandbox" if(isSandBox) else "")+".pay.meda.chat/v1/amole/otp/" + phoneNumber
    payload = {}
    headers = {
        'Authorization': merchantBearerToken,
        'Cookie': 'next-i18next=en'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text.encode('utf8'))
    if json_response.get("ErrorCode") != "00001":
        raise exec("OTP couldn't be sent")
    return json_response


def payBill(billref: str, phoneNumber: str, otp: str, amount: float,merchantBearerToken:str, isSandBox:bool = False):
    url = "https://api"+(".sandbox" if(isSandBox) else "")+".pay.meda.chat/v1/amole"
    payload = json.dumps({
        "referenceNumber":billref,
        "accountNumber": phoneNumber,
        "otp": otp,
        "amount": amount
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': merchantBearerToken
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text.encode('utf8'))


class AmolePayment():
    avalailable_payment_types = ["airtime"]

    def __init__(self, clientPhone: str, amount: float, billref: str, merchantBearerToken: str, isSandBox: bool = True,
                 otp_sent_callback=None):
        self.phoneNumber = clientPhone
        self.billref = billref
        self.amount = amount
        self.merchantBearerToken = merchantBearerToken
        self.isSandBox = isSandBox
        sendOTP(clientPhone,merchantBearerToken=self.merchantBearerToken
                ,isSandBox=self.isSandBox)
        if otp_sent_callback is not None: otp_sent_callback()

    def verifyPayment(self, otp: str):
        return payBill(billref=self.billref, phoneNumber=self.phoneNumber, otp=otp, amount=self.amount,merchantBearerToken=self.merchantBearerToken
                ,isSandBox=self.isSandBox)
