import logging
import redis
from flask import Flask, request, jsonify
from src.Utils import clear_ns
from src.TokenBucket import TokenBucket
from src.FixedWindow import FixedWindow
from src.Response import Response
from src.SlidingWindow import SlidingWindow
from src.Config import get_free_plan_requests
from src.Config import get_free_plan_window
from src.Config import get_pro_plan_requests
from src.Config import get_pro_plan_window
from src.Config import get_enterprise_plan_requests
from src.Config import get_enterprise_plan_window

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
fixed_window = FixedWindow("FREE:user", get_free_plan_requests(), get_free_plan_window())
token_buket = TokenBucket("ENTERPRISE:user", get_enterprise_plan_requests(), get_enterprise_plan_window())
sliding_window = SlidingWindow("PRO:user", get_pro_plan_requests(), get_pro_plan_window())


@app.route('/jokes/chuck_norris')
def execute():
    app_id = request.headers.get('X-App-Id')

    if "PRO" in app_id:
        app.logger.info("PRO type")
        # key: str, max_requests: int, tokens_per_second: int, expire: int
        return pass_or_abort(token_buket.rate_limit(), app_id)

    elif "ENTERPRISE" in app_id:
        app.logger.info("Enterprise type")
        return pass_or_abort(sliding_window.rate_limit(), app_id)
    else:
        app.logger.info("Free type")
        return pass_or_abort(fixed_window.rate_limit(), app_id)


def pass_or_abort(response: Response, app_id: str):
    if response.allowed :
        return jsonify(response)
    return jsonify(error=str(f"Too many requests for {app_id}")), 429


if __name__ == '__main__':
    app.run()
