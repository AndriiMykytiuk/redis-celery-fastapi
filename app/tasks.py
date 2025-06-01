from celery import Celery
from dotenv import load_dotenv
import os
import random
import string

load_dotenv()

redis_url = os.getenv("REDIS_URL")

celery_app = Celery('worker')

celery_app.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    broker_use_ssl={'ssl_cert_reqs': 'none'},
    redis_backend_use_ssl={'ssl_cert_reqs': 'none'}
)

# Лічильник виконань (глобальна змінна, лише для демонстрації — не для продакшену)
run_counter = {"count": 0}

@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,  # експоненційна затримка: 1s, 2s, 4s, ...
    retry_kwargs={'max_retries': 3}
)
def greet(self):
    run_counter["count"] += 1
    name = ''.join(random.choices(string.ascii_letters, k=6))
    print(f"👋 Hello, {name}")
    import time
    time.sleep(2)

    # Логування інформації про retry
    if self.request.retries > 0:
        print(f"🔁 Retry attempt {self.request.retries} for {name}")

    # Імітація помилки кожного 5-го запуску
    if run_counter["count"] % 5 == 0:
        print("💥 Simulated failure!")
        raise Exception("Simulated task failure!")

    print(f"✅ Done greeting {name}")
    return f"Hello {name}!"

