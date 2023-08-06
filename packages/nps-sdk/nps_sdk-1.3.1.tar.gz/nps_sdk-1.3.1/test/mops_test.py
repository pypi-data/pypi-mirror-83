from nps_sdk.constants import PRODUCTION_ENV, STAGING_ENV, SANDBOX_ENV, DEVELOPMENT_ENV
import nps_sdk
import logging
import uuid

nps_sdk.Configuration.configure(environment=DEVELOPMENT_ENV,
                                secret_key="IeShlZMDk8mp8VA6vy41mLnVggnj1yqHcJyNqIYaRINZnXdiTfhF0Ule9WNAUCR6", #psp_test
                                # secret_key="I7EPfs5muJ88ElsvwGb01yA2ACg2j3yuZzdokTuhQIE6RFdlKuuWTTYoizBK23d3", #denis_test
                                # secret_key="yiaHxEanfYLfcueh4Zz9W3QKnOAfdEG0YBkxUvZniV5Pe1nN3R8fO0EA9f6VbSoo", #denis_test_1
                                # secret_key="Ylur7fUdUXDx0qydsd5HIfNaXrMERSzF7E1pqJulxYatNjkLZMAREe0V3sCS3WML", #nps_1858_test
                                log_level=logging.INFO, debug=True, cert_verify_peer=False, cert=False, timeout=30,
                                cache=True, cache_location='/tmp', cache_ttl=86400, as_obj=True)

sdk = nps_sdk.Nps()
merchant_id = "psp_test"

# PROCESSING METHOD CONSTANTS
TRANSBANK_LOCAL = 26
DATAFAST = 50
VISANET_ECORE3 = 51
BBVA = 53


visanet_params = {
    'psp_Version': '2.2',
    'psp_TxSource': 'WEB',
    'psp_MerchantId': merchant_id,
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),
    'psp_NumPayments': '1',
    'psp_Amount': '1000',

    'psp_Country': 'PER',
    'psp_Currency': '604',
    # 'psp_Currency': '840',

    'psp_Product': '14',
    'psp_CardNumber': '4551478422045511',
    'psp_CardExpDate': '2912',

    # 'psp_CardNumber': '4507990000000010',
    # 'psp_CardExpDate': '1910',

    'psp_CardSecurityCode': '377',

    # 'psp_CustomerAdditionalDetails': {
    #     'EmailAddress': 'PRUEBA@email.com.12345678901234501',
    #     'AlternativeEmailAddress': 'Jdoe79@email.com',
    #     'IPAddress': '192.168.158.190',
    #     'AccountID': 'Jdoe78',
    #     'AccountCreatedAt': '2010-10-23',
    #     'AccountPreviousActivity': '1',
    #     'AccountHasCredentials': '1',
    #     'DeviceType': '1',
    #     'DeviceFingerPrint': 'KJhKHKJgh7777kgh...',
    #     'BrowserLanguage': 'ES',
    #     'HttpUserAgent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0'
    # },

    # 'psp_ShippingDetails': {
    #     'Method': '10',
    #     'PrimaryRecipient': {
    #         'DateOfBirth': '1979-01-12',
    #         'FirstName': 'John',
    #         'Gender': 'M',
    #         'IDNumber': '54111111',
    #         'IDType': '200',
    #         'LastName': 'Doe',
    #         'MiddleName': 'Michael',
    #         'Nationality': 'ARG',
    #         'PhoneNumber1': '+1 011 11111111',
    #         'PhoneNumber2': '+1 011 22222222'
    #     },
    #     'Address': {
    #         'AdditionalInfo': '3 B',
    #         'City': 'Ottawa',
    #         'Country': 'CAN',
    #         'HouseNumber': '6789',
    #         'StateProvince': 'Ontario',
    #         'Street': 'Av. Solis',
    #         'ZipCode': '77890'
    #     }
    # },

    # 'psp_BillingDetails': {
    #     'Person': {
    #         'DateOfBirth': '1979-01-12',
    #         'FirstName': '12345678901234567890123456',
    #         'Gender': 'M',
    #         'IDNumber': '123456789012',
    #         'IDType': '200',
    #         'LastName': '1234567890123456789012345612345678901234567890123456',
    #         'MiddleName': 'Michael',
    #         'Nationality': 'ARG',
    #         'PhoneNumber1': 'àáâãäçèéêë',
    #         },
    #     'Address': {
    #         'AdditionalInfo': '2 A',
    #         'City': 'Miami',
    #         'Country': 'USA',
    #         'HouseNumber': '1245',
    #         'StateProvince': 'Florida',
    #         'Street': 'Av. Collins',
    #         'ZipCode': '33140'
    #     }
    # },

    # 'psp_MerchantAdditionalDetails': {
    #     'Type': "G",
    #     'SellerDetails': {
    #         'ExternalReferenceId': "12345678",
    #         'IDNumber': "30706033471",
    #         'IDType': "200",
    #         'Name': "12345678901234567890123456",
    #         'Invoice': "54877555",
    #         'PurchaseDescription': "Samsung 4K SUHD TV",
    #         # 'EmailAddress': " jdoe@email.com",
    #         'PhoneNumber1': "1234567890",
    #         # 'PhoneNumber2': " +1 011 22222222",
    #         'MCC': "57325",
    #         'Address': {
    #             'Street': " Av. Collins",
    #             'HouseNumber': "1245",
    #             'City': "Miami",
    #             'StateProvince': "Florida1234567890123",
    #             'Country': "USA",
    #         },
    #     }
    # },
    # 'psp_3dSecure_XID': 'MjY0MjAxNjA4MDIyMDU1=',
    # 'psp_3dSecure_CAVV': 'AAABBYZ3N5Qhl3kBU3c3ELGUsMY=',
    # 'psp_3dSecure_ECI': '5',
    'psp_PosDateTime': '2019-12-01 12:00:00',
    # 'psp_Plan': 'CC',
    # 'psp_Recurrent': 1,
    'psp_ForceProcessingMethod': VISANET_ECORE3
}


