# -*- coding: utf-8 -*-
# from sqlalchemy.exc import SADeprecationWarning

from nps_sdk.constants import PRODUCTION_ENV, STAGING_ENV, SANDBOX_ENV, DEVELOPMENT_ENV
from nps_sdk.errors import ApiException
import nps_sdk
import logging

# prod_mer_id = "aeroarg_web"
merchant_id = "psp_test"
# merchant_id = "sdk_test"
#merchant_id = "365online"

nps_sdk.Configuration.configure(environment=DEVELOPMENT_ENV,
                                # secret_key="zqyHQTpFxTmIVKeFYAgw2RhqyJI6gCVd2SuRvjeqBQ8gimtHuXDwztnvC5ztGVUG", # prod key aeroarg_web
                                # secret_key="swGYxNeehNO8fS1zgwvCICevqjHbXcwPWAvTVZ5CuULZwKWaGPmXbPSP8i1fKv2q", #sdk_test
                                secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6", #psp_test
                                #secret_key="xfMzDG2gDMwYABT3JWUmkH14i3uwXMTW2hI2GIomhxq3FORdhDs9EDSAeqRQJmMt", #365online
                                #secret_key="wDbxnRDvF3wmcETN9bih7j4R9FhC3PczaBuNd7JqAFalR38adqGiYKAfZpsbCSYm", #inclufin
                                #secret_key="0NdyJ37jbRqUnw5ATJoDbkq52WYv9BY8YC6qDCZodNIOJLYmcL0D5oG5Kp0R0WZZ",
                                log_level=logging.INFO, debug=True, cert_verify_peer=False, cert=False, timeout=30, cache=True, cache_location='/tmp', cache_ttl=86400, as_obj=True)

"""PayOnLine_2p"""


def run_payOnline_2p():
    sdk = nps_sdk.Nps()
    import uuid
    unicid = uuid.uuid4()
    params ={
        'psp_MerchOrderId': unicid,
        'psp_MerchTxRef': unicid,
        'psp_PosDateTime': '2017-03-31 16:14:06',
        'psp_NumPayments': '1',
        # 'psp_Currency': '032',
        # 'psp_Country': 'ARG',
        'psp_Currency': '986',
        'psp_Country': 'BRA',



        'psp_TxSource': 'WEB',


        #Cielo

        # "psp_CardNumber": '4012123412341231',
        # "psp_CardExpDate": '2112',
        # "psp_CardSecurityCode": '123',
        # # 'psp_ForceProcessingMethod': 11, #CIELO
        # 'psp_Product': '14',

        # 'psp_ForceProcessingMethod': 20, #ELAVON BR
        # 'psp_ForceProcessingMethod': 11, #CIELO

        # "psp_CardNumber": '5448280000000007',
        # "psp_CardExpDate": '1901',
        # "psp_CardSecurityCode": '132',
        # 'psp_Product': '5',
        # 'psp_ForceProcessingMethod': 32, #eRede


        #GetNet Visa
        "psp_CardNumber": '4012001037141112',
        "psp_CardExpDate": '1904',
        "psp_CardSecurityCode": '456',
        'psp_ForceProcessingMethod': 33,
        'psp_Product': '14',
        # "psp_SoftDescriptor": "mariaconchitaÀ",
        # "psp_Plan" : "DEBIT",

        # GetNet Master
        # "psp_CardNumber": '5453010000083303',
        # "psp_CardExpDate": '1904',
        # "psp_CardSecurityCode": '321',
        # 'psp_ForceProcessingMethod': 33,
        # 'psp_Product': '5',
        # # "psp_Plan" : "CC",

        #'psp_Product': '5',
        #"psp_CardNumber": '5453010000083303',
        #"psp_CardExpDate": '1904',
        #"psp_CardSecurityCode": '456',


        #amex
        # "psp_CardNumber": '376442058032004',
        # "psp_CardExpDate": '2307',
        # "psp_CardSecurityCode": '1589',
        # 'psp_ForceProcessingMethod': 33,
        # 'psp_Product': '1',
        "psp_SoftDescriptor": "mariaconchitaÀ",

        #elo
        # "psp_CardNumber": '5067230000009011',
        # "psp_CardExpDate": '2110',
        # "psp_CardSecurityCode": '568',
        # 'psp_ForceProcessingMethod': 33,
        # 'psp_Product': '102',


        # 'psp_Recurrent': '1',
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_Amount': "1000",
        # "psp_CardHolderName": "Gustavo Diaz",
        "psp_PurchaseDescription": "Gusta",
        # Todo lo que tiene taxes esta siendo rechazado con el error CGW000315-Action Not Enabled for Terminal
        # "psp_AmountAdditionalDetails": {
        #     "Taxes": [
        #         {
        #             "TypeId": "100",
        #             "Amount": "20000"
        #         }]
        # },
        # "psp_NumPayments": "2",
        # "psp_Plan": "CC",

        #"psp_3dSecure_XID" : "amNkRGhHaFUxYXUyckxnaEZaNzE=",
        #"psp_3dSecure_CAVV" : "BwABCVhFYQAAAAB4ZEVhAAAAAAA=",
        #"psp_3dSecure_ECI" : "5",
        # 'psp_VaultReference': {
        #         'PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken
        #    # 'PaymentMethodToken': '6uItgIBjWsnG3UpleZX70RQlOpJTJ3wm'
        #
        # }




    }

    try:
        resp = sdk.pay_online_2p(params)
        return resp
    except ApiException as e:
        print(e.message)#Code to handle error
        pass


