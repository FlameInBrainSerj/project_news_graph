import logging
import logging.handlers


class LoggerSetup:
    """
    Logging setup.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("")
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self.log_file = "logs/fastapi-efk.log"
        self.backup_count = 5

        self.setup_logging()

    def setup_logging(self) -> None:
        logging.basicConfig(level=logging.INFO, format=self.log_format)

        formatter = logging.Formatter(self.log_format)

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        file = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_file,
            when="midnight",
            backupCount=self.backup_count,
        )
        file.setFormatter(formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(file)