def capture_transaction(transaction_id, amount):

    params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_TransactionId_Orig': transaction_id,
        'psp_AmountToCapture': amount,
        'psp_PosDateTime': '2019-12-01 12:00:00'
    }

    return sdk.capture(params)

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


#response = sdk.pay_online_2p(visanet_params)
#response = sdk.authorize_2p(visanet_params)
#respuesta = capture_transaction("258934", 950)
#response = refund_transaction("258944", 1000)


transbank_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': merchant_id,
    'psp_TxSource': 'WEB',
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),

    'psp_Amount': '100',
    'psp_NumPayments': '2',

    'psp_Currency': '152',
    'psp_Country': 'CHL',

    'psp_Product': '14',
    "psp_CardHolderName": 'Teste Holder',

    "psp_CardNumber": '4051885600446623',
    "psp_CardExpDate": '2010',
    "psp_CardSecurityCode": '123',

    'psp_PosDateTime': '2019-12-01 12:00:00',
    'psp_ForceProcessingMethod': TRANSBANK_LOCAL
}

def do_get_installments_options():
    client_session_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_PosDateTime': '2019-12-01 12:00:00'
    }
    client_session_response = sdk.create_client_session(client_session_params)

    payment_method_token_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_CardInputDetails': {
            'Number': '4051885600446623',
            'ExpirationDate': '2010',
            'SecurityCode': '123',
            'HolderName': 'Teste Holder'
        },
        'psp_ClientSession': client_session_response['psp_ClientSession']
    }
    payment_method_token_response = sdk.create_payment_method_token(payment_method_token_params)

    installment_options_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': merchant_id,
        'psp_Amount': '100',

        'psp_Product': '14',
        'psp_Currency': '152',
        'psp_Country': 'CHL',

        'psp_NumPayments': '49',
        # 'psp_NumPayments': '13',

        'psp_PaymentMethodToken': payment_method_token_response['psp_PaymentMethodToken'],
        'psp_ClientSession': client_session_response['psp_ClientSession'],
        'psp_PosDateTime': '2017-04-04 13:35:20'
    }
    installment_options_response = sdk.get_installments_options(installment_options_params)
    return installment_options_response

