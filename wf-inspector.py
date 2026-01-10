import yaml
from pathlib import Path

WORKFLOWS_DIR = Path(".github/workflows")

def load_yaml(path: Path):
    with path.open() as f:
        return yaml.safe_load(f)

def extract_on(on_field):
    if isinstance(on_field, dict):
        return list(on_field.keys())
    if isinstance(on_field, list):
        return on_field
    if isinstance(on_field, str):
        return [on_field]
    return []

def inspect_workflow(path: Path):
    data = load_yaml(path)

    name = data.get("name", path.name)
    events = extract_on(data.get("on"))
    permissions = "permissions" in data
    concurrency = "concurrency" in data

    external_reusables = []

    for job in data.get("jobs", {}).values():
        uses = job.get("uses")
        if isinstance(uses, str) and "/" in uses and "@” in uses:
            external_reusables.append(uses)

    return {
        "file": str(path),
        "name": name,
        "events": events,
        "permissions": permissions,
        "concurrency": concurrency,
        "external_reusables": external_reusables,
    }

def main():
    workflows = WORKFLOWS_DIR.rglob("*.yml")

    print("Workflow inventory\n")

    for wf in workflows:
        info = inspect_workflow(wf)
        print(f"- {info['name']}")
        print(f"  file: {info['file']}")
        print(f"  events: {', '.join(info['events']) or 'UNKNOWN'}")
        print(f"  permissions declared: {info['permissions']}")
        print(f"  concurrency declared: {info['concurrency']}")

        if info["external_reusables"]:
            print("  external reusable workflows:")
            for r in info["external_reusables"]:
                print(f"    - {r}")
        print()

if __name__ == "__main__":
    main()
