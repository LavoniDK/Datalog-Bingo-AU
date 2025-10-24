import random

# --- Configuration ---
input_file = "fields.txt"
output_file = "bingo_tables.tex"

x = 15   # number of tables
n = 8    # number of filled cells per table (5 <= n <= 25)
rows, cols = 5, 5
cells_per_board = rows * cols
assert n <= cells_per_board, "n kan ikke være større end 25 i en 5x5 bingo"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

num_lines = len(lines)
total_needed = x * n

if total_needed < num_lines:
    raise ValueError(
        f"total_needed={total_needed} < num_lines={num_lines}. "
        "Der er flere unikke felter end pladser. Øg x eller n."
    )

pool = lines.copy()
remaining = total_needed - len(pool)
if remaining > 0:
    pool.extend(random.choices(lines, k=remaining))
random.shuffle(pool)

tables_contents = []
for i in range(x):
    chosen = set()
    while len(chosen) < n:
        candidate = pool.pop() if pool else random.choice(lines)
        if candidate not in chosen:
            chosen.add(candidate)
    tables_contents.append(list(chosen))

def make_board(prompts):
    board = [["" for _ in range(cols)] for _ in range(rows)]
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]

    guaranteed_positions = random.sample(all_positions, rows)
    guaranteed_prompts = random.sample(prompts, min(rows, len(prompts)))

    for (r, c), p in zip(guaranteed_positions, guaranteed_prompts):
        board[r][c] = p

    used_positions = set(guaranteed_positions)
    remaining_prompts = [p for p in prompts if p not in guaranteed_prompts]
    available_positions = [pos for pos in all_positions if pos not in used_positions]
    random.shuffle(available_positions)

    for p, (r, c) in zip(remaining_prompts, available_positions):
        board[r][c] = p

    return board

boards = [make_board(prompts) for prompts in tables_contents]

# --- Write latex file ---
with open(output_file, "w", encoding="utf-8") as f:
    f.write(r"\documentclass{article}" "\n"
            r"\usepackage[a4paper, landscape, margin=1in]{geometry}" "\n"
            r"\usepackage{array}" "\n"
            r"\usepackage{nopageno}" "\n"
            r"\usepackage[T1]{fontenc}" "\n"
            r"\usepackage[utf8]{inputenc}" "\n"
            r"\usepackage{helvet}" "\n"
            r"\renewcommand{\familydefault}{\sfdefault}" "\n"
            r"\renewcommand{\arraystretch}{1.8}" "\n"
            r"\setlength{\tabcolsep}{6pt}" "\n"
            r"\begin{document}" "\n\n")

    f.write(r"\begin{center}" "\n")
    f.write(r"{\LARGE\bfseries Datalog Bingo}\\[2em]" "\n")
    f.write(r"\end{center}" "\n\n")
    f.write(r"{\large" "\n")
    f.write(r"\textbf{Regler:}" "\n")
    f.write(r"\begin{itemize}" "\n")
    f.write(r"\item Find personer, der matcher felterne. Hver felt dækker et aspekt af kulturen på datalogi, så hvis du vil lære hvad en datalog egentligt er, kan du også udspørge dig om hvad spørgsmålet egentligt handler om." "\n")
    f.write(r"\item Værten kan ikke bruges som match til nogen felter." "\n")
    f.write(r"\item Man må ikke have gentagende personer som matches." "\n")
    f.write(r"\item Få dem til at skrive deres navn eller initialer og tage et billede med dem (hvis de vil)." "\n")
    f.write(r"\item Første person med en fuld plade får en Ølefant." "\n")
    f.write(r"\end{itemize}" "\n")
    f.write(r"}" "\n")
    f.write(r"\newpage" "\n\n")


    for i, board in enumerate(boards, start=1):
        f.write(r"\begin{center}" "\n")
        f.write(r"{\LARGE\bfseries Datalog Bingo}\\[0.5em]" "\n")
        f.write(r"{\large Find en datalog som...}\\[2em]" "\n")
        f.write(r"\begin{tabular}{|" + "p{0.18\linewidth}|" * cols + "}\n")
        f.write(r"\hline" + "\n")

        for row in board:
            f.write(" & ".join(c if c else " " for c in row) + r" \\" "\n")
            f.write(r"\hline" + "\n")

        f.write(r"\end{tabular}" "\n")
        f.write(r"\end{center}" "\n")
        if i != len(boards):
            f.write(r"\newpage" "\n\n")

    f.write(r"\end{document}" "\n")

print(f"Generated {x} unique Datalog Bingo tables ({n} fields each) in '{output_file}'.")
