from aiot import Client
import json


def test_token():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    ok = client.token_verify(token)
    assert(ok)


def test_user_profile():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    profile = client.user_profile(token)
    print(profile)
