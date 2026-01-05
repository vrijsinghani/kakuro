"""Tests for configuration module."""

import pytest
from pathlib import Path
from src.puzzle_generation.config import PuzzleConfig, get_config


class TestPuzzleConfig:
    """Tests for PuzzleConfig class."""

    def test_load_default_config(self):
        """Test loading default configuration."""
        config = PuzzleConfig()
        assert config.default_width == 9
        assert config.default_height == 9

    def test_default_black_density(self):
        """Test default black density."""
        config = PuzzleConfig()
        assert config.default_black_density == 0.22

    def test_black_density_constraints(self):
        """Test black density min/max constraints."""
        config = PuzzleConfig()
        assert config.min_black_density == 0.1
        assert config.max_black_density == 0.4

    def test_grid_size_constraints(self):
        """Test grid size constraints."""
        config = PuzzleConfig()
        assert config.min_grid_size == 5
        assert config.max_grid_size == 15

    def test_max_generation_attempts(self):
        """Test max generation attempts."""
        config = PuzzleConfig()
        assert config.max_generation_attempts == 10

    def test_solver_randomize(self):
        """Test solver randomization setting."""
        config = PuzzleConfig()
        assert config.solver_randomize is True

    def test_get_with_dot_notation(self):
        """Test getting values with dot notation."""
        config = PuzzleConfig()
        width = config.get("puzzle.default_grid_size.width")
        assert width == 9

    def test_get_with_default(self):
        """Test getting non-existent key with default."""
        config = PuzzleConfig()
        value = config.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_get_difficulty_config_beginner(self):
        """Test getting beginner difficulty config."""
        config = PuzzleConfig()
        beginner = config.get_difficulty_config("beginner")
        assert beginner["grid_size"]["width"] == 7
        assert beginner["grid_size"]["height"] == 7
        assert beginner["black_density"] == 0.30

    def test_get_difficulty_config_intermediate(self):
        """Test getting intermediate difficulty config."""
        config = PuzzleConfig()
        intermediate = config.get_difficulty_config("intermediate")
        assert intermediate["grid_size"]["width"] == 9
        assert intermediate["grid_size"]["height"] == 9
        assert intermediate["black_density"] == 0.22

    def test_get_difficulty_config_expert(self):
        """Test getting expert difficulty config."""
        config = PuzzleConfig()
        expert = config.get_difficulty_config("expert")
        assert expert["grid_size"]["width"] == 12
        assert expert["grid_size"]["height"] == 12
        assert expert["black_density"] == 0.15

    def test_get_difficulty_config_master(self):
        """Test getting master difficulty config."""
        config = PuzzleConfig()
        master = config.get_difficulty_config("master")
        assert master["grid_size"]["width"] == 15
        assert master["grid_size"]["height"] == 15
        assert master["black_density"] == 0.12

    def test_get_difficulty_config_invalid(self):
        """Test getting invalid difficulty raises error."""
        config = PuzzleConfig()
        with pytest.raises(ValueError, match="Unknown difficulty level"):
            config.get_difficulty_config("invalid")

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            PuzzleConfig("/nonexistent/path/config.yaml")


class TestGetConfig:
    """Tests for get_config function."""

    def test_get_config_singleton(self):
        """Test that get_config returns singleton instance."""
        config2 = get_config()
        assert config2 is not None

    def test_get_config_with_path(self):
        """Test that providing path creates new instance."""
        # Get default config path
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "config" / "default_config.yaml"
        config2 = get_config(str(config_path))
        # Should be a valid config instance
        assert config2 is not None
        assert config2.default_width == 9