def run_Authorize_2p():
    """Authorize_2p"""
    sdk = nps_sdk.Nps()
    import uuid
    myid = uuid.uuid4()
    params = {
            "psp_Version": '2.2',
            "psp_MerchantId": 'psp_test',
            "psp_TxSource": 'WEB',
            "psp_MerchTxRef": myid,
            "psp_MerchOrderId": myid,
            "psp_Amount": '15050',
            "psp_NumPayments": '1',
            'psp_Currency': '986',
            "psp_Country": 'BRA',

            'psp_Amount': "50000",

            # "psp_Plan": "CC",
            #Cielo
            #"psp_CardNumber": '4012123412341231',
            #"psp_CardExpDate": '2112',
            #"psp_CardSecurityCode": '123',
            #'psp_ForceProcessingMethod': 11,  # CIELO



            # elo
            "psp_CardNumber": '5067230000009011',
            "psp_CardExpDate": '2110',
            "psp_CardSecurityCode": '568',
            "psp_Product": '102',


            # hipercard
            # "psp_CardNumber": '3841000000004',
            # "psp_CardExpDate": '1907',
            # "psp_CardSecurityCode": '123',
            # "psp_Product": '105',

            # amex
            # "psp_CardNumber": '376442058032004',
            # "psp_CardExpDate": '2307',
            # "psp_CardSecurityCode": '1589',
            # "psp_Product": '1',



            #getnet visa
            # "psp_CardNumber": '4012001038166662',
            # "psp_CardExpDate": '1907',
            # "psp_CardSecurityCode": '123',
            # "psp_Product": '14',



        'psp_ForceProcessingMethod': 33,
            "psp_CardHolderName": "Gustavo Diaz",
            #"psp_3dSecure_XID": "amNkRGhHaFUxYXUyckxnaEZaNzE=",
            #"psp_3dSecure_CAVV": "BwABCVhFYQAAAAB4ZEVhAAAAAAA=",
            #"psp_3dSecure_ECI": "5",
            #"psp_CardSecurityCode": '123',
            #"psp_CardHolderName": "Gustavo Diaz",
            #"psp_PurchaseDescription": "Juguetes",
            #"psp_ForceProcessingMethod": 31,
            "psp_PosDateTime": '2017-04-04 13:35:20',

            # "psp_AmountAdditionalDetails" :{
            #    "Taxes":[
            #    {
            #           "TypeId": "100",
            #           "Amount": "50"
            #             }]
            #  },

            #'psp_ForceProcessingMethod': 44 #CIELO
            #'psp_ForceProcessingMethod': 20 #ELAVON BR

            # "psp_VaultReference":{
            #    "PaymentMethodToken": "PyyaRXCxk1iyqKv3glGRW8QY1adQdE9H",
            # }
        }
    # params = {
    #     "psp_Version": "2.2",
    #     "psp_MerchantId": "psp_test",
    #     "psp_TxSource": "WEB",
    #     "psp_MerchTxRef": myid,
    #     "psp_MerchOrderId": "ORDERX1466Xz",
    #     "psp_Amount": "15050",
    #     "psp_NumPayments": "1",
    #     "psp_Currency": "032",
    #     "psp_Country": "ARG",
    #     "psp_Product": "14",
    #     "psp_CardNumber": "4507990000000010",
    #     "psp_CardExpDate": "1912",
    #     "psp_PosDateTime": "2019-12-01 12:00:00",
    #     "psp_AirlineDetails": {
    #         "PNR": "154DDD54DWW11",
    #         "Legs": [{
    #             "DepartureAirport": "EZE",
    #             "DepartureDatetime": "2014-05-12 13:05:00",
    #             "DepartureAirportTimezone": "-03:00",
    #             "ArrivalAirport": "AMS",
    #             "CarrierCode": "KL",
    #             "FlightNumber": "842",
    #             "FareBasisCode": "HL7LNR",
    #             "FareClassCode": "FR",
    #             "BaseFare": "30000",
    #             "BaseFareCurrency": "032"
    #         }],
    #         "Passengers": [{
    #             "FirstName": "John",
    #             "LastName": "Doe",
    #             "MiddleName": "Michael",
    #             "Type": "A",
    #             "DateOfBirth": "1979-01-12",
    #             "Nationality": "ARG",
    #             "IDNumber": "54111111",
    #             "IDType": "100",
    #             "IDCountry": "ARG",
    #             "LoyaltyNumber": "254587547",
    #             "LoyaltyTier": "1"
    #         }],
    #         "Ticket": {
    #             "TicketNumber": "07411865255578",
    #             "Eticket": "1",
    #             "Restricted": "1",
    #             "Issue": {
    #                 # "CarrierCode": "AA",
    #                 "TravelAgentCode": "32165464",
    #                 "TravelAgentName": "Washington Hilton",
    #                 "Date": "2017-01-10",
    #                 "Country": "ARG",
    #                 "City": "Buenos Aires",
    #                 "Address": "Av. Rivadavia 1111"
    #             },
    #             "TotalFareAmount": "80000",
    #             "TotalTaxAmount": "25200",
    #             "TotalFeeAmount": "14800"
    #         }
    #     }}
    try:
        resp = sdk.authorize_2p(params)
    except ApiException as e:
        print e.message
        pass
    return resp

