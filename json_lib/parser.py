import json
import os
from typing import Any, Union
from .exceptions import JsonParseError, JsonValidationError


class JsonParser:
    """JSON 문자열 및 파일을 파싱하는 클래스"""

    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    # ── 파싱 ──────────────────────────────────────────────

    def parse_string(self, text: str) -> Any:
        """JSON 문자열을 Python 객체로 변환합니다."""
        if not isinstance(text, str):
            raise JsonParseError(f"문자열이 필요하지만 {type(text).__name__} 가 입력되었습니다.")
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise JsonParseError(f"JSON 파싱 오류: {e}") from e

    def parse_file(self, path: str) -> Any:
        """JSON 파일을 읽어 Python 객체로 변환합니다."""
        if not os.path.isfile(path):
            raise JsonParseError(f"파일을 찾을 수 없습니다: {path}")
        try:
            with open(path, "r", encoding=self.encoding) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise JsonParseError(f"[{path}] JSON 파싱 오류: {e}") from e
        except OSError as e:
            raise JsonParseError(f"[{path}] 파일 읽기 실패: {e}") from e

    def parse_bytes(self, data: bytes) -> Any:
        """바이트 데이터를 JSON으로 파싱합니다."""
        try:
            return json.loads(data.decode(self.encoding))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise JsonParseError(f"바이트 파싱 오류: {e}") from e

    # ── 유효성 검사 ────────────────────────────────────────

    def validate(self, data: Any, schema: dict) -> None:
        """
        간단한 타입 기반 스키마 검증.

        schema 예시:
            {
                "name": str,
                "age":  int,
                "tags": list,
                "meta": dict,        # 중첩 dict 허용
            }
        """
        if not isinstance(data, dict):
            raise JsonValidationError("최상위 데이터가 dict 타입이어야 합니다.")

        errors: list[str] = []
        for key, expected_type in schema.items():
            if key not in data:
                errors.append(f"필수 키 누락: '{key}'")
            elif not isinstance(data[key], expected_type):
                actual = type(data[key]).__name__
                expect = expected_type.__name__
                errors.append(f"'{key}' 타입 오류: 예상={expect}, 실제={actual}")

        if errors:
            raise JsonValidationError("스키마 검증 실패:\n  " + "\n  ".join(errors))

    def parse_file_validated(self, path: str, schema: dict) -> Any:
        """파일을 파싱한 뒤 스키마 검증까지 수행합니다."""
        data = self.parse_file(path)
        self.validate(data, schema)
        return data
