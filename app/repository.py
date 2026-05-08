import os
from typing import Optional

from json_lib import JsonParser, JsonWriter
from json_lib.exceptions import JsonParseError, JsonWriteError
from .model import User

_DEFAULT_PATH = os.path.join("data", "users.json")


class UserRepository:
    """
    JSON 파일 기반 User CRUD 저장소.
    PoC 의 JsonParser / JsonWriter 를 그대로 사용한다.
    """

    def __init__(self, path: str = _DEFAULT_PATH):
        self._path = path
        self._parser = JsonParser()
        self._writer = JsonWriter()

    # ── 내부 헬퍼 ─────────────────────────────────────────

    def _load(self) -> list[dict]:
        """파일에서 레코드 목록을 불러온다. 파일이 없으면 빈 리스트 반환."""
        if not os.path.isfile(self._path):
            return []
        try:
            data = self._parser.parse_file(self._path)
            return data if isinstance(data, list) else []
        except JsonParseError:
            return []

    def _save(self, records: list[dict]) -> None:
        """레코드 목록을 JSON 파일에 저장한다."""
        self._writer.save(records, self._path)

    def _next_id(self, records: list[dict]) -> int:
        return max((r["id"] for r in records), default=0) + 1

    # ── Create ────────────────────────────────────────────

    def create(self, user: User) -> User:
        """새 사용자를 JSON 파일에 추가한다."""
        records = self._load()
        user.id = self._next_id(records)
        records.append(user.to_dict())
        self._save(records)
        return user

    # ── Read ──────────────────────────────────────────────

    def read_all(self) -> list[User]:
        """전체 사용자 목록을 반환한다."""
        return [User.from_dict(r) for r in self._load()]

    def read_by_id(self, user_id: int) -> Optional[User]:
        """ID 로 사용자를 조회한다."""
        for r in self._load():
            if r["id"] == user_id:
                return User.from_dict(r)
        return None

    def search(self, keyword: str) -> list[User]:
        """이름 또는 이메일에 키워드가 포함된 사용자를 반환한다."""
        kw = keyword.lower()
        return [
            User.from_dict(r)
            for r in self._load()
            if kw in r["name"].lower() or kw in r["email"].lower()
        ]

    # ── Update ────────────────────────────────────────────

    def update(self, user_id: int, fields: dict) -> Optional[User]:
        """
        특정 사용자의 필드를 수정한다.
        id 는 수정 불가. 존재하지 않는 ID 면 None 반환.
        """
        records = self._load()
        for record in records:
            if record["id"] == user_id:
                fields.pop("id", None)
                record.update(fields)
                self._save(records)
                return User.from_dict(record)
        return None

    # ── Delete ────────────────────────────────────────────

    def delete(self, user_id: int) -> bool:
        """
        ID 에 해당하는 사용자를 안전하게 삭제한다.
        삭제 성공 시 True, 존재하지 않으면 False 반환.
        """
        records = self._load()
        new_records = [r for r in records if r["id"] != user_id]
        if len(new_records) == len(records):
            return False
        self._save(new_records)
        return True
