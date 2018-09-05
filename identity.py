import requests

IDENTITY_API_URL = 'https://api.identity.plus/v1'
IDENTITY_REDIRECT_URL = 'https://get.identity.plus/'
IDENTITY_API_CLIENT_KEY = '/path/to/key/api.key'
IDENTITY_API_CLIENT_CERT = '/path/to/cert/api.pem'
ERROR_PAGE = 'https://<error_page>'
CURRENT_URL = 'https://<current_url>'


def verify_cn_status(client_id, current_url):
    json = {
        "Identity-Inquiry": {
            "anonymous-id": client_id
        }
    }

    cert = (IDENTITY_API_CLIENT_CERT, IDENTITY_API_CLIENT_KEY)
    res = requests.get(IDENTITY_API_URL, json=json, cert=cert, verify=False)

    return request_status(res.json(), current_url)


def associate_account(client_id, local_user, local_user_age, tokens_of_trust):
    json = {
        "Local-User-Information":{
            "anonymous-id": client_id,
            "local-user-name": local_user,
            "local-user-age": local_user_age,
            "tokens-of-trust": tokens_of_trust
        }
    }

    cert = (IDENTITY_API_CLIENT_CERT, IDENTITY_API_CLIENT_KEY)
    res = requests.put(IDENTITY_API_URL, json=json, cert=cert, verify=False)

    return request_status(res.json(), '')


def validate_idle_certificate(return_url):
    json = {
        'Intent': {
            'return-url': return_url
        }
    }

    cert = (IDENTITY_API_CLIENT_CERT, IDENTITY_API_CLIENT_KEY)
    res = requests.put(IDENTITY_API_URL, json=json, cert=cert, verify=False)
    status = request_status(res.json(), '')

    if status['action'] == 'error':
        return ERROR_PAGE

    if status['action'] == 'success':
        intent_value = status['value']
        redirect_url = IDENTITY_REDIRECT_URL + '?intent={0}'.format(intent_value)
        return redirect_url


def request_status(response, current_url):
    if 'Identity-Profile' in response:
        result = response['Identity-Profile']

        if result['outcome'] == 'OK 0000 Acknowledged':
            result['action'] = 'success'
            return result
        elif result['outcome'] == 'OK 0001 Subject anonymous certificate valid':
            result['action'] = 'register'
            return result
        elif result['outcome'] == 'OK 0002 Subject anonymous certificate valid and user uid associated':
            result['action'] = 'login'
            return result

    elif 'Simple-Response' in response:
        result = response['Simple-Response']

        if result['outcome'] == 'PB 0003 Identity Plus anonymous certificate needs validation':
            result['action'] = 'redirect'
            result['url'] = validate_idle_certificate(current_url)
            return result

        result['action'] = 'error'
        return result

    elif 'Intent-Reference' in response:
        result = response['Intent-Reference']

        if result['outcome'] == 'OK 0000 Acknowledged':
            result['action'] = 'success'
            return result
