"""
main.py 콘솔 메뉴를 자동 입력으로 시연하는 스크립트.
subprocess 로 main.py 를 띄우고 stdin 에 한 줄씩 전달한다.
"""
import subprocess
import sys
import time

PYTHON = r".\.venv\Scripts\python.exe"

STEPS = [
    # (설명,  입력 줄 목록)
    ("[ 1 ] Create — 홍길동 추가",         ["1", "홍길동", "30", "hong@example.com"]),
    ("[ 2 ] Create — 김철수 추가",         ["1", "김철수", "25", "kim@example.com"]),
    ("[ 3 ] Create — 이영희 추가",         ["1", "이영희", "28", "lee@example.com"]),
    ("[ 4 ] Read   — 전체 목록 조회",      ["2"]),
    ("[ 5 ] Read   — ID=2 검색",           ["3", "1", "2"]),
    ("[ 6 ] Read   — 키워드 '김' 검색",    ["3", "2", "김"]),
    ("[ 7 ] Update — ID=2 이름·나이 수정", ["4", "2", "김영수", "26", ""]),
    ("[ 8 ] Read   — 수정 후 전체 목록",   ["2"]),
    ("[ 9 ] Delete — ID=3 삭제",           ["5", "3", "y"]),
    ("[ 10] Read   — 삭제 후 전체 목록",   ["2"]),
]

SEP = "─" * 60

# 전체 입력 스트림 구성 (각 단계 사이에 엔터(pause) 포함)
all_lines: list[str] = []
for _, inputs in STEPS:
    all_lines.extend(inputs)
    all_lines.append("")   # _pause() 용 엔터
all_lines.append("0")      # 종료

stdin_data = "\n".join(all_lines) + "\n"

# main.py 실행
proc = subprocess.run(
    [PYTHON, "main.py"],
    input=stdin_data,
    capture_output=True,
    text=True,
    encoding="utf-8",
    env={**__import__("os").environ, "PYTHONUTF8": "1"},
)

output = proc.stdout

# ── 출력을 단계별로 분리해서 보기 좋게 표시 ───────────────────────
# "엔터를 눌러 메뉴로 돌아갑니다..." 기준으로 분리
blocks = output.split("엔터를 눌러 메뉴로 돌아갑니다...")

step_idx = 0
for block in blocks:
    block = block.strip()
    if not block:
        continue
    # 메인 메뉴 블록은 건너뜀 (단계 설명이 없는 경우)
    label = STEPS[step_idx][0] if step_idx < len(STEPS) else "[ 종료 ]"
    print(f"\n{SEP}")
    print(f"  {label}")
    print(SEP)
    print(block)
    step_idx += 1

if proc.returncode not in (0, 1):
    print("\n[stderr]", proc.stderr)
