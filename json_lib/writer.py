import json
import os
import tempfile
from typing import Any, Union
from .exceptions import JsonWriteError


class JsonWriter:
    """Python 객체를 JSON 파일로 저장하는 클래스"""

    def __init__(
        self,
        indent: int = 2,
        ensure_ascii: bool = False,
        encoding: str = "utf-8",
    ):
        self.indent = indent
        self.ensure_ascii = ensure_ascii
        self.encoding = encoding

    # ── 직렬화 ────────────────────────────────────────────

    def to_string(self, data: Any, *, compact: bool = False) -> str:
        """Python 객체를 JSON 문자열로 변환합니다."""
        indent = None if compact else self.indent
        try:
            return json.dumps(data, indent=indent, ensure_ascii=self.ensure_ascii)
        except (TypeError, ValueError) as e:
            raise JsonWriteError(f"직렬화 오류: {e}") from e

    # ── 파일 저장 ──────────────────────────────────────────

    def save(self, data: Any, path: str, *, atomic: bool = True) -> None:
        """
        Python 객체를 JSON 파일로 저장합니다.

        atomic=True (기본값): 임시 파일에 먼저 쓴 뒤 교체하여
        저장 도중 오류가 발생해도 기존 파일이 손상되지 않습니다.
        """
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        content = self.to_string(data)

        if atomic:
            self._atomic_write(path, content)
        else:
            self._direct_write(path, content)

    def save_compact(self, data: Any, path: str) -> None:
        """들여쓰기 없이 한 줄 JSON으로 저장합니다."""
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        content = self.to_string(data, compact=True)
        self._atomic_write(path, content)

    def append_to_array(self, item: Any, path: str) -> None:
        """
        기존 JSON 배열 파일에 항목을 추가합니다.
        파일이 없으면 새 배열을 생성합니다.
        """
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding=self.encoding) as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                raise JsonWriteError(f"기존 파일 읽기 실패: {e}") from e

            if not isinstance(existing, list):
                raise JsonWriteError(f"[{path}] 는 JSON 배열 파일이 아닙니다.")
            existing.append(item)
            self.save(existing, path)
        else:
            self.save([item], path)

    def merge(self, updates: dict, path: str) -> None:
        """
        기존 JSON 오브젝트에 키-값을 병합(업데이트)합니다.
        파일이 없으면 새로 생성합니다.
        """
        if not isinstance(updates, dict):
            raise JsonWriteError("merge() 에는 dict 타입만 사용할 수 있습니다.")

        existing: dict = {}
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding=self.encoding) as f:
                    existing = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                raise JsonWriteError(f"기존 파일 읽기 실패: {e}") from e

            if not isinstance(existing, dict):
                raise JsonWriteError(f"[{path}] 는 JSON 오브젝트 파일이 아닙니다.")

        existing.update(updates)
        self.save(existing, path)

    # ── 내부 헬퍼 ─────────────────────────────────────────

    def _atomic_write(self, path: str, content: str) -> None:
        dir_name = os.path.dirname(os.path.abspath(path))
        try:
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding=self.encoding) as f:
                    f.write(content)
                os.replace(tmp_path, path)
            except Exception:
                os.unlink(tmp_path)
                raise
        except OSError as e:
            raise JsonWriteError(f"[{path}] 파일 저장 실패: {e}") from e

    def _direct_write(self, path: str, content: str) -> None:
        try:
            with open(path, "w", encoding=self.encoding) as f:
                f.write(content)
        except OSError as e:
            raise JsonWriteError(f"[{path}] 파일 저장 실패: {e}") from e
