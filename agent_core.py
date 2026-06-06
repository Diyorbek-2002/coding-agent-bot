"""
agent_core.py — Agent yadrosi (bot va terminal uchun umumiy)
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv
from tools import write_file, run_code, read_file, TOOLS

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """Sen — AI Coding Agent. Vazifang:
1. Foydalanuvchi so'ragan kodni Python da yoz
2. Faylga saqlа (write_file)
3. Ishga tushir (run_code)
4. Xato bo'lsa o'zing tuzat (max 3 marta)
5. Natijani QISQA qilib qaytар — Telegram uchun 3000 belgidan oshmasin

MUHIM: Javobingni qisqa yoz. Faqat asosiy natija va fayl nomi.
"""


def run_tool(name: str, args: dict) -> str:
    if name == "write_file":
        return json.dumps(write_file(args["filename"], args["content"]), ensure_ascii=False)
    elif name == "run_code":
        return json.dumps(run_code(args["filepath"]), ensure_ascii=False)
    elif name == "read_file":
        return json.dumps(read_file(args["filepath"]), ensure_ascii=False)
    return json.dumps({"success": False, "message": f"Noma'lum tool: {name}"})


def run_agent(user_message: str, max_iter: int = 8) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    last_text = ""
    written_files = {}   # filename -> code
    run_results = {}     # filepath -> {success, stdout, stderr}

    for _ in range(max_iter):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            max_tokens=2048
        )

        msg = response.choices[0].message

        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in (msg.tool_calls or [])
            ] if msg.tool_calls else None
        })

        if msg.content:
            last_text = msg.content

        if not msg.tool_calls:
            break

        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            result_str = run_tool(name, args)
            result = json.loads(result_str)

            # Yozilgan faylni eslab qol
            if name == "write_file" and result.get("success"):
                written_files[args["filename"]] = args["content"]

            # Ishga tushirish natijasini eslab qol
            if name == "run_code":
                run_results[args["filepath"]] = {
                    "success": result.get("success"),
                    "stdout": result.get("stdout", ""),
                    "stderr": result.get("stderr", "")
                }

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result_str
            })

    # Chiroyli natija yasash
    parts = []

    for filename, code in written_files.items():
        # Telegram uchun 2000 belgi limit
        if len(code) > 2000:
            code = code[:2000] + "\n... (qisqartirildi)"
        parts.append(f"📄 `{filename}`:\n```python\n{code}\n```")

    for filepath, res in run_results.items():
        if res["success"] and res["stdout"].strip():
            stdout = res["stdout"].strip()
            if len(stdout) > 500:
                stdout = stdout[:500] + "\n... (qisqartirildi)"
            parts.append(f"▶️ Chiqish:\n```\n{stdout}\n```")
        elif not res["success"] and res["stderr"].strip():
            stderr = res["stderr"].strip()[:500]
            parts.append(f"❌ Xato:\n```\n{stderr}\n```")

    if last_text:
        parts.append(last_text)

    return "\n\n".join(parts) if parts else "✅ Vazifa bajarildi."