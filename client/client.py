from client.example import func

import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def main():
    out = func(2).run()
    assert out == 4
    logger.info("SUCCESS!")


if __name__ == '__main__':
    main()
