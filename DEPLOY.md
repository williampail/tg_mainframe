# 🚀 Деплой на Render

## Автоматический деплой

1. **Подключи Render к GitHub:**
   - Открой https://render.com/
   - Sign in через GitHub
   - New → **Blueprint**

2. **Импортируй репозиторий:**
   - Выбери `williampail/tg_mainframe`
   - Render автоматически прочитает `render.yaml`

3. **Заполни переменные окружения:**
   В панели Render перейди в настройки сервиса и добавь:
   
   | Key | Value |
   |-----|-------|
   | `TELEGRAM_BOT_TOKEN` | `8606718963:AAHbVUCJ8vo2DbLr8u2iMWf96TlLqu7iUvE` |
   | `OPENROUTER_API_KEY` | `sk-or-xxxxx` (получи на openrouter.ai) |

4. **Deploy:**
   - Нажми **Apply**
   - Render автоматически соберёт и запустит бота

---

## Ручной деплой (альтернатива)

1. **Создай Web Service:**
   - https://dashboard.render.com/new
   - Type: **Web Service**
   - Connect repository: `williampail/tg_mainframe`

2. **Настройки:**
   ```
   Name: mainframe-bot
   Region: Oregon
   Branch: main
   Root Directory: (оставь пустым)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   ```

3. **Plan:** Free

4. **Environment Variables:**
   Добавь те же переменные что выше

---

## После деплоя

1. **Проверь логи** в панели Render
2. **Отправь боту** `/start` в Telegram
3. **Перешли пост** для теста

---

## ⚠️ Важно для бесплатного плана

- **Спящий режим:** Free план засыпает после 15 мин без активности
- **Решение:** 
  - Использовать [UptimeRobot](https://uptimerobot.com/) для пинга
  - Или перейти на план **Starter** ($7/мес)

---

## Мониторинг

- Логи: https://dashboard.render.com → твой сервис → Logs
- Метрики: Metrics tab в панели
