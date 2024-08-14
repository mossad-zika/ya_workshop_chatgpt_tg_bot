# Telegram Bot Features

- On `/start` command greet the User and suggest sending back your text reply
- On `/image description` command in personal chat generate an image with content which matches description from the User (Also Works in Group Chats)
- On any text message in personal chat generate a message via ChatGPT
- In group chat if the bot has ("access to messages")[https://core.telegram.org/bots/features#privacy-mode] permission] it will reply to messages which start with `@comrade_danilevich_gpt_bot`
- On images generation, Bot also must "consume" a virtual user balancer, texts are free of charge
- If the user did "edit" the previous message or `/image description` command, ignore it
