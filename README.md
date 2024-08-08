# chatgpt_telegram_bot

### SQL list allowed users
```sql
SELECT * FROM allowed_users;
```

### SQL allow user
```sql
INSERT INTO allowed_users (user_id) VALUES (105013941);
```

### SQL remove user
```sql
DELETE FROM allowed_users WHERE user_id = 105013941;
```

### SQL balance change
```sql
insert into user_balances (user_id, balance, images_generated) VALUES (105013941, 100.0, 0)
```

### Bash example
```bash
psql -U $POSTGRES_USER \
-d $POSTGRES_DB \
-c "INSERT INTO allowed_users (user_id) VALUES (105013941);"
```
