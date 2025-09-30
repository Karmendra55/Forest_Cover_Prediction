class AppError(Exception):
    """Base class for all app-specific errors."""
    pass

class ThemeError(AppError):
    """Raised when theme application fails."""
    pass

class VisualizationError(AppError):
    """Raised when a visualization cannot be rendered."""
    pass

class PDFError(AppError):
    """Raised for PDF generation issues."""
    pass

class VoiceError(AppError):
    """Raised for voice processing issues."""
    pass
