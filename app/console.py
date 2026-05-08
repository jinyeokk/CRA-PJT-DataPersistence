import os
import sys
from typing import Optional

from .model import User
from .repository import UserRepository

_repo = UserRepository()

# ── 출력 유틸 ─────────────────────────────────────────────────────────────────

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _header(title: str) -> None:
    print("=" * 52)
    print(f"  {title}")
    print("=" * 52)


def _divider() -> None:
    print("  " + "-" * 48)


def _print_table(users: list[User]) -> None:
    if not users:
        print("  데이터가 없습니다.")
        return
    print(f"  {'ID':<5} {'이름':<12} {'나이':<6} 이메일")
    _divider()
    for u in users:
        print(f"  {u.id:<5} {u.name:<12} {u.age:<6} {u.email}")


def _print_user(user: User) -> None:
    print(f"  ID    : {user.id}")
    print(f"  이름  : {user.name}")
    print(f"  나이  : {user.age}")
    print(f"  이메일: {user.email}")


# ── 입력 유틸 ─────────────────────────────────────────────────────────────────

def _input(prompt: str) -> str:
    return input(f"  {prompt}: ").strip()


def _input_int(prompt: str) -> Optional[int]:
    raw = _input(prompt)
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        print("  [오류] 숫자를 입력하세요.")
        return None


def _pause() -> None:
    input("\n  엔터를 눌러 메뉴로 돌아갑니다...")


# ── Create ────────────────────────────────────────────────────────────────────

def _menu_create() -> None:
    _header("새 사용자 추가 (Create)")

    name = _input("이름")
    if not name:
        print("  [오류] 이름을 입력해야 합니다.")
        return

    age = _input_int("나이")
    if age is None:
        return

    email = _input("이메일")
    if not email:
        print("  [오류] 이메일을 입력해야 합니다.")
        return

    user = _repo.create(User(name=name, age=age, email=email))
    print(f"\n  [완료] 사용자가 추가되었습니다.")
    _divider()
    _print_user(user)


# ── Read ──────────────────────────────────────────────────────────────────────

def _menu_read_all() -> None:
    _header("전체 목록 조회 (Read)")
    users = _repo.read_all()
    _print_table(users)
    print(f"\n  총 {len(users)}건")


def _menu_search() -> None:
    _header("검색 (Read - Search)")
    print("  1. ID 로 검색")
    print("  2. 이름 / 이메일 키워드 검색")
    _divider()
    choice = _input("선택")

    if choice == "1":
        user_id = _input_int("ID")
        if user_id is None:
            return
        user = _repo.read_by_id(user_id)
        if user:
            _divider()
            _print_user(user)
        else:
            print(f"  [없음] ID {user_id} 에 해당하는 사용자가 없습니다.")

    elif choice == "2":
        keyword = _input("검색어")
        results = _repo.search(keyword)
        _divider()
        _print_table(results)
        print(f"\n  검색 결과: {len(results)}건")

    else:
        print("  [오류] 1 또는 2 를 입력하세요.")


# ── Update ────────────────────────────────────────────────────────────────────

def _menu_update() -> None:
    _header("데이터 수정 (Update)")

    user_id = _input_int("수정할 사용자 ID")
    if user_id is None:
        return

    user = _repo.read_by_id(user_id)
    if not user:
        print(f"  [없음] ID {user_id} 에 해당하는 사용자가 없습니다.")
        return

    print("\n  현재 정보:")
    _divider()
    _print_user(user)
    print("\n  수정할 값을 입력하세요. (변경하지 않으려면 엔터 입력)")
    _divider()

    new_name  = input(f"  이름   [{user.name}]: ").strip()
    new_age_s = input(f"  나이   [{user.age}]: ").strip()
    new_email = input(f"  이메일 [{user.email}]: ").strip()

    fields: dict = {}
    if new_name:
        fields["name"] = new_name
    if new_age_s:
        try:
            fields["age"] = int(new_age_s)
        except ValueError:
            print("  [오류] 나이는 숫자여야 합니다.")
            return
    if new_email:
        fields["email"] = new_email

    if not fields:
        print("\n  [취소] 변경된 내용이 없습니다.")
        return

    updated = _repo.update(user_id, fields)
    print("\n  [완료] 수정되었습니다.")
    _divider()
    _print_user(updated)


# ── Delete ────────────────────────────────────────────────────────────────────

def _menu_delete() -> None:
    _header("데이터 삭제 (Delete)")

    user_id = _input_int("삭제할 사용자 ID")
    if user_id is None:
        return

    user = _repo.read_by_id(user_id)
    if not user:
        print(f"  [없음] ID {user_id} 에 해당하는 사용자가 없습니다.")
        return

    print("\n  삭제 대상:")
    _divider()
    _print_user(user)
    _divider()
    confirm = _input("정말 삭제하시겠습니까? (y / N)")

    if confirm.lower() != "y":
        print("  [취소] 삭제가 취소되었습니다.")
        return

    _repo.delete(user_id)
    print(f"\n  [완료] ID {user_id} 사용자가 삭제되었습니다.")


# ── 메인 루프 ─────────────────────────────────────────────────────────────────

_MENU = {
    "1": ("사용자 추가    (Create)",          _menu_create),
    "2": ("전체 목록 보기 (Read)",            _menu_read_all),
    "3": ("검색          (Read - Search)",   _menu_search),
    "4": ("데이터 수정   (Update)",           _menu_update),
    "5": ("데이터 삭제   (Delete)",           _menu_delete),
}


def run() -> None:
    while True:
        _clear()
        _header("JSON CRUD 콘솔 애플리케이션")
        for key, (label, _) in _MENU.items():
            print(f"  {key}. {label}")
        print("  0. 종료")
        print("=" * 52)

        choice = _input("메뉴 선택")

        if choice == "0":
            print("\n  프로그램을 종료합니다.")
            sys.exit(0)

        if choice in _MENU:
            print()
            _MENU[choice][1]()
        else:
            print("  [오류] 0~5 중 하나를 입력하세요.")

        _pause()
