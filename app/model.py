from dataclasses import dataclass, asdict


@dataclass
class User:
    name: str
    age: int
    email: str
    id: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(
            id=data["id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
        )


# dataclass 필드가 아닌 클래스 변수로 선언 — asdict() 직렬화에서 제외됨
User.SCHEMA = {"id": int, "name": str, "age": int, "email": str}