# response = sdk.authorize_2p(transbank_params)
# response = sdk.pay_online_2p(transbank_params)
# response = refund_transaction("222697", "001")

# do_get_installments_options()


credibanco_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': merchant_id,
    'psp_TxSource': 'WEB',
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),

    'psp_Amount': '1000',
    'psp_NumPayments': '1',

    'psp_Currency': '170',
    'psp_Country': 'COL',

    'psp_Product': '14',
    "psp_CardHolderName": 'Teste Holder',

    "psp_CardNumber": '4051885600446623',
    "psp_CardExpDate": '2010',
    "psp_CardSecurityCode": '123',

    'psp_PosDateTime': '2019-12-01 12:00:00',
    'psp_ForceProcessingMethod': 28
}
# response = sdk.pay_online_2p(credibanco_params)




params = {
    'psp_Version': '2.2',
    'psp_MerchantId': 'psp_test',
    'psp_PosDateTime': '2019-12-01 12:00:00'
}
# response = sdk.create_client_session(params)

massterpass_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': 'psp_test',
    'psp_WalletInputDetails': {
        'WalletTypeId': '2',
        'WalletKey': '3e5d469e608d49bf7e3818de232a54aecf799f10',
        'MerchOrderId': '191016150054924c071e18a-fdf6-4973-9e9f-440601c4c049',
    },
    'psp_ClientSession': 'MNjFtkPvEZR5OXW6hrovIU9nGKxLvOHeQTSFhoseJJPlxNJIDTQubpPbwhwVgtgA',
}
# response = sdk.create_payment_method_token(massterpass_params)

rede_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': merchant_id,
    'psp_TxSource': 'WEB',
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),

    'psp_Amount': '1000',
    'psp_NumPayments': '1',

    'psp_Currency': '986',
    'psp_Country': 'BRA',

    'psp_Product': '14',
    "psp_CardHolderName": 'Teste Holder',

    "psp_CardNumber": '4761120000000148',
    "psp_CardExpDate": '3001',
    "psp_CardSecurityCode": '123',

    'psp_PosDateTime': '2019-12-01 12:00:00',
    'psp_ForceProcessingMethod': 32
}
# response = sdk.pay_online_2p(rede_params)

payon_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': merchant_id,
    'psp_TxSource': 'WEB',
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),

    'psp_Amount': '1000',
    'psp_NumPayments': '1',

    # 'psp_Currency': '840',
    'psp_Currency': '986',

    'psp_Country': 'BRA',

    'psp_Product': '14',
    "psp_CardHolderName": 'Teste Holder',

    "psp_CardNumber": '4761120000000148',
    "psp_CardExpDate": '3001',
    "psp_CardSecurityCode": '123',

    'psp_PosDateTime': '2019-12-01 12:00:00',
    'psp_ForceProcessingMethod': 40
}

# response = sdk.pay_online_2p(payon_params)



def BBVA_NPS2421_TEST():
    bbva_authorize_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': "silvina",
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_MerchOrderId': uuid.uuid4(),

        'psp_Amount': '100',
        'psp_NumPayments': '1',

        'psp_Currency': '840',
        'psp_Country': 'MEX',

        'psp_Product': '14',
        "psp_CardHolderName": 'Teste Holder',

        "psp_CardNumber": '4507999999999991',
        "psp_CardExpDate": '3001',
        "psp_CardSecurityCode": '123',

        'psp_PosDateTime': '2019-12-01 12:00:00',
        'psp_ForceProcessingMethod': BBVA
    }
    response = sdk.authorize_2p(bbva_authorize_params)
    authorization_transaction_id = response.psp_TransactionId
    authorization_amount = response.psp_Amount

    capture_bbva_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'silvina',
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_TransactionId_Orig': authorization_transaction_id,
        'psp_AmountToCapture': authorization_amount,
        'psp_PosDateTime': '2019-12-01 12:00:00'
    }
    response = sdk.capture(capture_bbva_params)
    capture_transaction_id = response.psp_TransactionId

    refund_bbva_params = {
        'psp_Version': '2.2',
        'psp_MerchantId': 'silvina',
        'psp_TxSource': 'WEB',
        'psp_MerchTxRef': uuid.uuid4(),
        'psp_TransactionId_Orig': capture_transaction_id,
        'psp_AmountToRefund': int(response.psp_CapturedAmount),
        'psp_PosDateTime': '2019-12-01 12:00:00'
    }
    response = sdk.refund(refund_bbva_params)

