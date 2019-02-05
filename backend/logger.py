import logging


def logger():
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                        datefmt="%d-%m-%Y:%H:%M:%S")
    logging.info("------------------------------------------------------------")
    logging.info("··········· (Re)Starting Backend Server Instance ···········")
    logging.info("------------------------------------------------------------")
