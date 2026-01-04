import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.backends.backend_pdf import PdfPages

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['pdf.fonttype'] = 42

random.seed(42)

def generate_valid_kakuro(grid_size=8, max_attempts=500):
    h, w = grid_size + 1, grid_size + 1
    
    for attempt in range(max_attempts):
        is_black = [[True if i == 0 or j == 0 else False for j in range(w)] for i in range(h)]
        
        black_density = 0.22
        for i in range(1, h):
            for j in range(1, w):
                if random.random() < black_density:
                    is_black[i][j] = True
                    is_black[h - i][w - j] = True
        
        # Iteratively fix orphan cells
        changed = True
        while changed:
            changed = False
            
            h_run_len = [[0]*w for _ in range(h)]
            v_run_len = [[0]*w for _ in range(h)]
            
            # Compute horizontal run lengths
            for i in range(1, h):
                j = 1
                while j < w:
                    if is_black[i][j]:
                        j += 1
                        continue
                    start = j
                    while j < w and not is_black[i][j]:
                        j += 1
                    length = j - start
                    for jj in range(start, j):
                        h_run_len[i][jj] = length
            
            # Compute vertical run lengths
            for j in range(1, w):
                i = 1
                while i < h:
                    if is_black[i][j]:
                        i += 1
                        continue
                    start = i
                    while i < h and not is_black[i][j]:
                        i += 1
                    length = i - start
                    for ii in range(start, i):
                        v_run_len[ii][j] = length
            
            # Convert cells not in both runs (len >= 2) to black
            for i in range(1, h):
                for j in range(1, w):
                    if not is_black[i][j]:
                        if h_run_len[i][j] < 2 or v_run_len[i][j] < 2:
                            is_black[i][j] = True
                            changed = True
        
        # Now assign run IDs
        h_run_id = [[-1]*w for _ in range(h)]
        v_run_id = [[-1]*w for _ in range(h)]
        run_count = 0
        
        for i in range(1, h):
            j = 1
            while j < w:
                if is_black[i][j]:
                    j += 1
                    continue
                cells = []
                while j < w and not is_black[i][j]:
                    cells.append((i, j))
                    j += 1
                if len(cells) >= 2:
                    for (ri, rj) in cells:
                        h_run_id[ri][rj] = run_count
                    run_count += 1
        
        for j in range(1, w):
            i = 1
            while i < h:
                if is_black[i][j]:
                    i += 1
                    continue
                cells = []
                while i < h and not is_black[i][j]:
                    cells.append((i, j))
                    i += 1
                if len(cells) >= 2:
                    for (ri, rj) in cells:
                        v_run_id[ri][rj] = run_count
                    run_count += 1
        
        white_cells = [(i, j) for i in range(1, h) for j in range(1, w) 
                       if not is_black[i][j]]
        
        if len(white_cells) < 20:
            continue
        
        # Fill values
        value = [[0]*w for _ in range(h)]
        used = [set() for _ in range(run_count)]
        
        def fill(pos):
            if pos == len(white_cells):
                return True
            i, j = white_cells[pos]
            hid, vid = h_run_id[i][j], v_run_id[i][j]
            for num in range(1, 10):
                if num not in used[hid] and num not in used[vid]:
                    value[i][j] = num
                    used[hid].add(num)
                    used[vid].add(num)
                    if fill(pos + 1):
                        return True
                    used[hid].remove(num)
                    used[vid].remove(num)
                    value[i][j] = 0
            return False
        
        if not fill(0):
            continue
        
        # FIXED CLUE PLACEMENT:
        # For each run, find the black cell immediately before it and place the clue there
        across_clue = [[0]*w for _ in range(h)]
        down_clue = [[0]*w for _ in range(h)]
        
        # Horizontal runs: clue goes in the black cell to the LEFT of the first white cell
        for i in range(1, h):
            j = 1
            while j < w:
                if is_black[i][j]:
                    j += 1
                    continue
                start_j = j
                s = 0
                while j < w and not is_black[i][j]:
                    s += value[i][j]
                    j += 1
                if j - start_j >= 2:
                    # Clue cell is at (i, start_j - 1) - must be black
                    clue_j = start_j - 1
                    if clue_j >= 0 and is_black[i][clue_j]:
                        across_clue[i][clue_j] = s
        
        # Vertical runs: clue goes in the black cell ABOVE the first white cell
        for j in range(1, w):
            i = 1
            while i < h:
                if is_black[i][j]:
                    i += 1
                    continue
                start_i = i
                s = 0
                while i < h and not is_black[i][j]:
                    s += value[i][j]
                    i += 1
                if i - start_i >= 2:
                    # Clue cell is at (start_i - 1, j) - must be black
                    clue_i = start_i - 1
                    if clue_i >= 0 and is_black[clue_i][j]:
                        down_clue[clue_i][j] = s
        
        print(f"Valid puzzle generated on attempt {attempt + 1}, {len(white_cells)} white cells")
        return is_black, across_clue, down_clue, value
    
    raise RuntimeError("Could not generate valid puzzle")