def run_PayOnline_3p():
    """PayOnLine_3p"""
    import uuid
    order = uuid.uuid4()
    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": order,
        "psp_MerchOrderId": order,
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_NumPayments": '1',
        'psp_Currency': '986',
        "psp_Country": 'BRA',
        "psp_Product": '14',
        'psp_Amount': '1000',
        'psp_ForceProcessingMethod': 33
    }

    resp = sdk.pay_online_3p(params)
    return resp



def run_Authorize_3p():
    """Authorize_3p"""
    import uuid
    sdk = nps_sdk.Nps()
    order = uuid.uuid4()
    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": order,
        "psp_MerchOrderId": order,
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_NumPayments": '1',
        'psp_Currency': '986',
        "psp_Country": 'BRA',
        "psp_Product": '14',
        'psp_Amount': '1000',
        'psp_ForceProcessingMethod': 33
    }

    resp = sdk.authorize_3p(params)
    return resp


def run_SplitPayOnline_3p():
    """SplitPayOnLine_3p"""
    import uuid
    order = uuid.uuid4()
    order2 = uuid.uuid4()
    order3 = uuid.uuid4()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": order,
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        # "psp_Currency": '032',
        # "psp_Country": 'ARG',

        "psp_Product": 14,
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [{
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order2,
            "psp_Product": 14,
            "psp_Amount": 10000,
            "psp_NumPayments": 1
        },{
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order3,
            "psp_Product": 14,
            "psp_Amount": 5050,
            "psp_NumPayments": 1
        }],
        'psp_ForceProcessingMethod': 33
        # 'psp_ForceProcessingMethod': 20  # ELAVON BR
        # "psp_CardNumber": '4012123412341231',
        # "psp_CardExpDate": '2112',
        # "psp_CardSecurityCode": '123',
        # 'psp_ForceProcessingMethod': 32 #CIELO
        # 'psp_ForceProcessingMethod': 16  # CIELO
    }

    resp = sdk.split_pay_online_3p(params)
    return resp


def run_SplitAuthorize_3p():
    """SplitAuthorize_3p"""
    import uuid
    order = uuid.uuid4()
    order2 = uuid.uuid4()
    order3 = uuid.uuid4()

    sdk = nps_sdk.Nps()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": order,
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [{
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order2,
            "psp_Product": 14,
            "psp_Amount": 10000,
            "psp_NumPayments": 1
        }, {
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order3,
            "psp_Product": 14,
            "psp_Amount": 5050,
            "psp_NumPayments": 1
        }],
        'psp_ForceProcessingMethod': 33
    }

    resp = sdk.split_authorize_3p(params)
    return resp


def run_SplitAuthorize_2p():
    """SplitAuthorize_3p"""
    import uuid
    order = uuid.uuid4()
    order2 = uuid.uuid4()
    order3 = uuid.uuid4()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": order,
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '4012001038166662',
        "psp_CardExpDate": '1906',
        "psp_CardHolderName": "Gustavo Diaz",
        # "psp_CardSecurityCode": '123',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [{
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order2,
            "psp_Product": 14,
            "psp_Amount": 10000,
            "psp_NumPayments": 1
            #"psp_CardNumber": '4012001038166662',
            #"psp_CardExpDate": '1906',
            # "psp_CardSecurityCode": '123',
        }, {
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order3,
            "psp_Product": 14,
            "psp_Amount": 5050,
            "psp_NumPayments": 1,
            "psp_VaultReference":{
                "PaymentMethodToken": run_create_payment_method_token().psp_PaymentMethodToken
            }
            #"psp_CardNumber": '4012001038166662',
            #"psp_CardExpDate": '1906',
            # "psp_CardSecurityCode": '123',
        }],
        'psp_ForceProcessingMethod': 33
    }

    resp = sdk.split_authorize_2p(params)
    return resp

