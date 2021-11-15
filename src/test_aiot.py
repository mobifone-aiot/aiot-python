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


def test_reset_password():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    ok = client.token_verify(token)
    assert(ok)
    client.reset_password(token, invalidPassword, validPassword)
    token = client.token(validEmail, invalidPassword)
    ok = client.token_verify(token)
    assert(ok)
    client.reset_password(token, validPassword, invalidPassword)


def test_create_thing():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)

    for thing in lists["data"]:
        client.delete_thing(token, thing["id"])


def test_list_thing_by_user():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)

    for thing in lists["data"]:
        client.delete_thing(token, thing["id"])


def test_delete_thing():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)

    for thing in lists["data"]:
        client.delete_thing(token, thing["id"])

    lists = client.list_things_by_user(token)
    assert(lists["total"] == 0)
    assert(len(lists["data"]) == 0)


def test_thing_profile():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)
    assert(lists["data"][0]["name"] == "demo-1")

    for thing in lists["data"]:
        client.delete_thing(token, thing["id"])


def test_update_thing():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})

    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)
    assert(lists["data"][0]["name"] == "demo-1")

    thing_id = lists["data"][0]["id"]
    client.update_thing(token, thing_id, "demo-2")

    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)
    assert(lists["data"][0]["name"] == "demo-2")

    for thing in lists["data"]:
        client.delete_thing(token, thing["id"])
