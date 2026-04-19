import os
import sys
import json
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / ".config.json"
DEFAULT_REPO = "https://github.com/loongyowl/my-skills.git"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    return {"repo_url": DEFAULT_REPO, "local_path": str(SCRIPT_DIR)}


def save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def get_index() -> dict:
    config = load_config()
    local_path = Path(config["local_path"])
    index_file = local_path / "index.json"

    if index_file.exists():
        return json.loads(index_file.read_text(encoding="utf-8"))

    index_url = config["repo_url"].replace(".git", "") + "/raw/main/index.json"
    try:
        with urllib.request.urlopen(index_url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except:
        print("Error: Cannot fetch index. Run 'skills-cli init' first.")
        sys.exit(1)


def cmd_init(repo_url: Optional[str] = None):
    config = load_config()

    if repo_url:
        config["repo_url"] = repo_url

    local_path = Path(config["local_path"])

    if local_path.exists():
        print(f"Pulling latest from {config['repo_url']}...")
        subprocess.run(["git", "pull"], cwd=local_path, capture_output=True)
    else:
        print(f"Cloning {config['repo_url']}...")
        subprocess.run(["git", "clone", config["repo_url"], str(local_path)], capture_output=True)

    save_config(config)
    print(f"Initialized at: {local_path}")


def cmd_search(keyword: str):
    index = get_index()
    skills = index.get("skills", {})

    print(f"\nSearching for '{keyword}'...\n")

    found = False
    for name, info in sorted(skills.items()):
        desc = info.get("description", "").lower()
        tags = " ".join(info.get("tags", [])).lower()
        name_lower = name.lower()

        if keyword.lower() in desc or keyword.lower() in tags or keyword.lower() in name_lower:
            print(f"  {name}")
            print(f"    {info.get('description', '')[:70]}...")
            print(f"    Tags: {', '.join(info.get('tags', []))}")
            print()
            found = True

    if not found:
        print("No matching skills found.")


def cmd_list():
    index = get_index()
    skills = index.get("skills", {})

    print(f"\nAvailable Skills ({len(skills)}):\n")
    for name, info in sorted(skills.items()):
        print(f"  {name}")
        print(f"    {info.get('description', '')[:60]}...")
        print()


def cmd_install(skill_name: str):
    config = load_config()
    local_path = Path(config["local_path"])
    skills_dir = local_path / "skills"

    if not skills_dir.exists():
        print("Error: Skills repository not initialized. Run 'skills-cli init' first.")
        sys.exit(1)

    target_dir = skills_dir / skill_name

    if not target_dir.exists():
        print(f"Error: Skill '{skill_name}' not found.")
        sys.exit(1)

    current_dir = Path.cwd()
    dest_dir = current_dir / ".skills" / skill_name

    import shutil
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    shutil.copytree(target_dir, dest_dir)

    print(f"Installed '{skill_name}' to {dest_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  skills-cli init [repo_url]")
        print("  skills-cli search <keyword>")
        print("  skills-cli list")
        print("  skills-cli install <skill-name>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        repo_url = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_init(repo_url)
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: skills-cli search <keyword>")
            sys.exit(1)
        cmd_search(sys.argv[2])
    elif command == "list":
        cmd_list()
    elif command == "install":
        if len(sys.argv) < 3:
            print("Usage: skills-cli install <skill-name>")
            sys.exit(1)
        cmd_install(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