def run_SplitPayOnline_2p():
    """run_SplitPayOnline_2p"""
    import uuid
    order = uuid.uuid4()
    order2 = uuid.uuid4()
    order3 = uuid.uuid4()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": order,
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '4012001038166662',
        "psp_CardExpDate": '1906',
        "psp_CardHolderName": "Gustavo Diaz",
        'psp_Recurrent': 1,
        # "psp_CardSecurityCode": '123',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [{
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order2,
            "psp_Product": 14,
            "psp_Amount": 10000,
            "psp_NumPayments": 1,

            #"psp_CardNumber": '4012001038166662',
            #"psp_CardExpDate": '1906',
            # "psp_CardSecurityCode": '123',
        }, {
            "psp_MerchantId": merchant_id,
            "psp_MerchTxRef": order3,
            "psp_Product": 14,
            "psp_Amount": 5050,
            "psp_NumPayments": 1
            #"psp_CardNumber": '4012001038166662',
            #"psp_CardExpDate": '1906',
            # "psp_CardSecurityCode": '123',
        }],
        'psp_ForceProcessingMethod': 33
    }

    resp = sdk.split_pay_online_2p(params)
    return resp


def run_CashPayment_3p():
    """CashPayment_3p"""
    
    

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": 'ORDER32145-3',
        "psp_MerchOrderId": 'ORDER32145',
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_Amount": 15050,
        "psp_Currency": '032',
        "psp_Country": 'ARG',
        "psp_Product": 301,
        "psp_FirstExpDate": '2016-12-01',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.cash_payment_3p(params)
    return resp


def run_BankPayment_3p():
    """BankPayment_3p"""
    import uuid
    order = uuid.uuid4()

    sdk = nps_sdk.Nps()

    # params = {
    #     "psp_Version": '2.2',
    #     "psp_MerchantId": 'psp_test',
    #     "psp_TxSource": 'WEB',
    #     "psp_MerchTxRef": 'ORDER36675-3',
    #     "psp_MerchOrderId": 'ORDER36675',
    #     "psp_ReturnURL": 'http://localhost/',
    #     "psp_FrmLanguage": 'es_AR',
    #     "psp_ScreenDescription": 'Descripcion',
    #     "psp_TicketDescription": 'Descripcion',
    #     "psp_Currency": '032',
    #     "psp_Country": 'ARG',
    #     "psp_Product": 320,
    #     "psp_ExpDate1": '2016-12-01',
    #     "psp_Amount1": 15050,
    #     "psp_ExpMark": 0,
    #     "psp_ExpTime": '14:00:00',
    #     "psp_PosDateTime": '2016-12-01 12:00:00'
    # }

    # 26873998

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': prod_mer_id,
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': order,
        'psp_MerchOrderId': 'ORDER99998',
        'psp_ReturnURL': 'http://localhost/',
        'psp_FrmLanguage': 'es_AR',
        'psp_ScreenDescription': 'Descripcion',
        'psp_TicketDescription': 'Descripcion',
        'psp_Currency': '032',
        'psp_Country': 'ARG',
        'psp_Product': '320',
        'psp_ExpDate1': '2018-05-30',
        'psp_Amount1': '100',
        'psp_ExpMark': '0',
        'psp_ExpTime': '14:00:00',
        'psp_PosDateTime': '2018-05-29 10:20:00'
    }

    resp = sdk.bank_payment_3p(params)
    return resp


def run_Capture():
    """Capture"""
    sdk = nps_sdk.Nps()
    import uuid
    fuck = uuid.uuid4()
    # from time import sleep
    auth_resp = run_Authorize_2p()
    # sleep(60)
    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": fuck,
        # "psp_TransactionId_Orig": 158871,
        "psp_TransactionId_Orig": auth_resp.psp_TransactionId,
        "psp_AmountToCapture": 50000,
        # "psp_AmountToCapture": 1,
        "psp_PosDateTime": '2017-12-01 12:00:00'
    }

    resp = sdk.capture(params)
    return resp


def run_Refund(withP2p=False, isAuth=False):
    """Refund"""
    import uuid
    id = uuid.uuid4()
    
    sdk = nps_sdk.Nps()

    if withP2p:
        req_resp = run_payOnline_2p()
    else:
        if isAuth:
            req_resp = run_Authorize_2p()
        else:
            req_resp = run_Capture()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": id,
        # "psp_TransactionId_Orig": 159048,
        "psp_AmountToRefund": 500,
        "psp_TransactionId_Orig": req_resp.psp_TransactionId,
        #"psp_AmountToRefund": cap_resp.psp_CapturedAmount if cap_resp else auth_resp.psp_Amount,
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.refund(params)
    return resp