# BBVA_NPS2421_TEST()


bbva_payonline_params = {
    'psp_Version': '2.2',
    'psp_MerchantId': "psp_test",
    'psp_TxSource': 'WEB',
    'psp_MerchTxRef': uuid.uuid4(),
    'psp_MerchOrderId': uuid.uuid4(),

    'psp_Amount': '100',
    # 'psp_Amount': '99909099',

    'psp_NumPayments': '1',
    'psp_Currency': '840',
    'psp_Country': 'MEX',

    # 'psp_Recurrent': 1,

    'psp_Product': '5',
    "psp_CardHolderName": 'Teste Holder',

    #"psp_CardNumber": '4507999999999991',
    #"psp_CardExpDate": '3001',
    #"psp_CardSecurityCode": '123',

    "psp_CardNumber": '5413330089020037',
    "psp_CardExpDate": '2512',
    "psp_CardSecurityCode": '123',

    # "psp_Plan": "CA",
    # "psp_Plan": "CC",

    'psp_MerchantAdditionalDetails': {
        'Type': "A",
        'SellerDetails': {
            'ExternalReferenceId': "12345678",
            'IDNumber': "30706033471",
            'IDType': "200",
            'Name': "12345678901234567890123456",
            'Invoice': "54877555",
            'PurchaseDescription': "Samsung 4K SUHD TV",
            # 'EmailAddress': " jdoe@email.com",
            'PhoneNumber1': "1234567890",
            # 'PhoneNumber2': " +1 011 22222222",
            'MCC': "57325",
            'Address': {
                'Street': " Av. Collins",
                'HouseNumber': "1245",
                'City': "Miami",
                'StateProvince': "Florida1234567890123",
                'Country': "MEX",
                'ZipCode': '33140'
            },
        }
    },

    'psp_3dSecure_XID': 'MjY0MjAxNjA4MDIyMDU1=',
    'psp_3dSecure_CAVV': 'AAABBYZ3N5Qhl3kBU3c3ELGUsMY=',
    'psp_3dSecure_ECI': '5',

    'psp_PosDateTime': '2019-12-01 12:00:00',
    'psp_ForceProcessingMethod': BBVA
}

response = sdk.pay_online_2p(bbva_payonline_params)
# response = sdk.authorize_2p(bbva_payonline_params)
# respuesta = capture_transaction("234201", 100)
# response = refund_transaction("234734", 100)



# bbva_payonline_params_1 = {
#     'psp_Version': '2.2',
#     'psp_MerchantId': "psp_test",
#     'psp_TxSource': 'WEB',
#     'psp_MerchTxRef': uuid.uuid4(),
#     'psp_MerchOrderId': uuid.uuid4(),
#
#     'psp_Amount': '9999999999',
#     'psp_NumPayments': '1',
#     'psp_Currency': '484',
#     'psp_Country': 'MEX',
#
#     'psp_Product': '14',
#     "psp_CardHolderName": 'Teste Holder',
#
#     "psp_CardNumber": '4772912170582641',
#     "psp_CardExpDate": '2805',
#     "psp_CardSecurityCode": '375',
#     'psp_PosDateTime': '2019-12-01 12:00:00',
#     'psp_ForceProcessingMethod': BBVA
# }
#
# response = sdk.pay_online_2p(bbva_payonline_params_1)