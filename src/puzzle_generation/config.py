"""Configuration management for puzzle generation."""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class PuzzleConfig:
    """Configuration for puzzle generation."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to YAML config file. If None, uses default.
        """
        if config_path is None:
            # Default to config/default_config.yaml
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "default_config.yaml"

        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., 'puzzle.default_grid_size.width')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def default_width(self) -> int:
        """Get default grid width."""
        return self.get("puzzle.default_grid_size.width", 9)

    @property
    def default_height(self) -> int:
        """Get default grid height."""
        return self.get("puzzle.default_grid_size.height", 9)

    @property
    def default_black_density(self) -> float:
        """Get default black cell density."""
        return self.get("puzzle.black_density.default", 0.22)

    @property
    def min_black_density(self) -> float:
        """Get minimum black cell density."""
        return self.get("puzzle.black_density.min", 0.1)

    @property
    def max_black_density(self) -> float:
        """Get maximum black cell density."""
        return self.get("puzzle.black_density.max", 0.4)

    @property
    def min_grid_size(self) -> int:
        """Get minimum grid size."""
        return self.get("puzzle.size_constraints.min_width", 5)

    @property
    def max_grid_size(self) -> int:
        """Get maximum grid size."""
        return self.get("puzzle.size_constraints.max_width", 15)

    @property
    def max_generation_attempts(self) -> int:
        """Get maximum generation attempts."""
        return self.get("puzzle.generator.max_attempts", 10)

    @property
    def solver_randomize(self) -> bool:
        """Get solver randomization setting."""
        return self.get("puzzle.solver.randomize", True)

    def get_difficulty_config(self, difficulty: str) -> Dict[str, Any]:
        """
        Get configuration for a specific difficulty level.

        Args:
            difficulty: Difficulty level (beginner, intermediate, expert, master)

        Returns:
            Dictionary with difficulty configuration

        Raises:
            ValueError: If difficulty level not found
        """
        config = self.get(f"difficulty.{difficulty}")
        if config is None:
            raise ValueError(
                f"Unknown difficulty level: {difficulty}. "
                f"Available: beginner, intermediate, expert, master"
            )
        return config


# Global configuration instance
_global_config: Optional[PuzzleConfig] = None


def get_config(config_path: Optional[str] = None) -> PuzzleConfig:
    """
    Get global configuration instance.

    Args:
        config_path: Path to config file. If None, uses default.

    Returns:
        PuzzleConfig instance
    """
    global _global_config

    if _global_config is None or config_path is not None:
        _global_config = PuzzleConfig(config_path)

    return _global_config
