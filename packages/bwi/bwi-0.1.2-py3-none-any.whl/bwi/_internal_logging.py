import logging


class BwiLogger:
    """
    Used for bwi logging, used by BWI developpers to debug the workers or
    library
    """

    class __BwiLogger:
        """
        Singleton to have only one connection per vhost for a worker
        """
        logger = None

        def __init__(self):
            self.logger = logging.getLogger('bwi_lib')
            self.logger.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    instance = None

    def __init__(self):
        if not BwiLogger.instance:
            BwiLogger.instance = BwiLogger.__BwiLogger()

    def __getattr__(self, name):
        return getattr(self.instance, name)
