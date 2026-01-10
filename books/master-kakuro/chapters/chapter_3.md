# Chapter 3: Your First Puzzle Walkthrough

Theory is great. But nothing beats solving your first puzzle.

In this chapter, we're going to solve a small Kakuro grid together. Step by step.

Don't just read this. Grab a pencil and follow along. By the end, you'll feel the rhythm of the game.

---

## The Puzzle

We have a compact grid with four clues. It looks simple, but it requires us to use the two core techniques we played with in Chapter 2: **Unique Combinations** and **Elimination**.

Here is our starting grid:

-   **Horizontal Clues (rows):** 11 and 7
-   **Vertical Clues (columns):** 4 and 14

Let's begin.

---

## Step 1: Scan for Unique Combinations

Remember the first rule of starting? Look for unique sums.

We scan the clues:
-   **11 in 2 cells:** Many options (2+9, 3+8, 4+7, 5+6). Not unique.
-   **7 in 2 cells:** Many options (1+6, 2+5, 3+4). Not unique.
-   **14 in 2 cells:** 5+9, 6+8. Not unique.
-   **4 in 2 cells:** **Bingo.**

The sum of 4 in two cells can ONLY be 1 + 3.

We don't know yet which cell is 1 and which is 3. But we know for a fact that those two cells contain those two digits.

![Step 1 Analysis](visuals/diagrams/chapter3/diagram_1.png)
*Diagram 1: We identify the sum of 4 as our starting point.*

---

## Step 2: Investigation & Elimination

Now we have a strong foothold. The first column contains {1, 3}.

Let's look at the top-left cell. It's the intersection of the **Row summing to 11** and the **Column summing to 4**.

Let's test our two candidates:

**Scenario A: The top-left cell is 1.**
If the top-left is 1, then the other cell in that row must be 10 (because 1 + 10 = 11).
But 10 is not a single digit! The maximum digit is 9.
So, the top-left cell **cannot be 1**.

**Scenario B: The top-left cell is 3.**
If the top-left is 3, then the other cell in that row must be 8 (because 3 + 8 = 11).
Does 8 work? Yes, it's a valid digit.

**Conclusion:** The top-left cell MUST be 3.

![Step 2 Elimination](visuals/diagrams/chapter3/diagram_2.png)
*Diagram 2: By testing our candidates, we prove that '3' is the only valid digit for the intersection.*

---

## Step 3: Completing the Intersections

Now the dominoes start to fall.

1.  **Vertical fill:** Since the top-left is 3, and the column sums to 4, the cell below it must be 1 (4 - 3 = 1).
2.  **Horizontal fill:** Since the top-left is 3, and the row sums to 11, the cell to its right must be 8 (11 - 3 = 8).

We fill these in confidently.

![Step 3 Intersections](visuals/diagrams/chapter3/diagram_3.png)
*Diagram 3: One determined digit allows us to fill two more cells instantly.*

---

## Step 4: The Final Cell

We have one cell left. The bottom-right empty square.

We can solve this two ways to check our work:
1.  **Across:** The bottom row sums to 7. We already have a 1. So 7 - 1 = **6**.
2.  **Down:** The right column sums to 14. We already have an 8. So 14 - 8 = **6**.

Both match! The last digit is 6.

![Step 4 Completion](visuals/diagrams/chapter3/diagram_4.png)
*Diagram 4: The final cell matches both clues. The puzzle is solved.*

---

## Lessons Learned

This small puzzle demonstrated the exact workflow you'll use on larger grids:

1.  **Find the weak point:** We started with the unique sum (4).
2.  **Use intersections:** We used the crossing row (11) to decide between candidates (1 vs 3).
3.  **Calculate the rest:** Once the intersection was solved, simple math filled the remaining cells.
4.  **Verify:** The final cell satisfied both clues perfectly.

You are now ready to tackle the Beginner Puzzles in Part 2. Turn the page, and good luck!
