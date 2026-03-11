# 📋 План развития Telegram бота MAINFRAME

## 🎯 Текущая архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    TELEGRAM BOT                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Receiver   │→ │   Rewriter   │→ │   Publisher      │  │
│  │  (forward)   │  │  (OpenRouter)│  │   (@mainframe_sh)│  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📌 ЭТАП 1: Генерация изображений (Nano Banana 2)

### Что нужно:

1. **Модель для генерации**
   - Nano Banana 2 через OpenRouter (если доступна)
   - Альтернативы:
     - `black-forest-labs/flux-1.1-pro` (платная, качественная)
     - `stability-ai/stable-diffusion-3.5-large` (платная)
     - Бесплатные: `playground/playground-v2.5-1024px-aesthetic`

2. **Промпт-инженерия**
   - Создать шаблон промптов в стиле MAINFRAME
   - Cyberpunk/терминал эстетика
   - Автоматическое извлечение ключевых слов из статьи

3. **Интеграция в бота**
   - Модуль `image_generator.py`
   - Генерация после переписывания текста
   - Публикация текста + изображения

### Структура промпта для изображения:
```
Cyberpunk terminal aesthetic, minimalist tech visualization,
neon green and black color scheme, [ТЕМА_СТАТЬИ],
digital art, futuristic interface, 4K
```

### Пример кода (image_generator.py):
```python
from openai import OpenAI

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

def generate_image(prompt: str) -> str:
    # Для моделей с поддержкой image generation
    # Или использовать отдельный API (Stability AI, Replicate)
    pass
```

### ⚠️ Важно:
- OpenRouter в основном для **текстовых** моделей
- Для изображений лучше использовать:
  - **Stability AI API** (стабильная диффузия)
  - **Replicate API** (разные модели)
  - **Pollinations.ai** (бесплатно, без API ключа)

---

## 📌 ЭТАП 2: Партнёрские программы

### Что нужно:

1. **База партнёрских ссылок**
   ```json
   {
     "notion": "https://notion.so/?via=your_id",
     "zapier": "https://zapier.com/?partner=your_id",
     "make": "https://make.com/?ref=your_id"
   }
   ```

2. **Модуль affiliate_matcher.py**
   - Анализ текста на упоминания инструментов
   - Автоматическая замена на партнёрские ссылки
   - NLP для распознавания названий (NLP)

3. **Источники партнёрок:**
   - **PartnerStack** — SaaS инструменты
   - **Impact** — tech сервисы
   - **Direct** — напрямую у сервисов

### Пример логики:
```python
AFFILIATE_LINKS = {
    "notion": "https://notion.so/?via=mainframe_{{REF}}",
    "zapier": "https://zapier.com/?partner=mainframe_{{REF}}",
    "make": "https://make.com/?ref=mainframe_{{REF}}",
    "airtable": "https://airtable.com/?r=mainframe_{{REF}}",
}

def add_affiliate_links(text: str) -> str:
    for tool, link in AFFILIATE_LINKS.items():
        if tool.lower() in text.lower():
            text = text.replace(tool, f"[{tool}]({link})")
    return text
```

---

## 📌 ЭТАП 3: Улучшения бота

### 3.1 Админ-панель
- `/stats` — статистика постов
- `/style <new_style>` — изменение стиля на лету
- `/affiliate add <tool> <link>` — добавление партнёрки

### 3.2 Очередь постов
- Планирование публикаций
- Отложенный постинг
- Queue management

### 3.3 Мульти-канальность
- Публикация в несколько каналов
- A/B тестирование заголовков

### 3.4 Аналитика
- Сохранение статистики (SQLite/PostgreSQL)
- Просмотры, клики, вовлечённость
- Интеграция с Google Analytics

---

## 📌 ЭТАП 4: Продвинутые функции

### 4.1 Авто-категоризация
- Определение темы поста
- Автоматические хештеги
- Роутинг по рубрикам

### 4.2 RAG (Retrieval-Augmented Generation)
- База знаний ваших прошлых постов
- Контекст для более точного стиля
- Векторная БД (Chroma, Pinecone)

### 4.3 Web-интерфейс
- Dashboard для управления
- Предпросмотр перед публикацией
- Редактирование стиля

### 4.4 Мультиязычность
- Перевод постов
- Локализация для разных аудиторий

---

## 💡 Советы для MAINFRAME

### Контент:
1. **Консистентность стиля** — сохраняй терминальную эстетику
2. **Короткие посты** — 200-400 символов идеально для Telegram
3. **Визуал** — каждое изображение должно быть в стиле канала
4. **CTA** — добавляй призывы к действию (ссылки, боты, каналы)

### Техническое:
1. **Логирование** — сохраняй все ошибки и успешные посты
2. **Rate limiting** — OpenRouter имеет лимиты
3. **Backup** — сохраняй оригиналы постов
4. **Testing** — тестовый канал перед публикацией

### Монетизация:
1. **Партнёрки** — основной доход
2. **Спонсорские посты** — платные размещения
3. **Premium контент** — закрытый канал
4. **Digital продукты** — гайды, шаблоны, курсы

---

## 📊 Дорожная карта

| Этап | Функция | Приоритет | Время |
|------|---------|-----------|-------|
| 1 | Генерация изображений | 🔴 Высокий | 1-2 дня |
| 2 | Партнёрские ссылки | 🔴 Высокий | 1 день |
| 3 | Админ-команды | 🟡 Средний | 1 день |
| 4 | Аналитика | 🟡 Средний | 2-3 дня |
| 5 | RAG для стиля | 🟢 Низкий | 3-5 дней |
| 6 | Web dashboard | 🟢 Низкий | 5-7 дней |

---

## 🛠️ Рекомендуемый стек для развития

```
Backend:
- Python 3.9+
- python-telegram-bot
- OpenRouter API
- SQLite/PostgreSQL (аналитика)

Image Generation:
- Pollinations.ai (бесплатно)
- Stability AI API
- Replicate API

Deployment:
- Docker
- VPS (DigitalOcean, Hetzner)
- Systemd / Supervisor

Monitoring:
- Sentry (ошибки)
- Prometheus + Grafana (метрики)
```

---

## 📝 Следующие шаги

1. [ ] Выбрать сервис для генерации изображений
2. [ ] Создать `image_generator.py`
3. [ ] Зарегистрировать партнёрские программы
4. [ ] Создать `affiliate_matcher.py`
5. [ ] Добавить админ-команды
6. [ ] Настроить логирование и аналитику

---

## 🔗 Полезные ресурсы

- **OpenRouter**: https://openrouter.ai/models
- **PartnerStack**: https://partnerstack.com/
- **Pollinations.ai**: https://pollinations.ai/ (бесплатные изображения)
- **Stability AI**: https://platform.stability.ai/
- **Replicate**: https://replicate.com/
- **Telegram Bot API**: https://core.telegram.org/bots/api
