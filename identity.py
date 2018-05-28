import requests

IDENTITY_API_URL = 'https://api.identity.plus/v1'
IDENTITY_API_CLIENT_KEY = '/path/to/key/api.key'
IDENTITY_API_CLIENT_CERT= '/path/to/cert/api.pem'

def verify_client_status(client_id):
    json = {
        "Identity-Inquiry": {
            "anonymous-id": client_id
        }
    }

    cert = (IDENTITY_API_CLIENT_CERT, IDENTITY_API_CLIENT_KEY)
    res = requests.get(IDENTITY_API_URL, json=json, cert=cert, verify=False)

    return res


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

    return res
