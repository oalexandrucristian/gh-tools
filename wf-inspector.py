from pathlib import Path
import yaml
import sys

WORKFLOWS_DIR = Path(".github/workflows")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

errors = []
warnings = []

def annotate(level, file, line, message):
    print(f"::{level} file={file},line={line}::{message}")

def inspect_workflow(path: Path):
    with path.open() as f:
        data = yaml.safe_load(f) or {}

    # Rule: permissions required
    if "permissions" not in data:
        errors.append((path, 1, "Missing top-level 'permissions' block"))
        annotate("error", path, 1, "Missing top-level 'permissions' block")

    # Rule: external reusable workflow pinned to main
    for job in data.get("jobs", {}).values():
        uses = job.get("uses")
        if isinstance(uses, str) and "@main" in uses:
            warnings.append((path, 1, f"External reusable workflow pinned to @main: {uses}"))
            annotate("warning", path, 1, f"External reusable workflow pinned to @main")

# Scan
workflows = list(WORKFLOWS_DIR.glob("*.yml"))
for wf in workflows:
    inspect_workflow(wf)

# --- Write Job Summary ---
summary = REPORTS_DIR / "summary.md"
with summary.open("w") as f:
    f.write("# Workflow Inspector Report\n\n")
    f.write(f"✔ **{len(workflows)} workflows scanned**\n")
    f.write(f"⚠ **{len(warnings)} warnings**\n")
    f.write(f"❌ **{len(errors)} errors**\n\n")

    if errors:
        f.write("## Errors\n")
        for file, _, msg in errors:
            f.write(f"- `{file}` — {msg}\n")
        f.write("\n")

    if warnings:
        f.write("## Warnings\n")
        for file, _, msg in warnings:
            f.write(f"- `{file}` — {msg}\n")

# Exit code → BLOCK PR
if errors:
    sys.exit(1)
