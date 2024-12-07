FROM python:3.10-slim

RUN groupadd -r bot_group && useradd -r -g bot_group bot_user

WORKDIR /app

COPY src/ /app/

COPY src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "rezy{discord_bot_hacked}" > /flag.txt

RUN chown -R bot_user:bot_group /app /flag.txt

USER bot_user

CMD ["python", "bot.py"]
