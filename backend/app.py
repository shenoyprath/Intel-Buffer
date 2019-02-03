import logging
import sys

if sys.version_info >= (3, 7):
    from api import app
else:
    raise RuntimeError("Python version >= 3.7 is required.")


def backend_log():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%d-%m-%Y:%H:%M:%S")
    logging.info("------------------------------------------------------------")
    logging.info("··········· (Re)Starting Backend Server Instance ···········")
    logging.info("------------------------------------------------------------")


if __name__ == "__main__":
    backend_log()
    app.run(host="0.0.0.0", port=8888, debug=True)
