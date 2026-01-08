# Diagram Renderer Design

## Context

The current diagram pipeline uses HTML → Playwright browser → PDF screenshot → pdf2svg conversion. This approach has fundamental problems:
- Bounding box calculations cause inconsistent whitespace
- Multiple conversion steps degrade quality
- External dependencies (Playwright, pdf2svg) are fragile
- Diagrams get scaled down when they're too tall, making text unreadable

Since we already use ReportLab for puzzle grid rendering, we should use the same approach for instructional diagrams.

## Goals / Non-Goals

**Goals:**
- Generate all instructional diagrams programmatically with ReportLab
- True vector output that scales perfectly
- Consistent sizing and styling across all diagrams
- No external dependencies beyond ReportLab
- Diagrams defined as data structures (easy to modify)

**Non-Goals:**
- Complex illustration capabilities (photos, gradients, etc.)
- Real-time diagram editing UI
- Supporting arbitrary diagram types (only Kakuro-specific)

## Decisions

### Decision 1: ReportLab Drawing API

Use ReportLab's `reportlab.graphics.shapes` module:
- `Drawing` as the container
- `Rect`, `Line`, `String` for primitives
- `Group` for composing elements
- Returns a Flowable for document integration

**Why:** Already a project dependency, proven for puzzle rendering, true PDF vector output.

### Decision 2: Diagram Definition as Python Dataclasses

Define diagrams using Python dataclasses:

```python
@dataclass
class DiagramCell:
    row: int
    col: int
    value: Optional[str] = None
    is_black: bool = False
    clue_across: Optional[int] = None
    clue_down: Optional[int] = None
    highlight: Optional[str] = None  # Color name or hex

@dataclass  
class DiagramGrid:
    rows: int
    cols: int
    cells: List[DiagramCell]
    title: Optional[str] = None
    caption: Optional[str] = None

@dataclass
class Annotation:
    text: str
    position: str  # 'below', 'right', 'callout'
    style: str = 'default'  # 'info', 'warning', 'error'

@dataclass
class DiagramDefinition:
    title: str
    grids: List[DiagramGrid]  # Support multiple grids (side-by-side)
    annotations: List[Annotation] = field(default_factory=list)
    legend: Optional[Dict[str, str]] = None  # color -> label mapping
    layout: str = 'horizontal'  # 'horizontal', 'vertical', 'single'
```

**Why:** Type-safe, self-documenting, easy to version control, IDE support.

### Decision 3: Diagram Definitions in Python Module

Store diagram definitions in `src/book_builder/diagrams/chapter1.py`:

```python
# src/book_builder/diagrams/chapter1.py
DIAGRAM_1_ANATOMY = DiagramDefinition(
    title="Diagram 1: Anatomy of a Kakuro Grid",
    grids=[DiagramGrid(...)],
    annotations=[...],
)
```

**Why:** Python is more flexible than YAML for complex structures, allows computed values, easy refactoring.

**Alternative considered:** YAML files - rejected because diagrams have complex nested structures that are verbose in YAML.

### Decision 4: DiagramRenderer Class

```python
class DiagramRenderer:
    def __init__(self, config: BookConfig):
        self.config = config
        self.cell_size = 0.5 * inch
        self.colors = config.layout.diagram_colors or DEFAULT_COLORS
    
    def render(self, diagram: DiagramDefinition) -> Drawing:
        """Render a diagram definition to a ReportLab Drawing."""
        ...
    
    def render_grid(self, grid: DiagramGrid, x: float, y: float) -> Group:
        """Render a single grid at the specified position."""
        ...
    
    def render_annotation(self, annotation: Annotation, ...) -> Group:
        """Render an annotation box."""
        ...
```

### Decision 5: Integration with ChapterRenderer

The `ChapterRenderer` will detect diagram references and delegate to `DiagramRenderer`:

```python
# In chapter_renderer.py
def _create_image(self, image_path: str, alt_text: str, chapter_dir: Path):
    # Check if this is a programmatic diagram
    if image_path.endswith('.diagram') or 'diagram_' in image_path:
        return self._create_programmatic_diagram(image_path, alt_text)
    # ... existing image loading logic
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Diagram definitions verbose | Use helper functions to reduce boilerplate |
| Learning curve for new diagrams | Provide well-commented examples |
| Can't preview without building PDF | Add a `preview_diagram.py` script |

## Migration Plan

1. Create `DiagramRenderer` class and data structures
2. Define all Chapter 1 diagrams in Python
3. Update `ChapterRenderer` to use programmatic diagrams
4. Remove HTML source files and conversion scripts (deprecate, don't delete yet)
5. Verify all diagrams render correctly
6. Repeat for Chapter 2

## File Structure

```
src/book_builder/
├── diagram_renderer.py      # DiagramRenderer class
├── diagram_models.py        # Dataclass definitions
└── diagrams/
    ├── __init__.py
    ├── chapter1.py          # Chapter 1 diagram definitions
    ├── chapter2.py          # Chapter 2 diagram definitions
    └── common.py            # Shared components (legends, styles)
```

## Open Questions

1. Should we support both Python and YAML definitions? (Leaning no - Python is more flexible)
2. Should diagrams be cached/serialized for faster rebuilds? (Probably not needed - rendering is fast)

