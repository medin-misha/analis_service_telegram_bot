FROM python:3.12.6

LABEL admin="https://github.com/medin-misha"

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY bot /bot

# сюда подставить токен бота (без кавычек) и url сервера (без слеша)
ENV token token
ENV server http://

WORKDIR /bot
CMD ["python", "main.py"]
