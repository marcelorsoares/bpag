import base64, hmac, json, requests
from hashlib import sha1, md5
from datetime import datetime
from .config import Configs


class BPag(object):

    def __init__(self,
                 merchant='',
                 account='',
                 access_id='',
                 secret_key='',
                 debug=False,
                 currency='BRL',
                 date_header=datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
                 date_iso_8601=datetime.now().isoformat(),
                 notification_url='',
                 verbose=False,
                 datetime_now='',
                 custom_total=False
                 ):

        if datetime_now != '':
            try:
                self.date_header = datetime_now.strftime('%a, %d %b %Y %H:%M:%S %z')
                self.date_iso_8601 = datetime_now.isoformat()
            except Exception as e:
                print('Erro datetime:', e)
                self.date_header = date_header
                self.date_iso_8601 = date_iso_8601

        if debug:
            self.debug = debug
        else:
            self.debug = Configs['DEBUG']

        if verbose:
            self.verbose = verbose
        else:
            self.verbose = Configs['VERBOSE']

        self.products = ()
        self.amount = 0
        self.products = []
        self.customers = []
        self.redirect_url = None
        self.notification_url = None
        self.custom_total = custom_total

        if merchant:
            self.merchant = merchant
        else:
            self.merchant = Configs['MERCHANT']

        if account:
            self.account = account
        else:
            self.account = Configs['ACCOUNT']

        if access_id:
            self.access_id = access_id
        else:
            self.access_id = Configs['ACCESS_ID']

        if secret_key:
            self.secret_key = secret_key
        else:
            self.secret_key = Configs['SECRET_KEY']

        if notification_url:
            self.notification_url = notification_url
        else:
            self.notification_url = Configs['NOTIFICATION_URL']

        self.protocol_version = Configs['PROTOCOL_VERSION']
        self.api_root = Configs['API_ROOT']
        self.signature = ''
        self.string_to_sign = ''
        self.authorization = ''
        self.hmac_algorithm = Configs['HMAC_ALGORITHM']
        self.city = ''
        self.content = {}
        self.content_type = Configs['CONTENT_TYPE']
        self.currency = currency
        self.financial_institution = Configs['FINANCIAL_INSTITUTION']
        self.technology = Configs['TECHNOLOGY']
        self.processor = Configs['PROCESSOR']
        self.credit_card = {}
        self.paymentMethod = {}
        self.content_md5 = ''
        self.reference = ''
        self.payment_subtype = 'CREDIT'
        self.payment_type = 'CARD'
        self.http_path_infos = {'purchase': '/upbc-service-fe/v1/order/purchase',
                                'consult': '/upbc-service-fe/v1/order/',
                                'create_token': '/upbc-service-fe/v1/token/',
                                'get_token': '/upbc-service-fe/v1/token/',
                                'cancel': '/upbc-service-fe/v1/order/',
                                'get_order': '/upbc-service-fe/v1/order/',
                                'get_client_list_token': '/upbc-service-fe/v1/token/customer-id/'}
        self.http_path_info = self.http_path_infos['purchase']
        self.request_method = ''
        self.content_md5 = ''
        self.response = ''
        self.content_response = {}
        self.reference_word = Configs['REFERENCE_WORD']

    def set_credit_card(self, brand=None, cvv=None, expdate=None, holder=None, installments=0, number=None, token=False):

        self.credit_card = {}

        if brand:
            self.credit_card['brand'] = brand

        if cvv:
            self.credit_card['cvv'] = cvv

        if number:
            self.credit_card['number'] = number

        if expdate:
            self.credit_card['expDate'] = expdate

        if installments:
            self.credit_card['installments'] = installments

        if holder:
            self.credit_card['holder'] = holder

        if token:
            self.credit_card['id'] = token

        return self.credit_card

    def add_product(self, amount, description, id, quantity, taxes):
        return self.products.append({'amount': amount,
                                     'quantity': quantity,
                                     'description': description,
                                     'taxes': taxes,
                                     'id': id})

    def add_customer(self, id, first_name, last_name, email, document, city, state, cep, district):
        return self.customers.append({'firstName': first_name,
                                      'addresses': [{'city': city, 'state': state, 'cep': cep, 'district': district}],
                                      'email': email,
                                      'id': id,
                                      'lastName': last_name,
                                      'type': 'CUSTOMER',
                                      'document': document,
                                      'documentType': 'CPF'
                                      })

    def set_payment_method(self, type=None, subtype=None, processor=None, technology=None, financial_institution=None,
                           installments=1, start_date=datetime.now(), cycles=False):
        payment = {}
        if type is not None:
            payment['paymentType'] = type
        else:
            payment['paymentType'] = self.payment_type

        if subtype is not None:
            payment['paymentSubtype'] = subtype
        else:
            payment['paymentSubtype'] = self.payment_subtype

        if technology is not None:
            payment['technology'] = technology
        else:
            payment['technology'] = self.technology

        if processor is not None:
            payment['processor'] = processor
        else:
            payment['processor'] = self.processor

        if financial_institution is not None:
            payment['financialInstitution'] = financial_institution
        else:
            payment['financialInstitution'] = self.financial_institution

        if installments > 1 and cycles:
            payment['subscription'] = {'cycleType': cycles,
                                       'cycles': installments,
                                       'startDate': start_date}

        # payment['reference'] = reference

        self.paymentMethod = payment
        return self.paymentMethod

    def get_signed_string(self, content_md5, http_path_info):
        return (self.request_method + "\n" + content_md5 + "\n" + self.content_type + "\n" + self.date_header + "\n" +
                http_path_info)

    def get_content_md5(self):
        self.content_md5 = md5(str(json.dumps(self.content, sort_keys=True)).encode('UTF-8')).hexdigest()
        return self.content_md5

    def get_signature(self, string_to_sign):
        self.signature = base64.b64encode(bytes(hmac.new(bytes(self.secret_key, 'UTF-8'),
                                                    bytes(string_to_sign, 'UTF-8'), sha1).digest()))
        return self.signature

    def get_authorization(self):
        self.authorization = ('UOLWS ' + self.access_id + ':' + self.signature.decode() + ':' +
                              self.hmac_algorithm + ':' + self.protocol_version).replace('\n', '')
        return self.authorization

    def get_headers(self):
        return {'Authorization': self.get_authorization().replace('\n', ''), 'Account': self.account,
                'Merchant': self.merchant, 'Date': self.date_header, 'Content-MD5': self.content_md5,
                'Content-Type': self.content_type}

    def verbose_mode(self):
        print('Secret Key: ', self.secret_key)
        print('-')
        print('Date Header: ', self.date_header)
        print('----')
        print('Access ID: ', self.access_id)
        print('-')
        print('Signature:', self.signature)
        print('-')
        print('HMAC-algoritmh: ', self.hmac_algorithm)
        print('-')
        print('protocol-version: ', self.protocol_version)
        print('-')
        print('string-to-sign: ', self.string_to_sign)
        print('-')
        print('HTTP Path Info: ', self.http_path_info)
        print('-')
        print('HTTP VERB: ', self.request_method)
        print('-------headers-------')
        print('Authorization', self.get_authorization())
        print('-')
        print('Account: ', self.account)
        print('-')
        print('Merchant: ', self.merchant)
        print('-')
        print('Content-Type: ', self.content_type)
        print('-')
        print('Content-MD5: ', self.content_md5)
        print('---------------BODY-----------')
        print('Content: ', str(json.dumps(self.content)))
        print('-')
        print('Payment Method: ', self.paymentMethod)
        print('-')
        print('Products: ', self.products)
        print('-')
        print('Customers: ', self.customers)

    def create_token_card(self):
        self.http_path_info = self.http_path_infos['create_token']
        self.request_method = 'POST'

        self.content = {
            'alias': '{}-{}-{}{}'.format(self.customers[0]['id'], str(self.credit_card['number'])[:5],
                                          str(self.credit_card['number'])[-4:], self.credit_card['expDate']),
            'brand': self.credit_card['brand'],
            'number': self.credit_card['number'],
            'customerId': self.customers[0]['id'],
            'expDate': self.credit_card['expDate'],
            'holder': self.credit_card['holder'],
            'cvv': self.credit_card['cvv']
        }

        self.get_content_md5()

        string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

        self.signature = self.get_signature(string_to_sign)

        self.authorization = self.get_authorization()

        if self.verbose or self.debug:
            self.verbose_mode()

        if self.debug:
            return True
        else:
            try:
                self.response = requests.post(self.api_root + self.http_path_info,
                                         headers=self.get_headers(),
                                         data=str(json.dumps(self.content)))

                self.content_response = json.loads(self.response.text)
            except requests.exceptions.Timeout:
                print('Timeout')
                return False

        if self.verbose:
            print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

        return self.response

    def get_client_list_token(self, customerId):
        self.http_path_info = '{}{}'.format(self.http_path_infos['get_client_list_token'], customerId)
        self.request_method = 'GET'

        self.content['customerId'] = customerId

        self.get_content_md5()

        string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

        self.signature = self.get_signature(string_to_sign)

        self.authorization = self.get_authorization()

        if self.verbose or self.debug:
            self.verbose_mode()

        if self.debug:
            return True
        else:
            try:
                self.response = requests.get(self.api_root + self.http_path_info,
                                             headers=self.get_headers(),
                                             data=str(json.dumps(self.content)))

                self.content_response = json.loads(self.response.text)
            except requests.exceptions.Timeout:
                print('Timeout')
                return False

        if self.verbose:
            print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

        return self.response

    def get_card_by_token(self, token_id):
        self.http_path_info = '{}{}'.format(self.http_path_infos['get_token'], token_id)
        self.request_method = 'GET'

        self.content = {'token': token_id}

        self.get_content_md5()

        string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

        self.signature = self.get_signature(string_to_sign)

        self.authorization = self.get_authorization()

        if self.verbose or self.debug:
            self.verbose_mode()

        if self.debug:
            return True
        else:
            try:
                self.response = requests.get(self.api_root + self.http_path_info,
                                             headers=self.get_headers(),
                                             data=str(json.dumps(self.content)))

                if self.response.status_code != 204:
                    print('response:', self.response)
                    self.content_response = json.loads(self.response.text)
                else:
                    print('RESPOSTA DO BPAG VEIO EM BRANCO')
                    return False
            except requests.exceptions.Timeout:
                print('Timeout')
                return False

        if self.verbose:
            print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

        return self.response

    def create_order(self, pedido_id, reference, amount=0.0):
        self.http_path_info = self.http_path_infos['purchase']
        self.request_method = 'POST'
        self.reference = reference
        # self.reference = '{}{}'.format(self.reference_word, reference)
        if self.products:
            for product in self.products:
                if self.custom_total:
                    self.amount = amount
                else:
                    self.amount += product['amount']

            self.content['currency'] = self.currency
            self.content['amount'] = self.amount
            self.content['details'] = {'customers': self.customers, 'products': self.products}

            self.content['reference'] = self.reference
            self.content['requestDate'] = self.date_iso_8601
            self.content['account'] = self.account
            self.content['notificationUrl'] = self.notification_url

            if self.paymentMethod:
                self.content['payments'] = [{'amount': self.amount, 'paymentMethod': self.paymentMethod,
                                             'creditCard': self.credit_card}]

            self.get_content_md5()

            string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

            self.signature = self.get_signature(string_to_sign)

            self.authorization = self.get_authorization()

            if self.verbose or self.debug:
                self.verbose_mode()

            if self.debug:
                return True
            else:

                try:
                    self.response = requests.post(self.api_root + self.http_path_info,
                                             headers=self.get_headers(),
                                             data=str(json.dumps(self.content)))

                    self.content_response = json.loads(self.response.text)

                except requests.exceptions.Timeout:
                    print('Timeout')
                    return '{"error": "Timeout"}'
                except requests.exceptions.ConnectionError:
                    print('error conexao Python Requests')
                    return '{"error": "Erro na conexao com o BPAG"}'
                    # return False

            if self.verbose:
                print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

            return self.response
        else:
            print('BPAG: No products')
            return '{"error": "Adicione algum produto"}'

    def cancel(self, order_id):

        if order_id:

            self.content = {'orderId': order_id}

            self.http_path_info = '{}{}/void'.format(self.http_path_infos['cancel'], order_id)
            self.request_method = 'PUT'

            self.get_content_md5()

            string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

            self.signature = self.get_signature(string_to_sign)
            self.authorization = self.get_authorization()

            if self.verbose or self.debug:
                self.verbose_mode()

            if self.debug:
                return True
            else:
                try:
                    self.response = requests.put(self.api_root + self.http_path_info,
                                                 headers=self.get_headers(),
                                                 data=str(json.dumps(self.content)))

                    self.content_response = json.loads(self.response.text)

                except requests.exceptions.Timeout:
                    print('Timeout')
                    return '{"error": "Timeout"}'
                except requests.exceptions.ConnectionError:
                    print('error conexao Python Requests')
                    return '{"error": "Erro na conexao com o BPAG"}'
                    # return False
                except Exception as e:
                    print('erro: ',e)

            if self.verbose:
                print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

            return self.response
        else:
            return '{"error": "order id invalido"}'

    def get_order(self, order_id):

        self.http_path_info = '{}{}'.format(self.http_path_infos['get_order'], order_id)
        self.request_method = 'GET'

        self.get_content_md5()

        string_to_sign = self.get_signed_string(content_md5=self.content_md5, http_path_info=self.http_path_info)

        self.signature = self.get_signature(string_to_sign)

        self.authorization = self.get_authorization()

        if self.verbose or self.debug:
            self.verbose_mode()

        if self.debug:
            return True
        else:
            try:
                self.response = requests.get(self.api_root + self.http_path_info,
                                              headers=self.get_headers(),
                                              data=str(json.dumps(self.content)))

                self.content_response = json.loads(self.response.text)
            except requests.exceptions.Timeout:
                print('Timeout')
                return False

        if self.verbose:
            print('VERBOSE RESPONSE BPAG RESPONSE', self.response.text)

        return self.response

