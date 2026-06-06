# Coding Agent

Groq API orqali ishlaydigan mustaqil coding agent. Kod yozadi, ishga tushiradi, xato bo'lsa o'zi tuzatadi.

## Loyiha tuzilmasi

```
coading-agent/
├── agent.py          # Asosiy agent (Groq + tool calling)
├── tools.py          # Asboblar: write, run, read, list
├── requirements.txt
├── .env              # GROQ_API_KEY (gitda yo'q)
├── .env.example
└── .claude/
    ├── settings.json
    ├── hooks/
    │   └── post_file_save.sh
    ├── rules/
    │   └── coding.md
    ├── skills/
    │   └── debug.md
    ├── commands/
    │   └── run.md
    └── agents/
        └── debugger.md
```

## Ishga tushirish

```bash
pip install -r requirements.txt
cp .env.example .env
# .env faylga GROQ_API_KEY ni qo'shing
python agent.py "fibonacci funksiya yoz va test qil"
```

## Agent qanday ishlaydi

1. Foydalanuvchi vazifa beradi
2. Agent Groq LLM orqali reja tuzadi
3. `write_file` tool bilan kod yozadi
4. `run_code` tool bilan ishga tushiradi
5. Xato bo'lsa — stack trace tahlil qilib, o'zi tuzatadi
6. Muvaffaqiyatli natijani qaytaradi

## Muhit o'zgaruvchilari

| O'zgaruvchi | Tavsif |
|-------------|--------|
| `GROQ_API_KEY` | Groq API kaliti (majburiy) |
| `GROQ_MODEL` | Model nomi (default: `llama-3.3-70b-versatile`) |
| `MAX_RETRIES` | Xato tuzatish urinishlari (default: 3) |
