import subprocess
import json
from pathlib import Path

GENERATED_DIR = Path("generated")
GENERATED_DIR.mkdir(exist_ok=True)


def write_file(filename: str, content: str) -> dict:
    path = GENERATED_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {"success": True, "path": str(path)}


def read_file(filepath: str) -> dict:
    path = Path(filepath)
    if not path.exists():
        path = GENERATED_DIR / filepath
    if not path.exists():
        return {"success": False, "message": f"Fayl topilmadi: {filepath}"}
    return {"success": True, "content": path.read_text(encoding="utf-8")}


def run_code(filepath: str, timeout: int = 30) -> dict:
    path = Path(filepath)
    if not path.exists():
        path = GENERATED_DIR / filepath
    if not path.exists():
        return {"success": False, "stdout": "", "stderr": f"Fayl topilmadi: {filepath}"}
    try:
        result = subprocess.run(
            ["python", str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": f"Timeout: {timeout}s"}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e)}


def list_files(directory: str = "generated") -> dict:
    path = Path(directory)
    if not path.exists():
        return {"success": True, "files": []}
    files = [str(f.relative_to(path)) for f in path.rglob("*") if f.is_file()]
    return {"success": True, "files": sorted(files)}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Python kod faylini generated/ papkasiga yozadi",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Fayl nomi (masalan: solution.py)"},
                    "content": {"type": "string", "description": "Fayl mazmuni"},
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Mavjud faylni o'qiydi",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Fayl nomi yoki yo'li"},
                },
                "required": ["filepath"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_code",
            "description": "Python faylni ishga tushiradi va stdout/stderr qaytaradi",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Ishga tushiriladigan fayl nomi"},
                    "timeout": {"type": "integer", "description": "Maksimal kutish vaqti (soniya)", "default": 30},
                },
                "required": ["filepath"],
            },
        },
    },
]
