import sys

# Windows 터미널 UTF-8 출력 보장 (reconfigure 는 래핑 없이 인코딩만 변경)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except AttributeError:
        pass  # Python 3.6 이하 무시

from app.console import run

if __name__ == "__main__":
    run()
