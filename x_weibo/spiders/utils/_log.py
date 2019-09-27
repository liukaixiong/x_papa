import logging


class LOG:

    logging.basicConfig(level=logging.NOTSET,
                        format="%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    def __init__(self, name):
        logging.getLogger(name)

    def info(self, text, *args):
        logging.info(text, *args)

    def debug(self, text, *args, **kwargs):
        logging.debug(text, *args, **kwargs)

    def error(self, text, *args, **kwargs):
        logging.error(text, *args, **kwargs)


if __name__ == '__main__':
    log = LOG("bbbb")
    log.info("aaa -%s", "b")
    # logging.info("aaaa - %s","a")
