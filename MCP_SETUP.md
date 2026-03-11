# 🔧 MCP (Model Context Protocol) Настройка

## Что такое MCP?

MCP позволяет AI ассистентам взаимодействовать с внешними сервисами (GitHub, файловая система, базы данных) через стандартизированный протокол.

---

## 📁 Структура MCP конфигов

### 1. **Локальный конфиг** (`mcp.json`)
Для локальной разработки с AI ассистентами (Cursor, Cline, etc.)

### 2. **Глобальный конфиг** (`~/.config/mcp.json`)
Для системных MCP серверов

---

## 🚀 Установка

### Шаг 1: Установи Node.js (если нет)
```bash
# Проверка
node --version

# Установка (macOS)
brew install node
```

### Шаг 2: Установи MCP серверы
```bash
# GitHub MCP сервер
npm install -g @modelcontextprotocol/server-github

# Filesystem MCP сервер
npm install -g @modelcontextprotocol/server-filesystem
```

### Шаг 3: Создай GitHub Personal Access Token
1. Открой https://github.com/settings/tokens
2. **Generate new token (classic)**
3. Выбери скоупы:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `read:org` (Read org data)
4. Скопируй токен

### Шаг 4: Добавь токен в окружение
```bash
# macOS/Linux (~/.zshrc или ~/.bashrc)
export GITHUB_TOKEN="ghp_твои_токен"

# Применить
source ~/.zshrc
```

---

## 📄 Конфигурация для разных AI редакторов

### **Cursor IDE**
1. Открой `Settings → AI → MCP Servers`
2. Добавь из `mcp.json`
3. Restart Cursor

### **Cline (VS Code)**
1. Открой настройки Cline
2. MCP Servers → Add Server
3. Укажи путь к `mcp.json`

### **Claude Desktop**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_твои_токен"
      }
    }
  }
}
```

---

## 🛠️ Доступные MCP команды

### GitHub Server:
```
- create_repository
- get_repository
- list_repositories
- create_issue
- get_issue
- list_issues
- create_pull_request
- get_pull_request
- list_pull_requests
- search_repositories
- get_file_contents
- create_branch
- push_files
```

### Filesystem Server:
```
- read_file
- write_file
- list_directory
- search_files
- get_file_info
```

---

## 📝 Примеры использования

### Создать issue через AI:
```
"Создай issue для добавления генерации изображений"
```

### Прочитать файл:
```
"Покажи содержимое bot.py"
```

### Найти файлы:
```
"Найди все Python файлы с обработчиками"
```

---

## 🔐 Безопасность

⚠️ **Никогда не коммить `.env` с токенами!**

Проверь `.gitignore`:
```
.env
*.token
secrets/
```

### Для production используй:
- GitHub Secrets (для Actions)
- Render Environment Variables
- Doppler / Vault для секретов

---

## 🐛 Troubleshooting

### MCP сервер не подключается:
```bash
# Проверь установку
npx -y @modelcontextprotocol/server-github --version

# Проверь токен
echo $GITHUB_TOKEN
```

### Ошибка авторизации GitHub:
- Пересоздай токен на https://github.com/settings/tokens
- Убедись что скоупы правильные
- Обновить в `.zshrc` и `source ~/.zshrc`

### Файлы не читаются:
- Проверь путь в `mcp.json`
- Убедись что файл существует
- Проверь права доступа

---

## 🔗 Полезные ссылки

- **MCP Spec**: https://modelcontextprotocol.io/
- **GitHub MCP**: https://github.com/modelcontextprotocol/servers/tree/main/src/github
- **Filesystem MCP**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **Awesome MCP**: https://github.com/punkpeye/awesome-mcp

---

## 📋 Чеклист настройки

- [ ] Node.js установлен
- [ ] MCP серверы установлены (`npm install -g`)
- [ ] GitHub токен создан
- [ ] Токен добавлен в `.zshrc`
- [ ] `mcp.json` настроен
- [ ] AI редактор подключён к MCP
- [ ] Тестовая команда работает
