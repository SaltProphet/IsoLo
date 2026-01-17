"""
Base Agent Class

Provides common functionality for all sample pack generator agents.
All specialized agents inherit from this base class to ensure consistent
interfaces and shared utilities.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import logging


class BaseAgent(ABC):
    """
    Base class for all sample pack generator agents.
    
    Provides common functionality for logging, error handling, file management,
    and configuration. All agents must inherit from this class and implement
    the process() method.
    
    Attributes:
        config: Configuration dictionary for the agent
        logger: Logger instance for this agent
        name: Human-readable name of the agent
        version: Agent version number
    
    Example:
        >>> class MyAgent(BaseAgent):
        ...     def process(self, input_data):
        ...         self.log_info("Processing started")
        ...         return {"status": "success"}
        ...
        >>> agent = MyAgent(config={"option": "value"})
        >>> result = agent.process({"input": "data"})
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the agent with optional configuration.
        
        Args:
            config: Optional configuration dictionary containing agent-specific
                   settings. Each agent may define its own config schema.
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """
        Set up logging for the agent.
        
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(self.name)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main processing method - must be implemented by subclasses.
        
        This is the core method that each agent must implement. It receives
        input data, performs its specific processing tasks, and returns
        output data.
        
        Args:
            input_data: Dictionary containing input parameters and data.
                       The schema varies by agent type.
            
        Returns:
            Dictionary containing output data, metadata, and status information.
            Should include at minimum:
            - status: "success" or "error"
            - message: Description of the result
            - data: The actual output data (paths, arrays, etc.)
            
        Raises:
            NotImplementedError: If subclass doesn't implement this method
        """
        raise NotImplementedError(f"{self.name} must implement process() method")
    
    def validate_input(self, input_data: Dict[str, Any], required_keys: List[str]) -> bool:
        """
        Validate that input data contains all required keys.
        
        Args:
            input_data: Dictionary to validate
            required_keys: List of keys that must be present
            
        Returns:
            True if all required keys are present, False otherwise
        """
        missing_keys = [key for key in required_keys if key not in input_data]
        if missing_keys:
            self.log_error(f"Missing required input keys: {missing_keys}")
            return False
        return True
    
    def log_info(self, message: str) -> None:
        """
        Log an informational message.
        
        Args:
            message: Message to log
        """
        self.logger.info(message)
    
    def log_warning(self, message: str) -> None:
        """
        Log a warning message.
        
        Args:
            message: Warning message to log
        """
        self.logger.warning(message)
    
    def log_error(self, message: str) -> None:
        """
        Log an error message.
        
        Args:
            message: Error message to log
        """
        self.logger.error(message)
    
    def log_debug(self, message: str) -> None:
        """
        Log a debug message.
        
        Args:
            message: Debug message to log
        """
        self.logger.debug(message)
    
    def ensure_output_dir(self, output_path: str) -> Path:
        """
        Ensure that an output directory exists, creating it if necessary.
        
        Args:
            output_path: Path to the output directory
            
        Returns:
            Path object for the directory
        """
        path = Path(output_path)
        path.mkdir(parents=True, exist_ok=True)
        self.log_debug(f"Ensured output directory exists: {path}")
        return path
    
    def get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.
        
        Returns:
            ISO formatted timestamp string
        """
        return datetime.utcnow().isoformat() + "Z"
    
    def create_success_response(
        self,
        data: Any,
        message: str = "Processing completed successfully"
    ) -> Dict[str, Any]:
        """
        Create a standardized success response.
        
        Args:
            data: The output data to include in the response
            message: Success message
            
        Returns:
            Standardized success response dictionary
        """
        return {
            "status": "success",
            "message": message,
            "data": data,
            "agent": self.name,
            "version": self.version,
            "timestamp": self.get_timestamp()
        }
    
    def create_error_response(
        self,
        error: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            error: Error message
            details: Optional additional error details
            
        Returns:
            Standardized error response dictionary
        """
        return {
            "status": "error",
            "message": error,
            "details": details or {},
            "agent": self.name,
            "version": self.version,
            "timestamp": self.get_timestamp()
        }
    
    def get_config_value(
        self,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get a configuration value with optional default.
        
        Args:
            key: Configuration key to retrieve
            default: Default value if key is not found
            
        Returns:
            Configuration value or default
        """
        return self.config.get(key, default)
