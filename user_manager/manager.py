"""
This module provides a Flask application for managing user access and balances.
It includes routes for viewing allowed users, allowing new users, disabling users,
and setting user balances. The application uses PostgreSQL for data storage and
includes logging for monitoring operations.
"""

import os
import logging

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from logfmter import Logfmter

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Enable logging
formatter = Logfmter(
    keys=["at", "logger", "level", "msg"],
    mapping={"at": "asctime", "logger": "name", "level": "levelname", "msg": "message"},
    datefmt='%H:%M:%S %d/%m/%Y'
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler("./logs/manager.log")
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[stream_handler, file_handler]
)

logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Establishes and returns a connection to the PostgreSQL database.
    Logs the process and handles any exceptions that occur.
    """
    try:
        logger.info("Establishing database connection.")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        return conn
    except Exception as e:
        logger.error("Error establishing database connection: %s", e)
        raise


@app.route('/')
def index():
    """
    Renders the index page with a list of allowed users.
    Fetches data from the database and handles any exceptions that occur.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT au.user_id, ub.balance, ub.images_generated AS images_generated
            FROM allowed_users au
            LEFT JOIN user_balances ub ON au.user_id = ub.user_id
            ORDER BY au.user_id
        """)
        allowed_users = cur.fetchall()
        logger.info("Fetched allowed users successfully.")
        return render_template('index.html', allowed_users=allowed_users)
    except Exception as e:
        logger.error("Error fetching allowed users: %s", e)
        flash("Could not load allowed users.", 'error')
        return render_template('index.html', allowed_users=[])
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()


@app.route('/allow', methods=['POST'])
def allow_user():
    """
    Allows a new user by adding their user_id to the allowed_users table.
    Handles any exceptions that occur and logs the process.
    """
    user_id = request.form.get('user_id')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if existing_user:
            flash("User %s is already allowed.", 'info')
            logger.info("User %s is already allowed.", user_id)
        else:
            cur.execute("INSERT INTO allowed_users (user_id) VALUES (%s)", (user_id,))
            conn.commit()
            flash("User %s has been allowed.", 'success')
            logger.info("User %s has been successfully allowed.", user_id)
    except Exception as e:
        logger.error("Error allowing user %s: %s", user_id, e)
        flash("Error allowing user %s.", 'error')
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()
    return redirect(url_for('index'))


@app.route('/disable', methods=['POST'])
def disable_user():
    """
    Disables a user by removing their user_id from the allowed_users table.
    Handles any exceptions that occur and logs the process.
    """
    user_id = request.form.get('user_id')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            flash("User %s is not currently allowed.", 'info')
            logger.info("User %s is not currently allowed.", user_id)
        else:
            cur.execute("DELETE FROM allowed_users WHERE user_id = %s", (user_id,))
            conn.commit()
            flash("User %s access revoked.", 'warning')
            logger.info("User %s access revoked.", user_id)
    except Exception as e:
        logger.error("Error disabling user %s: %s", user_id, e)
        flash("Error disabling user %s.", 'error')
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()
    return redirect(url_for('index'))


@app.route('/set_balance', methods=['POST'])
def set_balance():
    """
    Sets the balance for a user in the user_balances table.
    Handles any exceptions that occur and logs the process.
    """
    user_id = request.form.get('user_id')
    balance = request.form.get('balance')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT user_id FROM allowed_users WHERE user_id = %s", (user_id,))
        existing_user = cur.fetchone()
        if not existing_user:
            flash("User %s is not currently allowed.", 'info')
            logger.info("User %s is not currently allowed when setting balance.", user_id)
        else:
            cur.execute(
                """
                INSERT INTO user_balances (user_id, balance, images_generated)
                VALUES (%s, %s, 0)
                ON CONFLICT (user_id)
                DO UPDATE SET balance = EXCLUDED.balance
                """,
                (user_id, balance)
            )
            conn.commit()
            flash("User %s balance has been set to %s.", 'success')
            logger.info("User %s balance set to %s.", user_id, balance)
    except Exception as e:
        logger.error("Error setting balance for user %s: %s", user_id, e)
        flash("Error setting balance for user %s.", 'error')
    finally:
        logger.info("Closing database connection.")
        cur.close()
        conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
