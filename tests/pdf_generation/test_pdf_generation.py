"""Tests for the PDF generation module."""

from src.pdf_generation import (
    PageLayout,
    Margins,
    BookConfig,
    PDFDocument,
    create_puzzle_book,
    LETTER,
    POINTS_PER_INCH,
)


class TestModels:
    """Tests for PDF generation data models."""

    def test_letter_page_size(self):
        """LETTER should be 8.5 x 11 inches in points."""
        assert LETTER.width == 8.5 * POINTS_PER_INCH
        assert LETTER.height == 11 * POINTS_PER_INCH

    def test_margins_from_inches(self):
        """Margins.from_inches should convert correctly."""
        margins = Margins.from_inches(top=1.0, bottom=0.5, left=0.75, right=0.75)
        assert margins.top == 72.0
        assert margins.bottom == 36.0
        assert margins.left == 54.0
        assert margins.right == 54.0

    def test_default_page_layout(self):
        """Default PageLayout should have sensible defaults."""
        layout = PageLayout()
        assert layout.page_size == LETTER
        assert layout.puzzles_per_page == 2
        assert layout.render_config.cell_size > 0

    def test_large_print_layout(self):
        """Large print layout should have 1 puzzle per page."""
        layout = PageLayout.large_print()
        assert layout.puzzles_per_page == 1
        assert layout.render_config.cell_size > PageLayout().render_config.cell_size

    def test_content_dimensions(self):
        """content_width and content_height should account for margins."""
        layout = PageLayout()
        expected_width = LETTER.width - layout.margins.left - layout.margins.right
        expected_height = LETTER.height - layout.margins.top - layout.margins.bottom
        assert layout.content_width == expected_width
        assert layout.content_height == expected_height


class TestPDFDocument:
    """Tests for PDFDocument class."""

    def test_create_empty_document(self, tmp_path):
        """Creating an empty document should work."""
        output = tmp_path / "empty.pdf"
        doc = PDFDocument(output)
        result = doc.save()
        assert result.exists()

    def test_create_document_with_puzzles(self, tmp_path, sample_puzzles):
        """Creating a document with puzzles should work."""
        output = tmp_path / "puzzles.pdf"
        doc = PDFDocument(output)
        doc.add_puzzles(sample_puzzles)
        result = doc.save()
        assert result.exists()
        assert result.stat().st_size > 0

    def test_add_single_puzzle(self, tmp_path, sample_puzzle):
        """Adding a single puzzle should work."""
        output = tmp_path / "single.pdf"
        doc = PDFDocument(output)
        doc.add_puzzle(sample_puzzle)
        result = doc.save()
        assert result.exists()

    def test_document_with_solutions(self, tmp_path, sample_puzzles):
        """Document with solutions section should include more pages."""
        output = tmp_path / "with_solutions.pdf"
        config = BookConfig(include_solutions=True)
        doc = PDFDocument(output, config)
        doc.add_puzzles(sample_puzzles)
        result = doc.save()
        assert result.exists()

    def test_document_metadata(self, tmp_path):
        """Document should set title and author metadata."""
        output = tmp_path / "metadata.pdf"
        config = BookConfig(title="Test Title", author="Test Author")
        doc = PDFDocument(output, config)
        result = doc.save()
        assert result.exists()


class TestCreatePuzzleBook:
    """Tests for the create_puzzle_book convenience function."""

    def test_create_puzzle_book(self, tmp_path, sample_puzzles):
        """create_puzzle_book should generate a valid PDF."""
        output = tmp_path / "book.pdf"
        result = create_puzzle_book(sample_puzzles, output)
        assert result.exists()
        assert result.stat().st_size > 0

    def test_create_puzzle_book_with_config(self, tmp_path, sample_puzzles):
        """create_puzzle_book should accept custom config."""
        output = tmp_path / "custom_book.pdf"
        config = BookConfig(
            title="My Kakuro Book",
            author="Test Author",
            layout=PageLayout.large_print(),
        )
        result = create_puzzle_book(sample_puzzles, output, config)
        assert result.exists()


class TestIntegration:
    """Integration tests for end-to-end PDF generation."""

    def test_full_book_generation(self, tmp_path, sample_puzzles):
        """Generate a complete book with all features."""
        output = tmp_path / "full_book.pdf"
        config = BookConfig(
            title="Kakuro Puzzle Book - Beginner",
            author="Test Author",
            include_solutions=True,
        )
        result = create_puzzle_book(sample_puzzles, output, config)

        # Verify file was created
        assert result.exists()
        assert result.stat().st_size > 1000  # Should be at least 1KB

        # Verify it's a valid PDF (starts with PDF header)
        with open(result, "rb") as f:
            header = f.read(8)
            assert header.startswith(b"%PDF-")
