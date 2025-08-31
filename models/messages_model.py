from dataclasses import dataclass

@dataclass
class Logon:
    username: str
    password: str

@dataclass
class Logout:
    username: str