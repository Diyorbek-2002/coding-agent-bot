# /run Buyrug'i

Agent orqali kod yozib, ishga tushiradi va natijani ko'rsatadi.

## Sintaksis

```
/run <vazifa tavsifi>
```

## Misолlar

```
/run fibonacci sonlarini hisoblash funksiyasi yoz
/run CSV faylni o'qib statistika chiqar
/run oddiy HTTP server yoz port 8080 da
/run ro'yxatni tartiblash algoritmlarini solishtir
```

## Jarayon

1. Vazifani tahlil qiladi
2. Kod yozadi (`generated/<nom>.py`)
3. `python generated/<nom>.py` bilan ishga tushiradi
4. Xato bo'lsa — avtomatik tuzatib qayta ishga tushiradi (max 3 urinish)
5. Natija va kodni ko'rsatadi

## Opsiyalar

`/run --file <fayl>` — mavjud faylni ishga tushiradi  
`/run --test <vazifa>` — unittest bilan test yozadi  
`/run --explain <vazifa>` — kod yozadi va tushuntiradi
