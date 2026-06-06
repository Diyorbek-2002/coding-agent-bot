# Debug Ko'nikmasi

Kod xatolarini avtomatik aniqlash va tuzatish.

## Ishlatish

```
/debug <fayl_nomi>
```

yoki agent ichida `debug_code(file, error)` tool orqali.

## Qadamlar

### 1. Xatoni aniqlash
- `run_code` natijasida `returncode != 0` bo'lsa — xato bor
- `stderr` ni to'liq o'qi
- Xato turini aniqlash: `SyntaxError`, `RuntimeError`, `ImportError`, va h.k.

### 2. Xatoni tahlil qilish
```
Xato: <xato turi>
Fayl: <fayl nomi>, qator: <qator raqami>
Sabab: <qisqa tavsif>
```

### 3. Tuzatish strategiyasi

| Xato turi | Strategiya |
|-----------|-----------|
| `SyntaxError` | Ko'rsatilgan qatorni to'g'rila |
| `ImportError` | `pip install` yoki import yo'lini tekshir |
| `NameError` | O'zgaruvchini aniqlash yoki imlo xatosini tuzat |
| `TypeError` | Tip konversiyasi yoki funksiya imzosini tekshir |
| `IndexError` | Ro'yxat uzunligini tekshir |
| `KeyError` | Dict kalitini `.get()` bilan xavfsiz olish |

### 4. Qayta tekshirish
Tuzatgandan so'ng qayta ishga tushir. Agar xato hali bor — 3-qadamni qayta bajur.

## Misol

```python
# Xato kod
def divide(a, b):
    return a / b

print(divide(10, 0))  # ZeroDivisionError
```

```python
# Tuzatilgan kod
def divide(a, b):
    if b == 0:
        return None
    return a / b

result = divide(10, 0)
print(result if result is not None else "Bo'lish mumkin emas")
```
