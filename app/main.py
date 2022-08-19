from website import create_app
import logging
from config import *
app = create_app()
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    Config.init()
    app.logger.info("Website Started")
    app.run(host='0.0.0.0', port=80, debug=True)
