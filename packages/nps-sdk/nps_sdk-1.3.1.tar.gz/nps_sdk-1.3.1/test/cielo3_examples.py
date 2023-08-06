# -*- coding: utf-8 -*-
# from sqlalchemy.exc import SADeprecationWarning

from nps_sdk.constants import PRODUCTION_ENV, STAGING_ENV, SANDBOX_ENV, DEVELOPMENT_ENV
import nps_sdk
import logging
import uuid

# prod_mer_id = "aeroarg_web"
# merchant_id = "sdk_test"
# merchant_id = "365online"
merchant_id = "psp_test"

CIELO3 = 35


nps_sdk.Configuration.configure(environment=DEVELOPMENT_ENV,
                                # secret_key="zqyHQTpFxTmIVKeFYAgw2RhqyJI6gCVd2SuRvjeqBQ8gimtHuXDwztnvC5ztGVUG", # prod key aeroarg_web
                                # secret_key="swGYxNeehNO8fS1zgwvCICevqjHbXcwPWAvTVZ5CuULZwKWaGPmXbPSP8i1fKv2q", #sdk_test
                                secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6", #psp_test
                                #secret_key="xfMzDG2gDMwYABT3JWUmkH14i3uwXMTW2hI2GIomhxq3FORdhDs9EDSAeqRQJmMt", #365online
                                #secret_key="0NdyJ37jbRqUnw5ATJoDbkq52WYv9BY8YC6qDCZodNIOJLYmcL0D5oG5Kp0R0WZZ",
                                log_level=logging.INFO, debug=True, cert_verify_peer=False, cert=False, timeout=30, cache=True, cache_location='/tmp', cache_ttl=86400, as_obj=True)


sdk = nps_sdk.Nps()



