from aiot import Client
import json

gatewayAddr = "http://10.16.150.132"
validEmail = "testsdk@mobifone.vn"
validPassword = "12345678"
invalidPassword = "sda21j3h123"


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
