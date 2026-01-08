import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages

def generate_kakuro(h=9, w=9, black_density=0.22):
    grid = [[0]*w for _ in range(h)]
    for i in range(h):
        grid[i][0] = -1
    for j in range(w):
        grid[0][j] = -1
    for i in range(1, h):
        for j in range(1, w):
            if random.random() < black_density:
                grid[i][j] = -1
    
    for _ in range(50):
        changed = False
        h_runs, v_runs = compute_runs(grid, h, w)
        for i in range(1, h):
            for j in range(1, w):
                if grid[i][j] != -1:
                    in_h = any(i == r and c_start <= j < c_start + length for r, c_start, length, _ in h_runs)
                    in_v = any(j == c and r_start <= i < r_start + length for r_start, c, length, _ in v_runs)
                    if not (in_h and in_v):
                        grid[i][j] = -1
                        changed = True
        if not changed:
            break
    
    h_runs, v_runs = compute_runs(grid, h, w)
    if not solve_kakuro(grid, h, w, h_runs, v_runs):
        return generate_kakuro(h, w, black_density)
    return grid, h_runs, v_runs

def compute_runs(grid, h, w):
    h_runs, v_runs = [], []
    for i in range(h):
        j = 0
        while j < w:
            if grid[i][j] == -1:
                start = j + 1
                length = 0
                while start + length < w and grid[i][start + length] != -1:
                    length += 1
                if length >= 2:
                    h_runs.append([i, start, length, 0])
                j = start + length
            else:
                j += 1
    for j in range(w):
        i = 0
        while i < h:
            if grid[i][j] == -1:
                start = i + 1
                length = 0
                while start + length < h and grid[start + length][j] != -1:
                    length += 1
                if length >= 2:
                    v_runs.append([start, j, length, 0])
                i = start + length
            else:
                i += 1
    return h_runs, v_runs

def solve_kakuro(grid, h, w, h_runs, v_runs):
    cells = [(i, j) for i in range(h) for j in range(w) if grid[i][j] == 0]
    def get_constraints(i, j):
        h_cells, v_cells = [], []
        for r, c, length, _ in h_runs:
            if r == i and c <= j < c + length:
                h_cells = [(r, c + k) for k in range(length)]
                break
        for r, c, length, _ in v_runs:
            if c == j and r <= i < r + length:
                v_cells = [(r + k, c) for k in range(length)]
                break
        return h_cells, v_cells
    def is_valid(i, j, val):
        h_cells, v_cells = get_constraints(i, j)
        for ci, cj in h_cells:
            if (ci, cj) != (i, j) and grid[ci][cj] == val:
                return False
        for ci, cj in v_cells:
            if (ci, cj) != (i, j) and grid[ci][cj] == val:
                return False
        return True
    def backtrack(idx):
        if idx == len(cells):
            return True
        i, j = cells[idx]
        for val in random.sample(range(1, 10), 9):
            if is_valid(i, j, val):
                grid[i][j] = val
                if backtrack(idx + 1):
                    return True
                grid[i][j] = 0
        return False
    if backtrack(0):
        for run in h_runs:
            r, c, length, _ = run
            run[3] = sum(grid[r][c + k] for k in range(length))
        for run in v_runs:
            r, c, length, _ = run
            run[3] = sum(grid[r + k][c] for k in range(length))
        return True
    return False

def render_kakuro(grid, h_runs, v_runs, show_solution=False, title="Kakuro"):
    h = len(grid)
    w = len(grid[0])
    cell_size = 0.6
    fig, ax = plt.subplots(figsize=(w * cell_size + 1, h * cell_size + 1.5))
    ax.set_xlim(-0.3, w * cell_size + 0.3)
    ax.set_ylim(-0.5, h * cell_size + 0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(w * cell_size / 2, h * cell_size + 0.5, title, ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    clue_cells = {}
    for r, c, length, s in h_runs:
        clue_j = c - 1
        if clue_j >= 0 and grid[r][clue_j] == -1:
            if (r, clue_j) not in clue_cells:
                clue_cells[(r, clue_j)] = {}
            clue_cells[(r, clue_j)]['across'] = s
    for r, c, length, s in v_runs:
        clue_i = r - 1
        if clue_i >= 0 and grid[clue_i][c] == -1:
            if (clue_i, c) not in clue_cells:
                clue_cells[(clue_i, c)] = {}
            clue_cells[(clue_i, c)]['down'] = s
    
    for i in range(h):
        for j in range(w):
            x = j * cell_size
            y = (h - 1 - i) * cell_size
            if grid[i][j] == -1:
                if (i, j) in clue_cells:
                    ax.add_patch(patches.Rectangle((x, y), cell_size, cell_size, facecolor='#D0D0D0', edgecolor='black', linewidth=0.8))
                    ax.plot([x, x + cell_size], [y + cell_size, y], color='black', linewidth=0.8)
                    clues = clue_cells[(i, j)]
                    if 'across' in clues:
                        ax.text(x + cell_size * 0.75, y + cell_size * 0.75, str(clues['across']), ha='center', va='center', fontsize=8, fontweight='bold')
                    if 'down' in clues:
                        ax.text(x + cell_size * 0.25, y + cell_size * 0.25, str(clues['down']), ha='center', va='center', fontsize=8, fontweight='bold')
                else:
                    ax.add_patch(patches.Rectangle((x, y), cell_size, cell_size, facecolor='black', edgecolor='black', linewidth=0.8))
            else:
                ax.add_patch(patches.Rectangle((x, y), cell_size, cell_size, facecolor='white', edgecolor='black', linewidth=0.5))
                if show_solution and grid[i][j] > 0:
                    ax.text(x + cell_size/2, y + cell_size/2, str(grid[i][j]), ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax.add_patch(patches.Rectangle((0, 0), w * cell_size, h * cell_size, fill=False, edgecolor='black', linewidth=2))
    ax.text(w * cell_size / 2, -0.3, "© Kakuro Press", ha='center', va='top', fontsize=8, style='italic', color='#666666')
    plt.tight_layout()
    return fig

random.seed(42)
grid, h_runs, v_runs = generate_kakuro(h=9, w=9, black_density=0.20)

# Save JPGs
fig = render_kakuro(grid, h_runs, v_runs, show_solution=False, title="Kakuro Puzzle")
fig.savefig('kakuro_puzzle_v5.jpg', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)

fig = render_kakuro(grid, h_runs, v_runs, show_solution=True, title="Solution")
fig.savefig('kakuro_solution_v5.jpg', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(fig)

# Save PDF
with PdfPages('kakuro_v5.pdf') as pdf:
    fig = render_kakuro(grid, h_runs, v_runs, show_solution=False, title="Kakuro Puzzle")
    pdf.savefig(fig, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    fig = render_kakuro(grid, h_runs, v_runs, show_solution=True, title="Solution")
    pdf.savefig(fig, bbox_inches='tight', facecolor='white')
    plt.close(fig)

print("Generated: kakuro_puzzle_v5.jpg, kakuro_solution_v5.jpg, kakuro_v5.pdf")

img = Image.open('kakuro_puzzle_v5.jpg')
plt.figure(figsize=(8, 8))
plt.imshow(img)
plt.axis('off')
plt.show()