def run_PayOnline_2p():
    """PayOnline_2p"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_NumPayments': '1',
        'psp_Currency': '986',
        'psp_Country': 'BRA',
        'psp_TxSource': 'WEB',

        # "psp_CardNumber": '4000000140100006',
        "psp_CardNumber": '340000001999951',

        "psp_CardHolderName": 'Teste Holder',
        "psp_CardExpDate": '2012',
        "psp_CardSecurityCode": '123',
        # 'psp_Product': 14,
        'psp_Product': 1,

        # "psp_CardNumber": '4976720550100031', #VISADEBITO
        # "psp_CardExpDate": '3510',
        # "psp_CardSecurityCode": '055',
        # 'psp_Product': 55,

        # "psp_CardNumber": '5100000050100021',  #Master
        # "psp_CardExpDate": '3504',
        # "psp_CardSecurityCode": '005',
        # 'psp_Product': 5,

        # "psp_CardNumber": '340000001010031',  #Master
        # "psp_CardExpDate": '3501',
        # "psp_CardSecurityCode": '0001',
        # 'psp_Product': 1,

        # 'psp_Plan': "DEBIT",
        #
        # "psp_Recurrent": 1,

        "psp_SoftDescriptor": "Product sale",
        'psp_Amount': "15700",
        # "psp_PurchaseDescription": "Gusta",
        'psp_PosDateTime': '2017-03-31 16:14:06',

        # "psp_CustomerAdditionalDetails": {
        #   "AccountPreviousActivity": 1
        # },

        # "psp_BillingDetails": {
        #     "Person": {
        #         'FirstName': 'John',
        #         # 'IDType': 302,
        #         # 'IDNumber': "aaaaaaaaaaa"
        #         # 'IDNumber': "àáâãäçèéêëì"
        #     },
        #     # "Address": {
        #     #     "Street": "Fake Address",
        #     #     "HouseNumber": "123",
        #     #     "City": "Rio",
        #     #     "Country": "ARG",
        #     #     "StateProvince": "dF",
        #     #     "AdditionalInfo": "Extra Info"
        #     # }
        # },

        # 'psp_ShippingDetails': {
        #     # 'Method': '10',
        #     # 'PrimaryRecipient': {
        #     #     'DateOfBirth': '1979-01-12',
        #     #     'FirstName': 'John',
        #     #     'Gender': 'M',
        #     #     'IDNumber': '54111111',
        #     #     'IDType': '200',
        #     #     'LastName': 'Doe',
        #     #     'MiddleName': 'Michael',
        #     #     'Nationality': 'ARG',
        #     #     'PhoneNumber1': '+1 011 11111111',
        #     #     'PhoneNumber2': '+1 011 22222222'
        #     # },
        #     # 'Address': {
        #     #     'AdditionalInfo': '2 A',
        #     #     'City': 'Miami',
        #     #     'Country': 'USA',
        #     #     'HouseNumber': '1245',
        #     #     'StateProvince': 'dF',
        #     #     'Street': 'Av. Collins',
        #     #     'ZipCode': '33140'
        #     # }
        # },

        # "psp_AmountAdditionalDetails": {
        #     "Taxes": [
        #         {
        #             "TypeId": 100,
        #             "Amount": 1
        #         },
        #         # {
        #         #     "TypeId": 500,
        #         #     "BaseAmount": 20000
        #         # }
        #     ]
        # },

        # "psp_WalletReference": {
        #     "WalletTypeId": "1",
        #     "WalletIdentificationCode": "101"
        # },


        # 'psp_3dSecure_CAVV': 'AAABBYZ3N5Qhl3kBU3c3ELGUsMY=',
        # 'psp_3dSecure_XID': 'MjY0MjAxNjA4MDIyMDUzMzYyNjU=',
        # 'psp_3dSecure_ECI': '12',

        'psp_ForceProcessingMethod': CIELO3
    }
    return sdk.pay_online_2p(params)

def run_Authorize_2p():
    """Authorize_2p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_NumPayments": '1',
        'psp_Currency': '986',
        "psp_Country": 'BRA',
        'psp_Amount': "15700",

        # "psp_CardNumber": '40120010381666621',
        # "psp_CardExpDate": '1902',
        # "psp_CardSecurityCode": '123',
        # "psp_Product": 14,

        "psp_CardNumber": '340000001010031',
        "psp_CardExpDate": '2107',
        "psp_CardSecurityCode": '0001',
        "psp_Product": 1,

        "psp_Recurrent": 1,
        # "psp_PurchaseDescription": "Force Renova Facil",

        "psp_CardHolderName": "Gustavo Diaz",
        "psp_PosDateTime": '2017-04-04 13:35:20',

        # 'psp_VaultReference': {
        #     'PaymentMethodId': 'UmK1PMJNsd00ppcAXZ6TQlvKExRCJQLX'
        # },

        # "psp_CustomerAdditionalDetails": {
        #   "AccountPreviousActivity": 1
        # },
        # 'psp_Plan': "DEBIT",

        'psp_ForceProcessingMethod': CIELO3

    }

    return sdk.authorize_2p(params)

def run_PayOnline_3p():
    """PayOnLine_3p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        "psp_MerchOrderId": uuid.uuid4(),
        # "psp_ReturnURL": 'https://psp-client.nps.com.ar/simple_query_tx.php',
        "psp_ReturnURL": 'https://10.40.10.35/3pMopCatch.php',
        "psp_FrmLanguage": 'es_AR',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_NumPayments": '1',
        'psp_Currency': '986',
        "psp_Country": 'BRA',

        "psp_Product": '1',     # AMEX
        # "psp_Product": '14',
        # "psp_Product": '55',

        'psp_Amount': '1000',

        # 'psp_Plan': "DEBIT",

        'psp_3dSecureAction': 1,
        # 'psp_3dSecure_CAVV': 'AAABBYZ3N5Qhl3kBU3c3ELGUsMY=',
        # 'psp_3dSecure_XID': 'MjY0MjAxNjA4MDIyMDUzMzYyNjU=',
        # 'psp_3dSecure_ECI': '12',

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.pay_online_3p(params)

def run_Authorize_3p():
    """Authorize_3p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_ReturnURL": 'https://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_NumPayments": '1',
        'psp_Currency': '986',
        "psp_Country": 'BRA',
        "psp_Product": '14',
        'psp_Amount': '1000',

        'psp_Plan': "DEBIT",

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.authorize_3p(params)

