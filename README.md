# BarberTop Telegram Bot

Ushbu loyiha BarberTop uchun ishlab chiqarishga tayyor (production-ready) bo'lgan, enterprise arxitekturadagi Telegram bot hisoblanadi.

## Texnologiyalar

- Python 3.13+
- aiogram 3.x
- SQLAlchemy 2.0 (Async) + asyncpg
- PostgreSQL 15
- Redis (FSM va Throttling uchun)
- Alembic (Migratsiyalar)
- Docker & Docker Compose

## Papkalar tuzilmasi

```text
barbertop_bot/
├── alembic/                # Migratsiya skriptlari
├── bot/                    # Asosiy bot mantiqi
│   ├── database/           # DB modellar, crud va ulanish
│   ├── handlers/           # Telegram xabarlarni tutish
│   ├── keyboards/          # Inline va Reply klaviaturalar
│   ├── middlewares/        # Logging, Throttling, User
│   └── utils/              # Yordamchi xizmatlar (Broadcaster)
├── config.py               # .env o'qish
├── loader.py               # Bot obyekti initsializatsiyasi
├── main.py                 # Botni yurgizish
├── alembic.ini             # Alembic konfiguratsiyasi
├── docker-compose.yml      # Docker xizmatlari
├── Dockerfile              # Bot image builder
└── requirements.txt        # Kutubxonalar
```

## O'rnatish va Ishga Tushirish

### 1. Muhitni sozlash

`.env.example` faylidan nusxa olib `.env` yarating:
```bash
cp .env.example .env
```
Fayl ichidagi o'zgaruvchilarni (tokenlar, DB parollari) o'zgartiring.

### 2. Docker orqali yurgizish

Docker Compose orqali DB va Redis ni ishga tushiramiz:
```bash
docker-compose up -d db redis
```

### 3. Migratsiyalarni amalga oshirish

Bot ishlashidan oldin jadvallarni yaratish kerak. Agar bot kompyuteringizda bo'lsa:
```bash
alembic upgrade head
```
Agar to'liq Docker ichida qilmoqchi bo'lsangiz, bot konteyneriga ulanib `alembic upgrade head` qiling yoki CI/CD da ssenariy sifatida ishlating.

### 4. Botni ishga tushirish
To'liq muhit bilan:
```bash
docker-compose up -d
```
Bot loglarini ko'rish:
```bash
docker-compose logs -f bot
```

## Imkoniyatlari

- **WebApp integratsiyasi**: Saytni Telegram ichida ochish.
- **Support Chat**: Mijozlar adminlarga to'g'ridan-to'g'ri xabar yozishi va adminlarning Reply orqali javob berishi.
- **Yangiliklar tizimi**: Pagination bilan ishlaydigan rasm va matnli postlar.
- **FAQ tizimi**: Baza bilan ulangan javoblar.
- **Admin Panel**: Statistika, Yangilik qo'shish/o'chirish, Broadcast (flood control bilan).
- **Kafolatli ishlash**: Global error handling, Throttling (spam himoyasi), Auto-reconnect.
