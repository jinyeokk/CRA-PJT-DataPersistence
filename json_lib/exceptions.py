class JsonParseError(Exception):
    """JSON 파싱 실패 시 발생"""

class JsonWriteError(Exception):
    """JSON 파일 저장 실패 시 발생"""

class JsonValidationError(Exception):
    """JSON 스키마 검증 실패 시 발생"""