def run_SplitPayOnline_3p():
    """SplitPayOnLine_3p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 10000,
                "psp_NumPayments": 1
            },
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 5050,
                "psp_NumPayments": 1
            }
        ],

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_pay_online_3p(params)

def run_SplitAuthorize_3p():
    """SplitAuthorize_3p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_ReturnURL": 'http://localhost/',
        "psp_FrmLanguage": 'es_AR',
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 10000,
                "psp_NumPayments": 1
            },
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 5050,
                "psp_NumPayments": 1
            }
        ],

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_authorize_3p(params)

def run_SplitAuthorize_2p():
    """SplitAuthorize_2p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '40120010381666621',
        "psp_CardExpDate": '2112',
        "psp_CardSecurityCode": '123',
        "psp_CardHolderName": "Gustavo Diaz",
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 10000,
                "psp_NumPayments": 1
                # "psp_CardNumber": '4012001038166662',
                # "psp_CardExpDate": '1906',
                # "psp_CardSecurityCode": '123',
            },
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 5050,
                "psp_NumPayments": 1,
                # "psp_VaultReference":{
                #     "PaymentMethodToken": run_create_payment_method_token().psp_PaymentMethodToken
                # }
                # "psp_CardNumber": '4012001038166662',
                # "psp_CardExpDate": '1906',
                # "psp_CardSecurityCode": '123',
            }
        ],

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_authorize_2p(params)

def run_SplitPayOnline_2p():
    """SplitPayOnline_2p"""

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchOrderId": uuid.uuid4(),
        "psp_Amount": 15050,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '40120010381666621',
        "psp_CardExpDate": '2112',
        "psp_CardSecurityCode": '123',
        "psp_CardHolderName": "Gustavo Diaz",
        'psp_Recurrent': 1,
        # "psp_CardSecurityCode": '123',
        "psp_PosDateTime": '2016-12-01 12:00:00',
        "psp_Transactions": [
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 10000,
                "psp_NumPayments": 1,
                # "psp_CardNumber": '4012001038166662',
                # "psp_CardExpDate": '1906',
                # "psp_CardSecurityCode": '123',
            },
            {
                "psp_MerchantId": merchant_id,
                "psp_MerchTxRef": uuid.uuid4(),
                "psp_Product": 14,
                "psp_Amount": 5050,
                "psp_NumPayments": 1
                # "psp_CardNumber": '4012001038166662',
                # "psp_CardExpDate": '1906',
                # "psp_CardSecurityCode": '123',
            }
        ],

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_pay_online_2p(params)

def run_Capture(transaction_id = None):
    """Capture"""

    if (transaction_id == None):
        auth_resp = run_Authorize_2p()
        transaction_id = auth_resp.psp_TransactionId

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": merchant_id,
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        "psp_TransactionId_Orig": transaction_id,
        "psp_AmountToCapture": 15700,  # CAPTURA TOTAL,
        # "psp_AmountToCapture": auth_resp.psp_Amount, # CAPTURA TOTAL
        # "psp_AmountToCapture": int(int(auth_resp.psp_Amount)/2),  # CAPTURA PARCIAL
        "psp_PosDateTime": '2017-12-01 12:00:00',

        "psp_AmountAdditionalDetails": {
            "Taxes": [
                {
                    "TypeId": 100,
                    "BaseAmount": 20000
                },
                {
                    "TypeId": 500,
                    "BaseAmount": 20000
                }
            ]
        },

        # 'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.capture(params)

def run_Refund(withP2p=False, withA2p=False):
    """Refund"""

    if withP2p:
        req_resp = run_PayOnline_2p()
    else:
        if withA2p:
            req_resp = run_Authorize_2p()
        else:
            req_resp = run_Capture()

    params_1 = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        "psp_AmountToRefund": req_resp.psp_Amount,
        # "psp_AmountToRefund": int(int(req_resp.psp_Amount) - 10),
        # "psp_AmountToRefund": int(int(req_resp.psp_CapturedAmount) - 10),
        "psp_TransactionId_Orig": req_resp.psp_TransactionId,
        "psp_PosDateTime": '2016-12-01 12:00:00',
    }

    params_2 = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        # "psp_AmountToRefund": 7850,
        "psp_AmountToRefund": 11,
        "psp_TransactionId_Orig": req_resp.psp_TransactionId,
        "psp_PosDateTime": '2016-12-01 12:00:00',
    }

    params_3 = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": uuid.uuid4(),
        # "psp_AmountToRefund": 1,
        "psp_AmountToRefund": 10,
        "psp_TransactionId_Orig": req_resp.psp_TransactionId,
        "psp_PosDateTime": '2016-12-01 12:00:00',
    }

    refund_response_1 = sdk.refund(params_1)
    # refund_response_2 = sdk.refund(params_2)
    # refund_response_3 = sdk.refund(params_3)

    # query_result = run_SimpleQuery_Tx(refund_response.psp_TransactionId)

    return refund_response_1

def run_SimpleQuery_Tx(transaction_id = None):
    """SimpleQuery_Tx"""

    criteria_id = None

    if (transaction_id == None):
        criteria_id = run_PayOnline_2p().psp_TransactionId
    else:
        criteria_id = transaction_id


    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_QueryCriteria": 'T',
        "psp_QueryCriteriaId": criteria_id,
        "psp_PosDateTime": '2016-12-01 12:00:00',
    }

    return sdk.simple_query_tx(params)

def run_QueryTxs():
    """QueryTxs"""

    po2p_merch_order_id = run_PayOnline_2p().psp_MerchOrderId

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_QueryCriteria": 'O',
        "psp_QueryCriteriaId": po2p_merch_order_id,
        "psp_PosDateTime": '2016-12-01 12:00:00',

        # 'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.query_txs(params)

def run_FraudScreening():
    """FraudScreening"""

    po2p_merch_order_id = run_PayOnline_2p().psp_MerchOrderId

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": 'ORDER66666-3',
        "psp_MerchOrderId": po2p_merch_order_id,
        "psp_Amount": 15050,
        "psp_NumPayments": 1,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '40120010381666621',
        "psp_CardExpDate": '2112',
        "psp_PosDateTime": '2016-12-01 12:00:00',

        # 'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.fraud_screening(params)

def run_NotifyFraudScreeningReview():
    """NotifyFraudScreeningReview"""

    fraud_screening_params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_TxSource": 'WEB',
        "psp_MerchTxRef": 'ORDER66666-3',
        "psp_MerchOrderId": 'ORDER66666-3',
        "psp_Amount": 15050,
        "psp_NumPayments": 1,
        "psp_Currency": '986',
        "psp_Country": 'BRA',
        "psp_Product": 14,
        "psp_CardNumber": '4000111231110112',
        "psp_CardExpDate": '2112',
        "psp_PosDateTime": '2016-12-01 12:00:00',
    }

    fraud_screening_order_id = sdk.fraud_screening(fraud_screening_params).psp_OrderId

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": 'psp_test',
        "psp_Criteria": 'O',
        "psp_CriteriaId": fraud_screening_order_id,
        "psp_ReviewResult": 'A',
        "psp_PosDateTime": '2016-12-01 12:00:00'
    }

    return sdk.notify_fraud_screening_review(params)



def NPS_1515_PayOnline3p():

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_ReturnURL': "https://localhost/",
        'psp_FrmLanguage': "es_AR",
        'psp_Amount': "15700",
        'psp_NumPayments': '1',
        'psp_Plan': "DEBIT",
        'psp_Currency': '986',
        'psp_Country': 'BRA',
        'psp_Product': 1,
        # "psp_CardNumber": '340000001010031',
        # "psp_CardExpDate": '3701',
        # "psp_CardSecurityCode": '0001',
        "psp_PurchaseDescription": "Cielo3 - Test",
        'psp_ForceProcessingMethod': CIELO3,
        'psp_PosDateTime': '2017-03-31 16:14:06'
    }

    return sdk.pay_online_3p(params)

def NPS_1515_Autorize3p():

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_ReturnURL': "https://www.gmail.com/",
        'psp_FrmLanguage': "es_AR",
        'psp_Amount': "15700",
        'psp_NumPayments': '1',
        # 'psp_Plan': "DEBIT",
        'psp_Currency': '986',
        'psp_Country': 'BRA',
        'psp_Product': 1,
        # "psp_CardNumber": '340000001010031',
        # "psp_CardExpDate": '3701',
        # "psp_CardSecurityCode": '0001',
        "psp_PurchaseDescription": "Cielo3 - Test",
        'psp_ForceProcessingMethod': CIELO3,
        'psp_PosDateTime': '2017-03-31 16:14:06'
    }

    return sdk.authorize_3p(params)

def NPS_1515_SplitPayOnline3p():

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_TxSource': 'WEB',
        # 'psp_MerchTxRef': uuid.uuid4(),
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_ReturnURL': "https://www.google.com/",
        'psp_FrmLanguage': "es_AR",
        'psp_Amount': "20000",
        'psp_Currency': '986',
        'psp_Country': 'BRA',
        'psp_Product': 1,
        # "psp_CardNumber": '340000001010031',
        # "psp_CardExpDate": '3701',
        # "psp_CardSecurityCode": '0001',
        "psp_PurchaseDescription": "Cielo3 - Test",
        'psp_ForceProcessingMethod': CIELO3,
        'psp_PosDateTime': '2017-03-31 16:14:06',
        'psp_Transactions': [
            {
                'psp_MerchantId': merchant_id,
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': "10000",
                'psp_NumPayments': 1,
                'psp_Plan': "DEBIT"
            },
            {
                'psp_MerchantId': merchant_id,
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': "10000",
                'psp_NumPayments': 1,
                'psp_Plan': "DEBIT"
            }
        ]
    }

    return sdk.split_pay_online_3p(params)

def renova_facil_test():
    renova_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_NumPayments': '1',
        'psp_Currency': '986',
        'psp_Country': 'BRA',
        'psp_TxSource': 'WEB',
        "psp_CardNumber": '40120010381666623',
        "psp_CardExpDate": '1712',
        "psp_CardSecurityCode": '123',
        'psp_Product': 14,
        "psp_Recurrent": 1,
        # 'psp_Plan': "DEBIT",
        "psp_SoftDescriptor": "Product sale ",
        'psp_Amount': "10000",
        "psp_PurchaseDescription": "Gusta",
        'psp_PosDateTime': '2017-03-31 16:14:06',

        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.pay_online_2p(renova_params)

def cpmt():
    # cs_params = {
    #     'psp_Version': '2.2',
    #     'psp_MerchantId': 'sdk_test',
    #     'psp_PosDateTime': '2019-12-01 12:00:00'
    # }
    #
    # session = sdk.create_client_session(cs_params)
    #
    # token_params = {
    #     "psp_Version": "2.2",
    #     "psp_MerchantId": "sdk_test",
    #     "psp_CardInputDetails": {
    #         "Number": "4507990000000010",
    #         "ExpirationDate": "2501",
    #         "SecurityCode": "123",
    #         "HolderName": "JOHN DOE"
    #     },
    #     "psp_ClientSession": session.get('psp_ClientSession')
    # }
    #
    # token = sdk.create_payment_method_token(token_params)

    pm_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_PaymentMethod': {
            'CardInputDetails': {
                "Number": '40120010381666621',
                "ExpirationDate": '2112',
                "SecurityCode": '123',
                'HolderName': 'TEST'
            },
            # 'PaymentMethodTag': 'Corporate card',
            # 'Person': {
            #     'FirstName': 'John',
            #     'LastName': 'Doe',
            #     'MiddleName': 'Michael',
            #     'PhoneNumber1': '+1 011 11111111',
            #     'PhoneNumber2': '+1 011 22222222',
            #     'DateOfBirth': '1979-01-12',
            #     'Gender': 'M',
            #     'Nationality': 'ARG',
            #     'IDNumber': '54111111',
            #     'IDType': '200'
            # },
            # 'Address': {
            #     'Street': 'Av. Collins',
            #     'HouseNumber': '4702',
            #     'AdditionalInfo': '2 A',
            #     'City': 'Buenos Aires',
            #     'StateProvince': 'CABA',
            #     'Country': 'ARG',
            #     'ZipCode': '1425'
            # }
        },
        'psp_PosDateTime': '2008-01-12 13:05:00'
    }

    return sdk.create_payment_method(pm_params)



def NPS_1642_SplitPayOnLine_3p():
    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_TxSource': 'WEB',

        "psp_ReturnURL": "https://www.siteMerchantTesting-CIELO3BR.com",
        "psp_FrmLanguage": "es_AR",

        'psp_Amount': '2000',
        'psp_Currency': '986',
        'psp_Country': 'BRA',

        "psp_Product": 1,
        # "psp_CardNumber": '340000001010031',
        # "psp_CardExpDate": '1902',
        # "psp_CardSecurityCode": '0001',

        "psp_Transactions": [
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '1'
            },
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '1'
            }
        ],

        'psp_PosDateTime': '2019-12-01 12:00:00',
        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_pay_online_3p(params)

def NPS_1720_SplitPayOnline3p():
    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_MerchOrderId': uuid.uuid4(),
        'psp_TxSource': 'WEB',

        "psp_ReturnURL": "https://www.siteMerchantTesting-CIELO3BR.com",
        "psp_FrmLanguage": "es_AR",

        'psp_Amount': '5000',
        'psp_Currency': '986',
        'psp_Country': 'BRA',

        'psp_Product': 14,

        # "psp_CardNumber": '4000000140100001',
        # "psp_CardHolderName": 'Teste Holder',
        # "psp_CardExpDate": '1912',
        # "psp_CardSecurityCode": '123',

        "psp_Transactions": [
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '1'
            },
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '2'
            },
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '3'
            },
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '4'
            },
            {
                'psp_MerchTxRef': uuid.uuid4(),
                'psp_Amount': '1000',
                'psp_NumPayments': '5'
            }
        ],

        'psp_PosDateTime': '2019-12-01 12:00:00',
        'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.split_pay_online_3p(params)


def refund_transaction(transaction_id, amount):

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_TransactionId_Orig': transaction_id,
        'psp_AmountToRefund': amount,
        'psp_PosDateTime': '2019-12-01 12:00:00'

    }

    return sdk.refund(params)


# respuesta = cpmt()
# respuesta = renova_facil_test()
# respuesta = NPS_1515_PayOnline3p()
# respuesta = NPS_1515_Autorize3p()
# respuesta = NPS_1515_SplitPayOnline3p()

# respuesta = NPS_1642_SplitPayOnLine_3p()
# respuesta = NPS_1720_SplitPayOnline3p()

respuesta = run_PayOnline_2p()
# respuesta = run_Authorize_2p()

respuesta = run_PayOnline_3p()
# respuesta = run_Authorize_3p()

# respuesta = run_SplitPayOnline_3p()
# respuesta = run_SplitAuthorize_3p()
# respuesta = run_SplitAuthorize_2p()
# respuesta = run_SplitPayOnline_2p()

#refund_transaction('258987', 100)

# respuesta = run_Capture("257742")
#respuesta = run_Refund()
#respuesta = run_Refund(withP2p=True)

# respuesta = run_SimpleQuery_Tx("222026")
# respuesta = run_QueryTxs()

# respuesta = run_CashPayment_3p()
# respuesta = run_BankPayment_3p()
# respuesta = run_FraudScreening()
# respuesta = run_NotifyFraudScreeningReview()
# respuesta = run_QueryCardNumber()                 #TODO Probar metodo
# respuesta = run_GetIINDetails()                   #TODO Probar metodo




def run_get_installmentsOptions():
    """GetInstallmentsOptions"""

    resp_ccs = run_create_client_session()
    resp_cpmt = run_create_payment_method_token()

    params = {
        "psp_Version": '2.2',
        "psp_MerchantId": merchant_id,
        "psp_Amount": '100',
        "psp_Product": '14',
        "psp_Currency": '152',
        "psp_Country": "CHL",
        "psp_NumPayments": "1",
        "psp_PaymentMethodToken": resp_ccs.psp_PaymentMethodToken,
        "psp_ClientSession": resp_cpmt.psp_ClientSession,
        "psp_PosDateTime": '2017-04-04 13:35:20'
    }

    return sdk.get_installments_options(params)

def run_query_card_details():
    """QueryCardDetails"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'psp_test',
        'psp_QueryCriteria': 'T',
        'psp_QueryCriteriaId': '100409',
        'psp_PosDateTime': '2016-12-01 12:00:00'
    }

    return sdk.query_card_details(params)

