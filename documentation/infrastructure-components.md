# Current Infrastructure Components

1. [Telegram Bot](./telegram-bot-features.md)
2. [User Manager](./user-manager-features.md)
3. Grafana (Logs Dashboard) accessible as [http://localhost:3000/d/...](http://localhost:3000/d/f4df65a2-4129-4f66-b955-e2f9a1a2578f/telegram-bot-and-user-manager-logs?orgId=1)
   - Login: `admin`
   - Password: value from `grafana/.env`
4. Loki (Logs Storage) as Grafana Data Source
5. Promtail (Sends logs to Loki)
6. Liquibase (Database Migrations)
7. PostgreSQL (Database)
