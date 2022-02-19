Backend for [Reboot Investing](https://rebootinvesting.com/)
===========

This project is intended to provide stock history data gained yahoo finance.


Installation
------------

First of all, make sure you have [docker](https://docs.docker.com/compose/install/) and [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed on your computer.

1. The easies way is to use the docker-compose. Go to the top folder containing docker-compose.yml and use the following command in terminal.
    ```sh
    docker-compose up -d --build
    ```
    Or you can use the following one if you have installed [Typer](https://typer.tiangolo.com/#fastapi-of-clis).
    ```sh
    python main.py start-back
    ```

2. If you are familiar with python you can take another approach on backend folder.
    ```sh
    pip install --upgrade pip
    pip install -r requirements.txt

    python app/main.py
    ```