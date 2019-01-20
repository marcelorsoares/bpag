from django.conf import settings

Configs = dict(
    API_ROOT='https://psp.uol.com.br',
    FINANCIAL_INSTITUTION='REDECARD',
    TECHNOLOGY='WEBSERVICES',
    PROCESSOR='EREDE',
    HMAC_ALGORITHM='S1',
    PROTOCOL_VERSION='0.2',
    CONTENT_TYPE='application/json',
    MERCHANT=settings.BPAG_SETTINGS['merchant'],
    ACCOUNT=settings.BPAG_SETTINGS['account'],
    ACCESS_ID=settings.BPAG_SETTINGS['access_id'],
    SECRET_KEY=settings.BPAG_SETTINGS['secret_key'],
    NOTIFICATION_URL=settings.BPAG_SETTINGS['notification_url'],
    REFERENCE_WORD=settings.BPAG_SETTINGS['reference_word'],
    USER_APP=settings.BPAG_SETTINGS['user_app'],
    USER_MODEL=settings.BPAG_SETTINGS['user_model'],
    PEDIDO_APP=settings.BPAG_SETTINGS['pedido_app'],
    PEDIDO_MODEL=settings.BPAG_SETTINGS['pedido_model'],
    DEBUG=settings.BPAG_SETTINGS['debug'],
    VERBOSE=settings.BPAG_SETTINGS['verbose']
)
