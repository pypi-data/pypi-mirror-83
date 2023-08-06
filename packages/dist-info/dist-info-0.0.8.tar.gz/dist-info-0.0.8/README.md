# NAME

dist-info - получить информацию об установленном дистрибутиве

# VERSION

0.0.8

# SYNOPSIS

```python
# Устанавливаваем некий модуль:
$ pip3 install pytest

# И затем в питоне:
# @@ examples.py
from dist_info import dists, metadata, files, modules, \
	modules_in_dir, modules_from, \
	imports, imports_from

# Список всех установленных пакетов:
packages = dists()
# -> ['Brlapi', 'Dumper', ...]

DIST_NAME = 'pytest'

# Получаем путь к каталогу с файлами пакета
src_dir = src_path(DIST_NAME)
# -> '/home/dart/.local/lib/python3.6/site-packages/pytest'

# Получаем каталоги с модулями пакета и путь к метаинформации
# (может быть как файлом, так и каталогом)
dist_dir, egg_dir = dist_info_paths(DIST_NAME)
# -> '/home/dart/.local/lib/python3.6/site-packages', 
#    '/home/dart/.local/lib/python3.6/site-packages/pytest-5.4.1.dist-info'

# Получаем файлы
package_files = files(DIST_NAME)
# [ '/home/dart/.local/lib/python3.6/site-packages/../../../bin/py.test',
#   '/home/dart/.local/lib/python3.6/site-packages/../../../bin/pytest', ... ]

# Получаем модули пакета
package_modules = modules(DIST_NAME)
# -> ['_pytest', '_pytest._argcomplete', ...]

# Получаем словарь с краткой информацией о пакете:
meta_dict = metadata(DIST_NAME)
# -> {'Name': 'pytest', ...}

# Получаем модули в указанном каталоге:
the_modules = modules_in_dir(".")
# -> ['x', 'x.y', 'x.y.z', ...]

# Получаем подмодули модуля (например, io.six - ищется в sys.path):
the_modules = modules_from("io.six")
# -> ['io.six.bar', 'io.six.bar.baz', ...]

# импортирует все указанные модули в текущий модуль (тут в examples.py)
# остальные параметры принимает те же, что и __import__
# imports(modules, globals=None, locals=None, fromlist=(), level=0)
# возвращает список результатов __import__
import_returns = imports(the_modules)

# Есть сокращение для imports( modules_from(module), *av, **kw ):
the_modules, import_returns = imports_from("io.six")
```

# DESCRIPTION

Позволяет получить модули установленного пакета, файлы и пути к каталогу с метаинформацией пакета, так и каталогу в котром стоит пакет.

Распознаются dist-info, egg-info и egg-link.

В дистрибутив входит одноимённая утилита:

```sh
Вывести список каталогов с модулями (sys.path):
$ dist -s
$ dist --syspath

Вывести все установленные дистрибутивы:
$ dist-info

Вывести сводную информацию о дистрибутиве:
$ dist-info <дистрибутив>

Вывести каталог в котором находятся модули пакета:
$ dist-info <дистрибутив> dist

Вывести путь к файлу или каталогу с метаинформацией:
$ dist-info <дистрибутив> egg

Вывести сокращённую метаинформацию:
$ dist-info <дистрибутив> meta

Вывести файлы:
$ dist-info <дистрибутив> files

Вывести модули:
$ dist-info [-c|--check] <дистрибутив> modules

Вывести модули по указанному пути:
$ dist-info [-c|--check] <каталог> mod

Вывести подмодули модуля (например, io.six - ищется в sys.path):
$ dist-info [-c|--check] <модуль> mods
```

# INSTALL

```sh
$ pip3 install dist-info
```

# REQUIREMENTS

* data-printer

# AUTHOR

Kosmina O. Yaroslav <darviarush@mail.ru>

# LICENSE

MIT License

Copyright (c) 2020 Kosmina O. Yaroslav

