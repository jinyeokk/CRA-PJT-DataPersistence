import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.model import User
from app.repository import UserRepository

repo = UserRepository("data/test_users.json")

# 테스트 파일 초기화
if os.path.isfile("data/test_users.json"):
    os.remove("data/test_users.json")

print("=" * 50)
print("  CRUD 통합 테스트")
print("=" * 50)

# ── Create ────────────────────────────────────────
u1 = repo.create(User(name="홍길동", age=30, email="hong@example.com"))
u2 = repo.create(User(name="김철수", age=25, email="kim@example.com"))
u3 = repo.create(User(name="이영희", age=28, email="lee@example.com"))
print(f"[Create] ID={u1.id} {u1.name}, ID={u2.id} {u2.name}, ID={u3.id} {u3.name}")

# ── Read All ──────────────────────────────────────
all_users = repo.read_all()
print(f"[Read All] 총 {len(all_users)}명: {[u.name for u in all_users]}")

# ── Read by ID ────────────────────────────────────
found = repo.read_by_id(2)
print(f"[Read ID=2] {found.name} / {found.email}")

# ── Search ────────────────────────────────────────
results = repo.search("김")
print(f"[Search '김'] {[u.name for u in results]}")

# ── Update ────────────────────────────────────────
updated = repo.update(2, {"name": "김영수", "age": 26})
print(f"[Update ID=2] 이름={updated.name}, 나이={updated.age}")

# ── Delete ────────────────────────────────────────
ok = repo.delete(3)
print(f"[Delete ID=3] 성공={ok}")

# ── 최종 목록 ─────────────────────────────────────
final = repo.read_all()
print(f"[최종 목록] {[(u.id, u.name) for u in final]}")

# ── 예외 처리 ─────────────────────────────────────
print(f"[없는 ID=99] {repo.read_by_id(99)}")
print(f"[없는 삭제] 성공={repo.delete(99)}")

print("=" * 50)
print("  모든 테스트 통과")
print("=" * 50)

# 최종 JSON 파일 내용 출력
print("\n-- 최종 저장된 JSON 파일 --")
with open("data/test_users.json", "r", encoding="utf-8") as f:
    print(f.read())

# 테스트 파일 정리
os.remove("data/test_users.json")
