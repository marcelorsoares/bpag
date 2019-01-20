from datetime import datetime
from bpag.bpag import BPag


class Profile(object):
    id = 0
    first_name = ''
    last_name = ''
    email = ''
    document = 0
    city = ''
    state = ''
    zip_code = ''
    district = ''


# Metodo para gerar token de cartao de credito
def generate_token_card(request, response):
    payment_token = BPag()

    profile = Profile()
    profile.id = 1
    profile.first_name = 'Name'
    profile.last_name = 'Lastname'
    profile.email = 'email@test.com'
    profile.document = 123456789
    profile.city = 'City'
    profile.state = 'State'
    profile.zip_code = '12345-678'

    payment_token.add_customer(id=profile.id,
                               first_name=profile.first_name,
                               last_name=profile.last_name,
                               email=profile.email,
                               document=profile.document,
                               city=profile.city,
                               state=profile.state,
                               cep=profile.zip_code,
                               district=profile.district)

    bandeira = 'VISA'
    holder = 'Nome no cartao'
    number = '1234567890'
    expdate = '2020-01'
    cvv = '123'

    payment_token.set_credit_card(brand=bandeira, cvv=cvv, expdate=expdate, holder=holder, number=number)

    return payment_token.create_token_card()


def order(request, response):
    order = BPag()

    profile = Profile()
    profile.id = 1
    profile.first_name = 'Name'
    profile.last_name = 'Lastname'
    profile.email = 'email@test.com'
    profile.document = 123456789
    profile.city = 'City'
    profile.state = 'State'
    profile.zip_code = '12345-678'

    order.add_customer(id=profile.id,
                               first_name=profile.first_name,
                               last_name=profile.last_name,
                               email=profile.email,
                               document=profile.document,
                               city=profile.city,
                               state=profile.state,
                               cep=profile.zip_code,
                               district=profile.district)

    order.set_payment_method(type='CARD',
                                     subtype='CREDIT',
                                     installments=1,
                                     start_date=datetime.now().strftime('%Y-%m-%d'))

    bandeira = 'VISA'
    holder = 'Nome no cartao'
    number = '1234567890'
    expdate = '2020-01'
    cvv = '123'

    order.set_credit_card(brand=bandeira, cvv=cvv, expdate=expdate, holder=holder, number=number)

    return order.create_token_card()

