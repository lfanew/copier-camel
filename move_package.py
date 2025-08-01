#!/usr/bin/env python3
import shutil
import sys
from pathlib import Path

def main():
    # Expect project_folder and package_name
    if len(sys.argv) != 3:
        print(
            "Usage: python move_package.py <project_folder> <package_name>",
            file=sys.stderr
        )
        sys.exit(1)

    project_folder = sys.argv[1]
    pkg            = sys.argv[2]  # e.g. com.example.demo

    # Base path where Java sources are located
    base = Path(project_folder) / "src" / "main" / "java"
    if not base.exists():
        print(f"Error: Java source base not found at {base}", file=sys.stderr)
        sys.exit(1)

    # Locate the placeholder PackagePath directory
    source_dir = base / "PackagePath"
    if not source_dir.exists():
        print(f"Error: {source_dir} not found.", file=sys.stderr)
        sys.exit(1)

    # Compute destination for the Java package
    dest = base / Path(pkg.replace('.', '/'))
    dest.mkdir(parents=True, exist_ok=True)

    # Move all files and directories from PackagePath into the package path
    for item in source_dir.rglob("*"):
        rel    = item.relative_to(source_dir)
        target = dest / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(target))

    # Remove the now-empty PackagePath directory
    shutil.rmtree(source_dir)
    print(f"✅ Moved Java sources into {dest}")

    try:
        Path(__file__).unlink()
    except Exception:
        pass

if __name__ == "__main__":
    main()