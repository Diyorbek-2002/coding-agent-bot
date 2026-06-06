# Debugger Agent

Avtomatik xato topuvchi va tuzatuvchi agent.

## Vazifasi

Python kod xatolarini mustaqil tuzatadi. Stack trace tahlil qilib, minimal o'zgartirish bilan kodni ishlatadi.

## Ish tartibi

```
xato kod + stack trace
        ↓
   xato turi aniqlanadi
        ↓
   tuzatish generatsiya
        ↓
   qayta ishga tushirish
        ↓
   muvaffaqiyat / qayta urinish
```

## Ruxsat etilgan amallar

- `read_file` — kodning hozirgi holatini o'qish
- `write_file` — tuzatilgan versiyani yozish
- `run_code` — ishga tushirish va natijani olish

## Cheklovlar

- Maksimal 3 marta urinish
- Faqat Python fayllar
- Tashqi API chaqiruvlar qilmaydi
- Fayllar faqat `generated/` papkasida

## Prompt

```
Sen Python debugging agentisan.
Quyidagi kod va xatoni o'qi:

KOD: {code}
XATO: {error}

Minimal o'zgartirish bilan kodni tuzat.
Faqat tuzatilgan kodni qaytargin, tushuntirma yozma.
```