def run_SimpleQuery_Tx():
    """SimpleQuery_Tx"""
    
    
    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_QueryCriteria": 'T',
        "psp_QueryCriteriaId": '156961',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.simple_query_tx(params)
    return resp


def run_QueryTxs():
    """QueryTxs"""
    
    
    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_QueryCriteria": 'T',
        "psp_QueryCriteriaId": '156836',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }
    resp = sdk.query_txs(params)
    return resp

def run_ChangeSecretKey():
    """ChangeSecretKey"""
    

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_NewSecretKey": 'P1SPiAVp3TtAvWFdLceTvlftm2QO5TFUShr9sNytqp1jJGLcsz4nljeVk3rpW6Hw',
        "psp_SecureHash": 'P1SPiAVp3TtAvWFdLceTvlftm2QO5TFUShr9sNytqp1jJGLcsz4nljeVk3rpW6Hw',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.change_secret_key(params)
    return resp


def run_FraudScreening():
    """FraudScreening"""
    

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": 'ORDER66666-3',
        "psp_MerchOrderId": 'ORDER66666',
        "psp_Amount": 15050,
        "psp_NumPayments": 1,
        "psp_Currency": '032',
        "psp_Country": 'ARG',
        "psp_Product": 14,
        "psp_CardNumber": 4507990000000010,
        "psp_CardExpDate": 1612,
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.fraud_screening(params)
    return resp


def run_NotifyFraudScreeningReview():
    """NotifyFraudScreeningReview"""
    

    sdk = nps_sdk.Nps()


    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_Criteria": 'T',
        "psp_CriteriaId": "ORDER66666",
        "psp_ReviewResult": 'A',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    resp = sdk.notify_fraud_screening_review(params)

    return resp


def run_QueryCardNumber():
    """QueryCardNumber"""
    

    sdk = nps_sdk.Nps()

    params = {
        'psp_Version' : '2.2',
        'psp_MerchantId' : 'psp_test',
        'psp_QueryCriteria': 'O',
        'psp_QueryCriteriaId': '100400',
        'psp_PosDateTime' : '2017-12-01 12:00:00'
    }

    resp = sdk.query_card_number(params)

    return resp


def run_GetIINDetails():
    """GetIINDetails"""
    

    sdk = nps_sdk.Nps()

    params = {
        'psp_Version' : '2.2',
        'psp_MerchantId' : 'psp_test',
        'psp_IIN' : '424242',
        'psp_PosDateTime' : '2016-12-01 12:00:00'
    }
    resp = sdk.get_iin_details(params)

    return resp


def run_create_client_session():
    """CreateClientSession"""

    sdk = nps_sdk.Nps()

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_PosDateTime': '2017-01-01 12:00:00'
    }
    resp = sdk.create_client_session(params)

    return resp



def run_create_customer():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()
    params = {
            "psp_Version": "2.2",
            "psp_MerchantId": merchant_id,
            "psp_EmailAddress": "jhon.doe@example.com",
            "psp_AlternativeEmailAddress": "jdoe@example.com",
            "psp_AccountID": "jdoe78",
            "psp_AccountCreatedAt": "2010-10-23",
            "psp_PosDateTime": "2008-01-12 13:05:00"
            #"psp_Person": {
                 #    "FirstName": "John",
                 #    "LastName": "Doe",
                #"MiddleName": "Michael",
                #"PhoneNumber1": "+1 011 11111111",
                #"PhoneNumber2": "+1 011 22222222",
                #"DateOfBirth": "1979-01-12",
                #"Gender": "M",
                #"Nationality": "ARG",
                #"IDNumber": "54111111",
                #"IDType": "200"
        #},
                 #   "psp_Address": {
                 # "Street": "Av. Collins",
                #"HouseNumber": "1245",
                #"AdditionalInfo": "2 A",
                #"StateProvince": "Florida",
                #"City": "Miami",
                #"Country": "USA",
                #"ZipCode": "33140"
        #},
            #"psp_PaymentMethod": {
            #    "PaymentMethodToken": run_create_payment_method_token().psp_PaymentMethodToken,
                #"Address": {
                #    "Street": "Av. Collins",
                #    "HouseNumber": "1245",
                #    "AdditionalInfo": "2 A",
                #    "StateProvince": "Florida",
                #    "City": "Miami",
                #    "Country": "USA",
                #    "ZipCode": "33140"
                #},
                #"Person": {
                #    "FirstName": "John",
                #    "LastName": "Doe",
                #    "MiddleName": "Michael",
                #    "PhoneNumber1": "+1 011 11111111",
                #    "PhoneNumber2": "+1 011 22222222",
                #    "DateOfBirth": "1979-01-12",
                #    "Gender": "M",
                #    "Nationality": "ARG",
                #    "IDNumber": "54111111",
                #    "IDType": "200"
                #}


    #},

}

    resp = sdk.create_customer(params)

    return resp


