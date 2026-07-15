"""Application-specific exceptions."""


class FileSystemAnalysisError(Exception):
    """Base exception for the application."""


class ConfigurationError(FileSystemAnalysisError):
    """Raised when configuration is invalid or cannot be loaded."""


class FileReadError(FileSystemAnalysisError):
    """Raised when a supported document cannot be read."""
