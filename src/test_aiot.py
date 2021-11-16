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
    assert(profile["email"] == validEmail)


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
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)


def test_list_thing_by_user():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)


def test_delete_thing():
    cleanup()

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
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_thing(token, "demo-1", {"meta-1": "meta-1"})
    lists = client.list_things_by_user(token)
    assert(lists["total"] == 1)
    assert(len(lists["data"]) == 1)
    assert(lists["data"][0]["name"] == "demo-1")


def test_update_thing():
    cleanup()

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


def test_create_channel():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_channel(token, "demo-1", {"meta-1": "meta-1"})
    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)
    assert(channels["data"][0]["name"] == "demo-1")


def test_update_channel():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    client.create_channel(token, "demo-1", {"meta-1": "meta-1"})

    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)
    assert(channels["data"][0]["name"] == "demo-1")

    channel_id = channels["data"][0]["id"]
    client.update_channel(token, channel_id, "demo-2")

    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)
    assert(channels["data"][0]["name"] == "demo-2")


def test_channel_profile():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    client.create_channel(token, "demo-1", {"meta-1": "meta-1"})

    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)

    channel_id = channels["data"][0]["id"]
    profile = client.channel_profile(token, channel_id)
    assert(profile["name"] == "demo-1")


def test_delete_channel():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    client.create_channel(token, "demo-1", {"meta-1": "meta-1"})

    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)

    channel_id = channels["data"][0]["id"]
    client.delete_channel(token, channel_id)

    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 0)
    assert(len(channels["data"]) == 0)


def test_list_channels_user():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)
    client.create_channel(token, "demo-1", {"meta-1": "meta-1"})
    channels = client.list_channels_by_user(token)
    assert(channels["total"] == 1)
    assert(len(channels["data"]) == 1)
    assert(channels["data"][0]["name"] == "demo-1")


def test_connect():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    things = create_things(token, 3)
    channels = create_channels(token, 3)

    response = client.list_channels_by_thing(token, things[0]["id"])
    assert(response["total"] == 0)
    assert(len(response["data"]) == 0)

    for channel in channels:
        thing_id = things[0]["id"]
        channel_id = channel["id"]
        client.connect(token, [channel_id], [thing_id])

    response = client.list_channels_by_thing(token, things[0]["id"])
    assert(response["total"] == 3)
    assert(len(response["data"]) == 3)


def test_disconnect():
    cleanup()

    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    things = create_things(token, 3)
    channels = create_channels(token, 3)

    response = client.list_channels_by_thing(token, things[0]["id"])
    assert(response["total"] == 0)
    assert(len(response["data"]) == 0)

    for channel in channels:
        thing_id = things[0]["id"]
        channel_id = channel["id"]
        client.connect(token, [channel_id], [thing_id])

    response = client.list_channels_by_thing(token, things[0]["id"])
    assert(response["total"] == 3)
    assert(len(response["data"]) == 3)

    for channel in channels:
        thing_id = things[0]["id"]
        channel_id = channel["id"]
        client.disconnect(token, channel_id, thing_id)

    response = client.list_channels_by_thing(token, things[0]["id"])
    assert(response["total"] == 0)
    assert(len(response["data"]) == 0)


def cleanup():
    client = Client(gatewayAddr)
    token = client.token(validEmail, validPassword)

    channels = client.list_channels_by_user(token)
    for channel in channels["data"]:
        client.delete_channel(token, channel["id"])

    things = client.list_things_by_user(token)
    for thing in things["data"]:
        client.delete_thing(token, thing["id"])


def create_things(token, count):
    client = Client(gatewayAddr)

    for i in range(count):
        name = "demo-%s" % i
        metadata = {"meta-%s" % i: "meta-%s % i"}
        client.create_thing(token, name, metadata)

    response = client.list_things_by_user(token)

    return response["data"]


def create_channels(token, count):
    client = Client(gatewayAddr)

    for i in range(count):
        name = "demo-%s" % i
        metadata = {"meta-%s" % i: "meta-%s % i"}
        client.create_channel(token, name, metadata)

    response = client.list_channels_by_user(token)

    return response["data"]