def run_create_client_session():
    """CreateClientSession"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_PosDateTime': '2017-01-01 12:00:00'
    }

    return sdk.create_client_session(params)

def run_create_customer():
    """CreateCustomer"""

    params = {
        "psp_Version": "2.2",
        "psp_MerchantId": merchant_id,
        "psp_EmailAddress": "jhon.doe@example.com",
        "psp_AlternativeEmailAddress": "jdoe@example.com",
        "psp_AccountID": "jdoe78",
        "psp_AccountCreatedAt": "2010-10-23",
        "psp_PosDateTime": "2008-01-12 13:05:00"
        # "psp_PaymentMethod": {
        #    "PaymentMethodToken": run_create_payment_method_token().psp_PaymentMethodToken,
        # },
    }

    return sdk.create_customer(params)

def run_create_payment_method():
    """CreatePaymentMethod"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        #psp_CustomerId': 'm3lzaT955LyaT9bKk6vkXZBfwsmxtRIe',
        'psp_PaymentMethod': {
            # 'PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken,
            'CardInputDetails': {
                'ExpirationDate': '1909',
                'HolderName': 'VISA',
                'Number': '4242424242424242',
                'SecurityCode': '9822',
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

    return sdk.create_payment_method(params)

def run_retrieve_payment_method():
    """RetrievePaymentMethod"""

    params = {
            'psp_MerchantId': merchant_id,
            'psp_PaymentMethodId': 'btxMxGIvv487gQvpVuZ6XiGSnPoXPZbo',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_Version': '2.2'
        }

    return sdk.retrieve_payment_method(params)

def run_create_payment_method_from_payment():
    """CreatePaymentMethodFromPayment"""

    params = {
            'psp_MerchantId': 'psp_test',
            'psp_PosDateTime': '2008-01-12 13:05:00',
            'psp_TransactionId': run_PayOnline_2p().psp_TransactionId,
            'psp_Version': '2.2'
        }

    return sdk.create_payment_method_from_payment(params)

def run_create_payment_method_token():
    """CreatePaymentMethodToken"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
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
            'HolderName': 'sol',
            'Number': '4051885600446623',
            #'Number': '4242885600446623',
            'SecurityCode': '123'
       },
       'psp_ClientSession': run_create_client_session().psp_ClientSession,
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
        }
    }

    return sdk.create_payment_method_token(params)

def run_retrieve_payment_method_token():
    """RetrievePaymentMethodToken"""

    resp_ccs = run_create_client_session()

    params = {
        'psp_ClientSession': resp_ccs.psp_ClientSession,
        'psp_MerchantId': merchant_id,
        'psp_PaymentMethodToken': 'xxxx',
        # 'psp_PaymentMethodToken': run_create_payment_method_token().psp_PaymentMethodToken,
        'psp_Version': '2.2'}

    return sdk.retrieve_payment_method_token(params)

def run_recache_payment_method_token():
    """RecachePaymentMethodToken"""

    params = {
        'psp_Version': '2.2',
        'psp_Address': {
            'AdditionalInfo': '2 A',
            'City': 'Miami',
            'Country': 'USA',
            'HouseNumber': '1245',
            'StateProvince': 'Florida',
            'Street': 'Av. Collins',
            'ZipCode': '33140'
        },
        'psp_CardSecurityCode': '123',
        'psp_ClientSession': 'ib8P79uYxUlPZ90NmIgKkbwTZFHZZfeD9pioSSkAiPGv2ivMyD01aW9Eh37jq0Tz',
        'psp_MerchantId': merchant_id,
        'psp_PaymentMethodId': 'BrMcwXgYtHEfgbHsuYF8WJUceD0s0nMc',
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
        }
    }

    return sdk.recache_payment_method_token(params)

def run_CashPayment_3p():
    """CashPayment_3p"""

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

    return sdk.cash_payment_3p(params)

def run_BankPayment_3p():
    """BankPayment_3p"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'psp_test',
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
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

    return sdk.bank_payment_3p(params)

def run_QueryCardNumber():
    """QueryCardNumber"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'psp_test',
        'psp_QueryCriteria': 'O',
        'psp_QueryCriteriaId': '100400',
        'psp_PosDateTime': '2017-12-01 12:00:00',

        # 'psp_ForceProcessingMethod': CIELO3
    }

    return sdk.query_card_number(params)

def run_GetIINDetails():
    """GetIINDetails"""

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'psp_test',
        'psp_IIN': '424242',
        'psp_PosDateTime': '2016-12-01 12:00:00'
    }

    return sdk.get_iin_details(params)