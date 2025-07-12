"""
Logger Factory Module

This module provides a centralized logging configuration factory for the application.
It supports different log levels, formatters, and output destinations.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from enum import Enum


class LogLevel(Enum):
    """Enumeration for log levels"""

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LoggerFactory:
    """
    Factory class for creating and configuring loggers with consistent formatting
    and output destinations across the application.
    """

    _loggers: Dict[str, logging.Logger] = {}
    _default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    _detailed_format = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s"

    @classmethod
    def get_logger(
        cls,
        name: str,
        level: LogLevel = LogLevel.INFO,
        log_to_file: bool = True,
        log_to_console: bool = True,
        log_file_path: Optional[str] = None,
        detailed_format: bool = False,
        max_file_size_mb: int = 10,
        backup_count: int = 5,
    ) -> logging.Logger:
        """
        Get or create a logger with the specified configuration.

        Args:
            name: Logger name (typically module name)
            level: Logging level
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
            log_file_path: Custom log file path (optional)
            detailed_format: Use detailed format with file/line info
            max_file_size_mb: Maximum log file size in MB before rotation
            backup_count: Number of backup files to keep

        Returns:
            Configured logger instance
        """
        # Return existing logger if already configured
        if name in cls._loggers:
            return cls._loggers[name]

        # Create new logger
        logger = logging.getLogger(name)
        logger.setLevel(level.value)

        # Clear any existing handlers to avoid duplicates
        logger.handlers.clear()

        # Choose format
        formatter = logging.Formatter(
            cls._detailed_format if detailed_format else cls._default_format,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Add console handler if requested
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level.value)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Add file handler if requested
        if log_to_file:
            file_path = log_file_path or cls._get_default_log_file_path(name)

            # Ensure log directory exists
            log_dir = Path(file_path).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            # Use rotating file handler to manage log file size
            file_handler = logging.handlers.RotatingFileHandler(
                file_path,
                maxBytes=max_file_size_mb * 1024 * 1024,  # Convert MB to bytes
                backupCount=backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(level.value)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Prevent log messages from being handled by parent loggers
        logger.propagate = False

        # Cache the logger
        cls._loggers[name] = logger

        return logger

    @classmethod
    def _get_default_log_file_path(cls, logger_name: str) -> str:
        """
        Generate default log file path based on logger name.

        Args:
            logger_name: Name of the logger

        Returns:
            Default log file path
        """
        # Create logs directory in project root
        project_root = Path(__file__).parent.parent.parent.parent
        logs_dir = project_root / "logs"

        # Clean logger name for filename
        clean_name = logger_name.replace(".", "_").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d")

        return str(logs_dir / f"{clean_name}_{timestamp}.log")

    @classmethod
    def get_api_logger(cls, level: LogLevel = LogLevel.INFO) -> logging.Logger:
        """Get a logger specifically configured for API operations."""
        return cls.get_logger(
            name="api",
            level=level,
            detailed_format=True,
            log_to_file=True,
            log_to_console=True,
        )

    @classmethod
    def get_service_logger(cls, level: LogLevel = LogLevel.INFO) -> logging.Logger:
        """Get a logger specifically configured for service layer operations."""
        return cls.get_logger(
            name="service",
            level=level,
            detailed_format=True,
            log_to_file=True,
            log_to_console=True,
        )

    @classmethod
    def get_database_logger(cls, level: LogLevel = LogLevel.WARNING) -> logging.Logger:
        """Get a logger specifically configured for database operations."""
        return cls.get_logger(
            name="database",
            level=level,
            detailed_format=True,
            log_to_file=True,
            log_to_console=False,  # Database logs typically only to file
        )

    @classmethod
    def get_scraper_logger(cls, level: LogLevel = LogLevel.INFO) -> logging.Logger:
        """Get a logger specifically configured for web scraping operations."""
        return cls.get_logger(
            name="scraper",
            level=level,
            detailed_format=True,
            log_to_file=True,
            log_to_console=True,
        )

    @classmethod
    def configure_from_env(cls) -> Dict[str, Any]:
        """
        Configure logger settings from environment variables.

        Environment variables:
        - LOG_LEVEL: Default log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        - LOG_TO_FILE: Whether to log to file (true/false)
        - LOG_TO_CONSOLE: Whether to log to console (true/false)
        - LOG_FILE_PATH: Custom log file path
        - LOG_DETAILED_FORMAT: Use detailed format (true/false)

        Returns:
            Dictionary of configuration settings
        """
        config = {
            "level": LogLevel.INFO,
            "log_to_file": True,
            "log_to_console": True,
            "log_file_path": None,
            "detailed_format": False,
        }

        # Parse log level
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        try:
            config["level"] = LogLevel[log_level_str]
        except KeyError:
            config["level"] = LogLevel.INFO

        # Parse boolean settings
        config["log_to_file"] = os.getenv("LOG_TO_FILE", "true").lower() == "true"
        config["log_to_console"] = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
        config["detailed_format"] = (
            os.getenv("LOG_DETAILED_FORMAT", "false").lower() == "true"
        )

        # Custom log file path
        config["log_file_path"] = os.getenv("LOG_FILE_PATH")

        return config

    @classmethod
    def setup_application_logging(cls) -> None:
        """
        Set up application-wide logging configuration.
        This should be called once at application startup.
        """
        config = cls.configure_from_env()

        # Set up main loggers with environment configuration
        cls.get_logger("app", **config)
        cls.get_api_logger(config["level"])
        cls.get_service_logger(config["level"])

        # Log startup message
        app_logger = cls.get_logger("app")
        app_logger.info("Application logging configured successfully")
        app_logger.info(f"Log level: {config['level'].name}")
        app_logger.info(f"Log to file: {config['log_to_file']}")
        app_logger.info(f"Log to console: {config['log_to_console']}")

    @classmethod
    def log_performance(
        cls, logger: logging.Logger, operation: str, duration: float
    ) -> None:
        """
        Log performance metrics for operations.

        Args:
            logger: Logger instance to use
            operation: Name of the operation
            duration: Duration in seconds
        """
        if duration > 5.0:
            logger.warning(f"Slow operation detected: {operation} took {duration:.2f}s")
        elif duration > 1.0:
            logger.info(f"Operation completed: {operation} took {duration:.2f}s")
        else:
            logger.debug(f"Operation completed: {operation} took {duration:.3f}s")

    @classmethod
    def log_error_with_context(
        cls,
        logger: logging.Logger,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log an error with additional context information.

        Args:
            logger: Logger instance to use
            error: Exception that occurred
            context: Additional context information
        """
        context = context or {}

        error_msg = f"Error occurred: {type(error).__name__}: {str(error)}"

        if context:
            context_str = ", ".join([f"{k}={v}" for k, v in context.items()])
            error_msg += f" | Context: {context_str}"

        logger.error(error_msg, exc_info=True)


# Convenience functions for common use cases
def get_logger(name: str, level: LogLevel = LogLevel.INFO) -> logging.Logger:
    """Convenience function to get a logger with default settings."""
    return LoggerFactory.get_logger(name, level)


def get_api_logger() -> logging.Logger:
    """Convenience function to get the API logger."""
    return LoggerFactory.get_api_logger()


def get_service_logger() -> logging.Logger:
    """Convenience function to get the service logger."""
    return LoggerFactory.get_service_logger()


def setup_logging() -> None:
    """Convenience function to set up application logging."""
    LoggerFactory.setup_application_logging()
