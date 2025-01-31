import logging
import redis
from flask import Flask, request
from Utils import clear_ns
from TokenBucket import TokenBucket
from FixedWindow import FixedWindow
from Response import Response
from SlidingWindow import SlidingWindow

# the Flask application object creation has to be in the __init__.py file. That way each module can import it safely
# and the __name__ variable will resolve to the correct package.

app = Flask(__name__)

# Configure Flask logging
app.logger.setLevel(logging.INFO)  # Set log level to INFO
handler = logging.FileHandler('app.log')  # Log to a file
app.logger.addHandler(handler)

# adding Folder_2/subfolder to the system path


# Configure Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
clear_ns(redis_client)

#### Plans
fixed_window = FixedWindow("FREE:user", 50, 86400)
token_buket = TokenBucket("PRO:user", max_requests=12000, tokens_per_second=10, expire=86400)
sliding_window = SlidingWindow("ENTERPRISE:user", 5, 300)


@app.route('/jokes/chuck_norris')
def execute():
    app_id = request.headers.get('X-App-Id')

    if "PRO" in app_id:
        app.logger.info("PRO type")
        # key: str, max_requests: int, tokens_per_second: int, expire: int
        return str(token_buket.rate_limit())

    elif "ENTERPRISE" in app_id:
        app.logger.info("Enterprise type")
        return str(sliding_window.rate_limit())
    else:
        app.logger.info("Free type")
        return str(fixed_window.rate_limit())

    return f"X-App-Id: {app_id}"


if __name__ == '__main__':
    app.run()
