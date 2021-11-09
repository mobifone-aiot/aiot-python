from aiot import Client


def test_aiot_hello():
    client = Client()
    assert client.hello() == "hello world!"