def run_create_payment_method():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()
    """params = {
            'psp_MerchantId': merchant_id,
            #'psp_CustomerId': 'm3lzaT955LyaT9bKk6vkXZBfwsmxtRIe',
            'psp_PaymentMethod': {
                'PaymentMethodToken': 'uZW5fs68Ql1IWllxyk0gWBLh4ACfhcIh'
                #'Product': '14'
            },
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_SetAsCustomerDefault': '1',
            'psp_Version': '2.2'
        }"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        #psp_CustomerId': 'm3lzaT955LyaT9bKk6vkXZBfwsmxtRIe',
        'psp_PaymentMethod': {
            #'PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken,
            'CardInputDetails': {
                    'ExpirationDate': '1909',
                   'HolderName': 'VISA',
                    'Number': '4242424242424242',
                    'SecurityCode': '9822'
                 },
            'Person': {
                'FirstName': 'John',
                'LastName': 'Doe',
                'MiddleName': 'Michael',
                'PhoneNumber1': '+1 011 11111111',
                'PhoneNumber2': '+1 011 22222222',
                'DateOfBirth': '1979-01-12',
                'Gender': 'M',
                'Nationality': 'ARG',
                'IDNumber': '54111111',
                'IDType': '200'
            },
            'Address': {
                'Street': 'Av. Collins',
                'HouseNumber': '4702',
                'AdditionalInfo': '2 A',
                'City': 'Buenos Aires',
                'StateProvince': 'CABA',
                'Country': 'ARG',
                'ZipCode': '1425'
            }
        },
        #'psp_SetAsCustomerDefault': '1',
        'psp_PosDateTime': '2008-01-12 13:05:00'
    }

    resp = sdk.create_payment_method(params)

    return resp



def run_retrieve_payment_method():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_MerchantId': merchant_id,
            'psp_PaymentMethodId': 'btxMxGIvv487gQvpVuZ6XiGSnPoXPZbo',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.retrieve_payment_method(params)

    return resp


def run_update_payment_method():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_Address': {
                'AdditionalInfo': '2 A',
                'City': 'Miami',
                'Country': 'USA',
                'HouseNumber': '1245',
                'StateProvince': 'Florida',
                'Street': 'Av. Collins',
                'ZipCode': '33140'
            },
            'psp_CardInputDetails': {
                'ExpirationDate': '1909',
                'HolderName': 'JOHN DOE'
            },
            'psp_MerchantId': 'psp_test',
            'psp_PaymentMethodId': 'L4eabajAGaEL1Lgg6DW5Mn2dlRVsSjWX',
            'psp_Person': {
                'DateOfBirth': '1979-01-12',
                'FirstName': 'John',
                'Gender': 'M',
                'IDNumber': '54111111',
                'IDType': '200',
                'LastName': 'Doe',
                'MiddleName': 'Michael',
                'Nationality': 'ARG',
                'PhoneNumber1': '+1 011 11111111',
                'PhoneNumber2': '+1 011 22222222'
            },
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.update_payment_method(params)

    return resp

def run_update_customer():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_AccountCreatedAt': '2010-10-23',
            #'psp_AccountID': 'jdoe78',
            #'psp_Address': {
                 #     'AdditionalInfo': '2 A',
                #'City': 'Miami',
                #'Country': 'USA',
                #'HouseNumber': '1245',
                #'StateProvince': 'Florida',
                #'Street': 'Av. Collins',
                #'ZipCode': '33140'
        #},
            'psp_AlternativeEmailAddress': 'jdoe@example.com',
            'psp_CustomerId': 'QOlx2FDBVcvaznghdIA6vAWIBuI5gswD',
            #'psp_DefaultPaymentMethodId': 'jGW24iDaoMBzfKHViL18TmHo9sHBgW4J',
            'psp_EmailAddress': 'jhon.doe@example.com',
            'psp_MerchantId': merchant_id,
            'psp_PaymentMethod': {
                'PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken,
                #'CardInputDetails': {
                #    'ExpirationDate': '1909',
                #   'HolderName': 'VISA',
                #    'Number': '4242424242424242',
                #    'SecurityCode': '9822'
                #},
                #'Person': {
                #   'DateOfBirth': '1979-01-12',
                #   'FirstName': 'John',
                #   'Gender': 'M',
                #   'IDNumber': '54111111',
                #   'IDType': '200',
                #   'LastName': 'Doe',
                #   'MiddleName': 'Michael',
                #   'Nationality': 'ARG',
                #   'PhoneNumber1': '+1 011 11111111',
                #   'PhoneNumber2': '+1 011 22222222'
                #},
                #'Product': '14'
            },
            #'psp_Person': {
                 #    'DateOfBirth': '1979-01-12',
                #'FirstName': 'John',
                #'Gender': 'M',
                #'IDNumber': '54111111',
                #'IDType': '200',
                #'LastName': 'Doe',
                #'MiddleName': 'Michael',
                #'Nationality': 'ARG',
                #'PhoneNumber1': '+1 011 11111111',
                #'PhoneNumber2': '+1 011 22222222'
        #},
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.update_customer(params)

    return resp


def run_retrieve_customer():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_CustomerId': 'QOlx2FDBVcvaznghdIA6vAWIBuI5gswD',
            'psp_MerchantId': merchant_id,
            'psp_PosDateTime': '2017-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.retrieve_customer(params)

    return resp


def run_delete_payment_method():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
        'psp_MerchantId': merchant_id,
        'psp_PaymentMethodId': 'oHmPvBJuKGb31Jf1QI27GZVRDSwfx4Lo',
        'psp_PosDateTime': '2008-01-12 13:05:00',
        'psp_Version': '2.2'
    }

    resp = sdk.delete_payment_method(params)

    return resp

def run_delete_customer():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params =  {
            'psp_CustomerId': 'btxMxGIvv487gQvpVuZ6XiGSnPoXPZbo',
            'psp_MerchantId': merchant_id,
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.delete_customer(params)

    return resp

def run_create_payment_method_from_payment():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_MerchantId': 'psp_test',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_TransactionId': run_payOnline_2p().psp_TransactionId,
            'psp_Version': '2.2'
        }

    resp = sdk.create_payment_method_from_payment(params)

    return resp



def run_customer():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {
            'psp_CustomerId': 'LABwv1EENe60wpvJVxSmvur5AwK40Upg',
            'psp_MerchantId': 'psp_test',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    resp = sdk.delete_customer(params)

    return resp



def run_create_payment_method_token():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params = {'psp_Address': {'AdditionalInfo': '2 A',
                                   'City': 'Miami',
                                   'Country': 'USA',
                                   'HouseNumber': '1245',
                                   'StateProvince': 'Florida',
                                   'Street': 'Av. Collins',
                                   'ZipCode': '33140'},
                   'psp_CardInputDetails': {'ExpirationDate': '1909',
                                            'HolderName': 'sol',
                                            'Number': '4051885600446623',
                                            #'Number': '4242885600446623',
                                            'SecurityCode': '123'},
                   'psp_ClientSession': run_create_client_session().psp_ClientSession,
                   #'psp_ClientSession': run_create_client_session().psp_Client_,
                   'psp_MerchantId': merchant_id,
                   'psp_Person': {
                       # 'DateOfBirth': '1979-01-12',
                                  'FirstName': 'John'
                                  # 'Gender': 'M',
                                  # 'IDNumber': '54111111',
                                  # 'IDType': '200',
                                  # 'LastName': 'Doe',
                                  # 'MiddleName': 'Michael',
                                  # 'Nationality': 'ARG',
                                  # 'PhoneNumber1': '+1 011 11111111',
                                  # 'PhoneNumber2': '+1 011 22222222'
                                  },
                   'psp_Version': '2.2'}

    resp = sdk.create_payment_method_token(params)

    return resp


def run_retrieve_payment_method_token():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()
    respccs = run_create_client_session()

    params = {'psp_ClientSession': respccs.psp_ClientSession,
               'psp_MerchantId': merchant_id,
               'psp_PaymentMethodToken': 'xxxx',
              # 'psp_PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken,
               'psp_Version': '2.2'}

    resp = sdk.retrieve_payment_method_token(params)

    return resp

#resp = run_create_client_session()

def run_recache_payment_method_token():
    """CreatePaymentMethod"""

    sdk = nps_sdk.Nps()

    params =  {'psp_Address': {'AdditionalInfo': '2 A',
                                   'City': 'Miami',
                                   'Country': 'USA',
                                   'HouseNumber': '1245',
                                   'StateProvince': 'Florida',
                                   'Street': 'Av. Collins',
                                   'ZipCode': '33140'},
                   'psp_CardSecurityCode': '123',
                   'psp_ClientSession': 'ib8P79uYxUlPZ90NmIgKkbwTZFHZZfeD9pioSSkAiPGv2ivMyD01aW9Eh37jq0Tz',
                   'psp_MerchantId': merchant_id,
                   'psp_PaymentMethodId': 'BrMcwXgYtHEfgbHsuYF8WJUceD0s0nMc',
                   'psp_Person': {'DateOfBirth': '1979-01-12',
                                  'FirstName': 'John',
                                  'Gender': 'M',
                                  'IDNumber': '54111111',
                                  'IDType': '200',
                                  'LastName': 'Doe',
                                  'MiddleName': 'Michael',
                                  'Nationality': 'ARG',
                                  'PhoneNumber1': '+1 011 11111111',
                                  'PhoneNumber2': '+1 011 22222222'},
                   'psp_Version': '2.2'}

    resp = sdk.recache_payment_method_token(params)

    return resp


def run_query_card_details():
    sdk = nps_sdk.Nps()

    params = {
                 'psp_Version': '2.2',
                 'psp_MerchantId': 'psp_test',
                 'psp_QueryCriteria': 'T',
                 'psp_QueryCriteriaId': '100409',
                 'psp_PosDateTime': '2016-12-01 12:00:00'
             }
    try:
        resp = sdk.query_card_details(params)
    except ApiException as e:
        print e.msg# Code to handle error
        pass
    return resp


def run_Refund_Payu():
    resp = run_payOnline_2p()
    """Refund"""
    import uuid
    id = uuid.uuid4()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": id,
        "psp_TransactionId_Orig": resp.psp_TransactionId,
        "psp_AmountToRefund": 15050,
        "psp_PosDateTime": '2017-04-04 13:35:20'
    }

    resp = sdk.refund(params)
    return resp


def run_get_installmentsOptions():
    import uuid
    id = uuid.uuid4()
    respccs = run_create_client_session()
    resp = run_create_payment_method_token()

    sdk = nps_sdk.Nps()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": merchant_id,
        "psp_Amount": '100',
        "psp_Product": '14',
        "psp_Currency": '152',
        "psp_Country": "CHL",
        "psp_NumPayments": "1",
        "psp_PaymentMethodToken": resp.psp_PaymentMethodToken,
        "psp_ClientSession": respccs.psp_ClientSession,
        "psp_PosDateTime": '2017-04-04 13:35:20'
    }

    resp = sdk.get_installments_options(params)
    return resp

#resp = run_get_installmentsOptions()



#resp = run_query_card_details()

# resp = run_create_client_session()
#resp = run_create_payment_method_token()
#resp = run_create_payment_method()

#resp = run_create_customer()
#resp = run_update_customer()
#resp = run_retrieve_customer()

# resp =run_Authorize_2p()
resp = run_payOnline_2p()
# resp = run_payOnline_2p()
# resp = run_payOnline_2p()
# resp = run_payOnline_2p()
# resp = run_payOnline_2p()
# resp = run_payOnline_2p()

# resp =run_Capture()
# resp =run_Refund(withP2p=True)




# resp =run_PayOnline_3p()

#resp =run_Authorize_3p()
# resp =run_BankPayment_3p()
#resp =run_CashPayment_3p()
#resp =run_FraudScreening()
# resp =run_SplitAuthorize_3p()
# resp =run_SplitPayOnline_3p() #TODO terminar de probar esto.. esta enviando en los campos de respuestas cosas que no debe
#resp =run_QueryTxs()

# resp = run_SplitAuthorize_2p()
#resp = run_SplitPayOnline_2p()


# resp =run_SimpleQuery_Tx()
#resp =run_ChangeSecretKey()
#resp =run_GetIINDetails() #metodo desabilitado para el comercio
#resp =run_QueryCardNumber()
#resp =run_NotifyFraudScreeningReview() # "Error Interno 1014 - Transacción inexistente"
#resp = run_create_client_session()
#resp = run_create_payment_method()
#resp = run_retrieve_payment_method()
# resp = run_retrieve_payment_method_token()
#resp = run_recache_payment_method_token()
#resp = run_update_payment_method()
#resp = run_create_customer()

#resp = run_create_payment_method_from_payment()
#resp = run_delete_customer()
# resp = run_Authorize_2p()
#resp = run_Capture()
#resp = run_Refund_Payu()
#resp = run_delete_payment_method()
# resp = run_query_card_details()


def run_create_example_for_capacitacion():
    pass


def run_payOnline_2p_kafka():
    sdk = nps_sdk.Nps()
    import uuid
    unicid = uuid.uuid4()
    params ={
        'psp_MerchOrderId': unicid,
        'psp_MerchTxRef': unicid,
        'psp_PosDateTime': '2017-03-31 16:14:06',
        'psp_NumPayments': '1',
        'psp_Currency': '032',
        'psp_Country': 'ARG',
        'psp_TxSource': 'WEB',
        'psp_Product': '14',

        "psp_SoftDescriptor": "mariaconchitaÀ",
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_Amount': "1000",
        "psp_PurchaseDescription": "Gusta",
        # Todo lo que tiene taxes esta siendo rechazado con el error CGW000315-Action Not Enabled for Terminal
        'psp_VaultReference': {
                'PaymentMethodId': run_create_payment_method().psp_PaymentMethod.PaymentMethodId
                # 'PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken
        },
        'psp_BillingDetails': {
            'Address': {
                 "Street": "Av. Collins",
                "HouseNumber": "1245",
                "AdditionalInfo": "2 A",
                "StateProvince": "Florida",
                "City": "Miami",
                "Country": "USA",
                "ZipCode": "33140"
            }
        }

    }

    try:
        resp = sdk.pay_online_2p(params)
        return resp
    except ApiException as e:
        print(e.message)#Code to handle error
        pass

# resp = run_payOnline_2p_kafka()

print(resp)