# gunicorn_config.py

# You can customize this to suit your server's CPU/memory
workers = 1  # Since Telegram bots are not web-based apps, 1 worker is enough
worker_class = 'gthread'  # Use thread-based workers
threads = 2  # This number depends on how concurrent your bot operations are

timeout = 120  # Adjust the timeout as needed