def draw_premium(ax, is_black, across_clue, down_clue, value, is_solution, title, subtitle):
    h_g, w_g = len(is_black), len(is_black[0])
    cell = 0.55
    
    grid_w, grid_h = w_g * cell, h_g * cell
    page_w, page_h = 8.5, 11
    ox = (page_w - grid_w) / 2
    oy = 2.2
    
    ax.set_xlim(0, page_w)
    ax.set_ylim(0, page_h)
    ax.invert_yaxis()
    ax.axis('off')
    ax.set_aspect('equal')
    
    clue_gray = '#B8B8B8'
    black_fill = '#000000'
    white_fill = '#FFFFFF'
    line_color = '#000000'
    text_color = '#000000'
    
    ax.text(page_w/2, 0.6, title, fontsize=28, fontweight='bold', color='#1a1a1a', ha='center')
    ax.text(page_w/2, 1.1, subtitle, fontsize=14, color='#555555', ha='center')
    ax.add_line(Line2D([ox, ox + grid_w], [1.5, 1.5], color='#C9A227', lw=3))
    
    for i in range(h_g):
        for j in range(w_g):
            x, y = ox + j * cell, oy + i * cell
            has_across = across_clue[i][j] > 0
            has_down = down_clue[i][j] > 0
            
            if is_black[i][j]:
                if has_across or has_down:
                    ax.add_patch(Rectangle((x, y), cell, cell, 
                                          facecolor=clue_gray, edgecolor=line_color, lw=1.2))
                    ax.add_line(Line2D([x, x + cell], [y, y + cell], color=line_color, lw=1.2))
                    if has_down:
                        ax.text(x + cell * 0.72, y + cell * 0.35, str(down_clue[i][j]),
                               color=text_color, fontsize=11, fontweight='medium', ha='center', va='center')
                    if has_across:
                        ax.text(x + cell * 0.28, y + cell * 0.68, str(across_clue[i][j]),
                               color=text_color, fontsize=11, fontweight='medium', ha='center', va='center')
                else:
                    ax.add_patch(Rectangle((x, y), cell, cell, 
                                          facecolor=black_fill, edgecolor=line_color, lw=1.2))
            else:
                ax.add_patch(Rectangle((x, y), cell, cell, 
                                       facecolor=white_fill, edgecolor=line_color, lw=1.0))
                if is_solution and value[i][j] > 0:
                    ax.text(x + cell/2, y + cell/2, str(value[i][j]),
                           fontsize=16, color=text_color, fontweight='bold', ha='center', va='center')
    
    ax.add_patch(Rectangle((ox, oy), grid_w, grid_h, fill=False, edgecolor=line_color, lw=2.5))
    ax.text(page_w/2, oy + grid_h + 0.6, "© Kakuro Press  •  Premium Collection",
           fontsize=10, color='#777777', ha='center')


is_black, across_clue, down_clue, value = generate_valid_kakuro(grid_size=8)

with PdfPages('premium_kakuro_v3.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(8.5, 11))
    fig.patch.set_facecolor('#FFFFFF')
    draw_premium(ax, is_black, across_clue, down_clue, value, False, "KAKURO", "Easy  •  Puzzle No. 1")
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.3)
    fig.savefig('premium_puzzle_v3.jpg', dpi=250, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close(fig)
    
    fig, ax = plt.subplots(figsize=(8.5, 11))
    fig.patch.set_facecolor('#FFFFFF')
    draw_premium(ax, is_black, across_clue, down_clue, value, True, "SOLUTION", "Easy  •  Puzzle No. 1")
    pdf.savefig(fig, bbox_inches='tight', pad_inches=0.3)
    fig.savefig('premium_solution_v3.jpg', dpi=250, bbox_inches='tight', pad_inches=0.3, facecolor='white')
    plt.close(fig)

print("Done")

from PIL import Image
img = Image.open('premium_solution_v3.jpg')
plt.figure(figsize=(10, 13))
plt.imshow(img)
plt.axis('off')
plt.tight_layout()
plt.show()