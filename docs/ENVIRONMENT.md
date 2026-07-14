# Рабочая среда

## Что установлено

- Python 3.12 x64 — основной интерпретатор для обучения.
- Git — система контроля версий.
- Visual Studio Code — редактор кода.
- `.venv` — отдельное окружение библиотек этого проекта.
- Расширения VS Code: Python, Jupyter и Ruff.
- Git-репозиторий с основной веткой `main`.

Старый Python 3.8 не удалён: проект использует Python из `.venv`, поэтому версии не конфликтуют.

## Начало работы в PowerShell

Из папки `Кирилл 2.0` активируй окружение:

```powershell
.\.venv\Scripts\Activate.ps1
```

В начале строки терминала появится `(.venv)`. После этого команды `python` и `pip` относятся к текущему проекту.

Если PowerShell сообщает, что выполнение сценариев отключено, временно разреши локальные сценарии только для текущего терминала:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Настройка `Scope Process` исчезает после закрытия терминала и не изменяет политику для всего компьютера.

Проверь версию:

```powershell
python --version
```

Запусти тесты:

```powershell
python -m unittest discover -s projects/01_python_basics/tests -v
```

Запусти JupyterLab:

```powershell
python -m jupyter lab
```

Завершить работу с окружением:

```powershell
deactivate
```

После `deactivate` команда `python` снова может указывать на системную версию. Проверить выбранный интерпретатор:

```powershell
python -c "import sys; print(sys.executable)"
```

## Восстановление библиотек

Если `.venv` когда-нибудь будет удалена, библиотеки устанавливаются заново командой:

```powershell
python -m pip install -r requirements.txt
```

Папка `.venv` не хранится в Git. В Git хранится небольшой `requirements.txt`, описывающий нужные библиотеки.

## После первоначальной установки

Перезапусти VS Code и Codex один раз. Новый терминал после перезапуска увидит обновлённые команды `python`, `py` и `git` в системном `PATH`. Настройки проекта уже указывают VS Code на `.venv`.

Первый Git-коммит потребует имя и email автора. Их настроим отдельно, когда определим, какой email будет связан с GitHub; случайный адрес в историю проекта не записываем.
