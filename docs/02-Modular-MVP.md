---
title: "Отчет №2: Переход на модульную архитектуру (Clean MVP)"
date: 2026-11-15
tags:
  - linux
  - qtile
  - architecture
  - refactoring
  - git
status: completed
branch: refactor/modular-mvp -> dev -> main
---

# Отчет №2: Переход на модульную архитектуру (Clean MVP)

## 🎯 Цель этапа
Отказаться от монолитного файла `config.py` и переписать конфигурацию с нуля в виде чистого, модульного Python-пакета (принцип *Separation of Concerns*). Подготовить масштабируемый фундамент для дальнейшего добавления функций и внедрить базовую темную палитру **Tokyo Night**.

---

## 📂 Новая структура проекта
Конфигурация разбита на независимые логические модули внутри директории `core/`:

```text
~/.config/qtile/
├── config.py              # Лаконичная точка входа (импорты и системные флаги)
├── core/                  # Ядро конфигурации (Python-пакет)
│   ├── __init__.py        # Инициализация пакета
│   ├── colors.py          # Цветовая палитра (Tokyo Night: темный фон + неоновые акценты)
│   ├── keys.py            # Горячие клавиши и управление плавающими окнами мышью
│   ├── groups.py          # Настройка рабочих столов (1–6) и бинды переключения
│   ├── layouts.py         # Раскладки окон (Columns, Max), отступы и правила Floating
│   ├── screens.py         # Конфигурация экрана, верхней панели и базовых виджетов
│   └── hooks.py           # Заглушка для будущих системных событий и автозапуска
├── scripts/               # Директория для вспомогательных bash-скриптов
└── docs/                  # Документация проекта (связана симлинком с Obsidian)
    ├── 01-MVP-Setup.md
    └── 02-Modular-MVP.md  # Текущий отчет
```

---

## 🛠 Выполненные работы

### 1. Разделение ответственности по модулям
* **`core/colors.py`:** Заложена темная цветовая схема (`#1a1b26` фон, `#ff007f` неоново-розовый акцент активных окон, `#7aa2f7` неоново-синий), подготовленная под будущие обои в стиле dark anime / cars.
* **`core/keys.py`:** Настроена навигация в стиле Vim (`h/j/k/l` с клавишей `Super`), управление размером/перемещением окон, вызов терминала (`Super + Enter`) и перезагрузка конфига (`Super + Ctrl + R`).
* **`core/groups.py`:** Создано 6 рабочих столов с автоматической генерацией горячих клавиш для перехода и переноса окон.
* **`core/layouts.py`:** Подключены раскладки `Columns` и `Max` с внешними отступами (`margin: 8px`) и неоновой подсветкой активного окна.
* **`core/screens.py`:** Собрана минималистичная верхняя панель без внешних зависимостей (используются только встроенные виджеты Qtile: `GroupBox`, `Prompt`, `WindowName`, `Systray`, `Clock`, `QuickExit`).
* **`config.py`:** Сокращен до ~20 строк — теперь содержит исключительно сборку модулей и базовые системные параметры Qtile.

### 2. Тестирование и Git Flow
* Синтаксис всех модулей проверен командой `python3 config.py` — ошибок не обнаружено.
* Конфигурация применена в живой сессии (`Super + Ctrl + R`).
* Выполнена полная цепочка Git-слияний: `refactor/modular-mvp` $\rightarrow$ `dev` $\rightarrow$ `main`, все ветки синхронизированы с удаленным репозиторием `SenKen01/qtile-dotfiles`.

---

## 💻 Использованные команды (Лог)
```bash
# Создание ветки рефакторинга от dev
git checkout dev
git checkout -b refactor/modular-mvp

# Создание структуры модулей
mkdir -p core scripts
touch core/__init__.py core/colors.py core/keys.py core/groups.py core/layouts.py core/screens.py core/hooks.py

# Проверка синтаксиса
python3 config.py

# Фиксация и слияние веток (Git Flow)
git add .
git commit -m "refactor: implement clean modular MVP architecture"
git push -u origin refactor/modular-mvp

git checkout dev
git merge refactor/modular-mvp
git push origin dev

git checkout main
git merge dev
git push origin main

# Возврат в рабочую ветку разработки
git checkout dev
```

---

## ✅ Результат и проверка
- [x] Модульная архитектура успешно внедрена и протестирована.
- [x] Сессия Qtile перезапущена без сбоев, применяется темная тема и отступы между окнами.
- [x] Ветки `refactor/modular-mvp`, `dev` и `main` актуальны на GitHub.

## 🚀 Следующие шаги (Backlog)
1. **`feature/autostart-and-wallpaper`:** Реализовать скрипт `scripts/autostart.sh` и хук в `core/hooks.py` для запуска композитора (`picom`), уведомлений (`dunst`), трея и установки темных обоев (аниме + машины).
2. **`feature/scratchpads`:** Добавить выпадающий терминал по горячей клавише в `core/groups.py`.
3. **`feature/rofi-launcher`:** Заменить стандартный `Prompt` на стилизованное меню запуска приложений `Rofi`.
