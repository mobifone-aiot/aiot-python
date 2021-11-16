from enum import Enum


class Directions(str, Enum):
    Asc = "asc"
    Desc = "desc"


class ThingOrders(str, Enum):
    Name = "name"
    Key = "key"
    ID = "id"
