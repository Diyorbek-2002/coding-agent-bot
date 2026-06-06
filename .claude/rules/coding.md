# Coding Qoidalari

## Umumiy qoidalar

- Har doim ishlaydigan, test qilingan kod yoz
- Funksiyalar kichik va bir vazifali bo'lsin
- O'zgaruvchi nomlar ma'noli bo'lsin
- Xatolarni doimo `try/except` bilan ushlat

## Kod yozish tartibi

1. Avval muammoni tushun
2. Oddiy yechim yoz — murakkablashtirma
3. Ishga tushir va natijani ko'r
4. Xato bo'lsa stack trace'ni o'qi, tuzat, qayta ishga tushir
5. Ishlasa, kod tozalab qo'y

## Xato tuzatish

- Stack trace'ning oxirgi qatorini avval o'qi
- Import xatolari: `pip install <paket>`
- `NameError`: o'zgaruvchi nomi xato yoki aniqlanmagan
- `TypeError`: noto'g'ri tip, funksiya imzosini tekshir
- `FileNotFoundError`: fayl yo'lini tekshir

## Agent uchun maxsus

- Har bir kod bloki alohida faylda bo'lsin
- Fayllarni `generated/` papkasiga yoz
- Har doim `main()` funksiya orqali ishga tushir
- Natijani `print()` bilan ko'rsat
