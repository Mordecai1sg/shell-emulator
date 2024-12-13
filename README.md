****************************************************
# README
****************************************************

## Описание проекта

Этот проект представляет собой эмулятор командной строки, 
который имитирует работу операционной системы. Эмулятор работает с виртуальной файловой
системой и предоставляет базовые команды, такие как `ls`, `cd`, `touch`, `rmdir`, и `rev`.
Проект предназначен для работы с `config.csv` конфигурационным файлом, содержащим параметры пути к 
виртуальной файловой системе и файлу журнала.

## Установка и использование
в config.csv пропишите:

username,fs_path,log_path
your_username,virtual_fs.tar.gz,log.xml

**Функционал:**
ls – выводит список файлов и директорий текущей директории.
cd – переходит в указанную директорию.
touch – создает пустой файл в текущей директории.
rmdir – удаляет указанную пустую директорию.
rev – отображает содержимое файла в обратном порядке.

**Пример работы:**

Gordey:/$ ls



virtual_fs



Gordey:/$ touch help



File 'help' created.Gordey:/$ ls



virtual_fs



help

Gordey:/$ cd virtual_fs
Gordey:/virtual_fs$ ls



home



movies

Gordey:/virtual_fs$ rmdir movies



Directory 'movies' removed.

Gordey:/virtual_fs$ exit



Process finished with exit code 0
