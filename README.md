TechCockpit v0.2

Панель разработчика: мониторинг системы + очистка кэша.

Основные фичи

| Кнопка | Что делает |
|--------|------------|
| **System Info** | CPU/GPU/RAM в реальном времени |
| **Cache Flush** | (TEMP + Chrome/Discord/Steam) |
| **Make Working Place** | Яндекс.Музыка + Perplexity + PyCharm |
| **Live Monitor** | Живые статы в одном окне |

Запуск

```bash
pip install psutil
set PYCHARM_PATH="C:\Program Files\JetBrains\PyCharm 2025.3.2\bin\pycharm64.exe"
python gui/main_window.py
