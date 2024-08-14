# ChatGPT Telegram Bot

## Pre-requisites

### Docker and Docker Compose

Please make sure you have Docker and Docker Compose installed on your machine.

Consider [Docker Desktop](https://www.docker.com/products/docker-desktop/) for Windows, macOS or Ubuntu.

This software is free and contains all the necessary tools built-in.

Required versions:
- Docker 27.0.0 or later
- Docker Compose 2.28.0 or later

### OpenAI (ChatGPT) API Key

In order to use this bot, you need to have an OpenAI API key. 

Pre-generated list of API keys was sent via Telegram Group with Yandex Workshop team.

### Telegram Bot Token

You need to create a Telegram bot and get the token.

This is completely free of charge, and you can do it by talking to the [BotFather](https://core.telegram.org/bots/features#creating-a-new-bot).

## Configuration

### Put `.env` files in place

```bash
cp env_example .env
cp grafana/env_example grafana/.env
cp telegram_bot/env_example telegram_bot/.env
cp user_manager/env_example user_manager/.env
```

### Fill you OpenAI API key and Telegram Bot Token

Please edit `telegram_bot/.env` file and put your values for 
- OPENAI_API_KEY 
- TELEGRAM_BOT_TOKEN

[!TIP]
>  You don't have to change any other ENVs, but you are welcome to do this as well.

### Launch the bot
```bash
docker compose up -d
```

### Verify the bot is running

First of all, just try to send a text message to your bot in Telegram.

You will get a message
> "Sorry, you are not allowed to text with me."

**It's OK.**

> [!NOTE]  
> You can check the status of the running containers with the following command:
> ```bash
> docker compose ps -a
> ```

### Allow Bot to chat with you
1. Find you Telegram ID using the following command:
    ```bash
    docker compose logs telegram-bot
    ```
    
    For example log line like this
    > logger=__main__ level=INFO msg="User 105013941 (mossad_zika) requested sent text: 'hello'"
    
    means for user `mossad_zika` Telegram ID is `105013941`.

2. Navigate to User Manager App as [http://localhost:5005/](http://localhost:5005/)

3. Put the ID into the form and press "Allow User" button.

### Tear Down

If you want to completely remove the bot from your machine, you can use the following command:

```bash
docker compose down -v
```

## What's next?
- [Project Motivation](documentation/project-motivation.md)
- [Infrastructure components](documentation/infrastructure-components.md)
- [Telegram Bot Features](documentation/telegram-bot-features.md)
- [User Manager Features](documentation/user-manager-features.md)
- [Testing Notes](documentation/testing-notes.md)
