"""Tests for font management and registration."""

from unittest.mock import patch

from src.pdf_generation.fonts import (
    register_fonts,
    get_font_name,
    is_font_available,
)


class TestFontManagement:
    """Tests for font registration and fallback logic."""

    @patch("src.pdf_generation.fonts.pdfmetrics.registerFont")
    @patch("src.pdf_generation.fonts.TTFont")
    def test_register_fonts_success(self, mock_ttfont, mock_register, tmp_path):
        """register_fonts should attempt to register .ttf files in the directory."""
        # Create a dummy ttf file
        font_file = tmp_path / "TestFont.ttf"
        font_file.write_text("dummy")

        registered = register_fonts(tmp_path)

        assert "TestFont" in registered
        mock_register.assert_called_once()
        mock_ttfont.assert_called_once_with("TestFont", str(font_file))

    def test_get_font_name_builtin(self):
        """get_font_name should return a builtin font if preferred."""
        font = get_font_name("Helvetica")
        assert font == "Helvetica"

    def test_get_font_name_fallback(self):
        """get_font_name should return fallback if preferred is missing."""
        # Force a reload/check for a non-existent font
        with patch("src.pdf_generation.fonts.register_fonts") as mock_reg:
            font = get_font_name("NonExistentFont", fallback="Times-Bold")
            assert font == "Times-Bold"
            mock_reg.assert_called()

    def test_get_font_name_ultimate_fallback(self):
        """get_font_name should return Helvetica as ultimate fallback."""
        with patch("src.pdf_generation.fonts.register_fonts"):
            font = get_font_name("Missing1", fallback="Missing2")
            assert font == "Helvetica"

    def test_is_font_available_builtin(self):
        """is_font_available should return True for builtin fonts."""
        assert is_font_available("Courier") is True

    def test_is_font_available_unknown(self):
        """Check that unknown fonts return False after registration attempt."""
        with patch("src.pdf_generation.fonts.register_fonts") as mock_reg:
            assert is_font_available("GhostFont") is False
            mock_reg.assert_called()
