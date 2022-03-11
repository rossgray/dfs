import logging

from client.functions import func

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    """Run a distributed function"""
    out = func(2).run()
    assert out == 4
    logger.info("SUCCESS!")


if __name__ == '__main__':
    main()
