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


class Pedido(object):
    id = 0
    total = 0
    installments = 0
    reference = ''


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

    pedido = Pedido()
    pedido.id = 1
    # parcelas
    pedido.installments = 3
    pedido.reference = 'order-{}'.format(pedido.id)

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
                             subtype='CREDIT')

    bandeira = 'VISA'
    holder = 'Nome no cartao'
    number = '1234567890'
    expdate = '2020-01'
    cvv = '123'

    # Fazer uma compra passando o cartao de credito:
    order.set_credit_card(brand=bandeira, cvv=cvv, expdate=expdate, holder=holder, number=number,
                          installments=pedido.installments)

    # Fazer uma compra passando um token de cartão de credito:
    order.set_credit_card(token='ID-DO-TOKEN', cvv=123)

    return order.create_order(pedido.id, pedido.reference)


# Fazer assinatura de um plano
def cycle_order(request, response):
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
                             subtype='CREDIT')

    bandeira = 'VISA'
    holder = 'Nome no cartao'
    number = '1234567890'
    expdate = '2020-01'
    cvv = '123'

    pedido = Pedido()
    pedido.id = 1
    # parcelas
    pedido.installments = 3
    pedido.reference = 'order-{}'.format(pedido.id)

    # Define o pagamento como recorrente
    order.set_subscription(cycles=pedido.installments, start_date=datetime.now().strftime('%Y-%m-%d'))
    # Fazer uma compra passando o cartao de credito:
    order.set_credit_card(brand=bandeira, cvv=cvv, expdate=expdate, holder=holder, number=number)
    # Fazer uma compra passando um token de cartão de credito:
    order.set_credit_card(token='ID-DO-TOKEN', cvv=123)

    return order.create_order(pedido.id, pedido.reference)

