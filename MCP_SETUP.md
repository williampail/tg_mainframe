# 🔧 MCP (Model Context Protocol) Настройка

## Что такое MCP?

MCP позволяет AI ассистентам взаимодействовать с внешними сервисами (GitHub, файловая система, базы данных) через стандартизированный протокол.

---

## 📁 Структура MCP конфигов

### 1. **Глобальный конфиг** (`~/.config/mcp.json`) ⭐
**Рекомендуемый способ!** Один конфиг для всех AI ассистентов:
- Cursor
- Cline
- Qwen Code
- Claude Desktop
- Kiro

Путь: `~/.config/mcp.json` или `/Users/dim/.config/mcp.json`

### 2. **Локальный конфиг** (`.config/mcp.json` в проекте)
Для специфичных настроек проекта

### 3. **Старый локальный** (`mcp.json` в корне)
Устарел, используй глобальный или `.config/mcp.json`

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

### Шаг 5: Скопируй глобальный конфиг
```bash
# Создать директорию
mkdir -p ~/.config

# Скопировать конфиг из проекта
cp .config/mcp.json ~/.config/mcp.json
```

---

## 📄 Конфигурация для разных AI редакторов

Глобальный конфиг `~/.config/mcp.json` работает со всеми редакторами автоматически!

### **Cursor IDE**
Автоматически читает `~/.config/mcp.json`

### **Cline (VS Code)**
Автоматически читает `~/.config/mcp.json`

### **Qwen Code**
Автоматически читает `~/.config/mcp.json`

### **Kiro**
Автоматически читает `~/.config/mcp.json`

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
