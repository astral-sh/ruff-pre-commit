"""Updates the version in the readme and git commit."""

import re
from pathlib import Path
from subprocess import check_call, check_output


def main():
    readme_md = Path("README.md")
    readme = readme_md.read_text()
    rev = Path(".version").read_text().strip()
    readme = re.sub(r"rev: v\d+\.\d+\.\d+", f"rev: v{rev}", readme)
    readme = re.sub(r"/ruff/\d+\.\d+\.\d+\.svg", f"/ruff/{rev}.svg", readme)
    readme_md.write_text(readme)

    # Only commit on change.
    # https://stackoverflow.com/a/9393642/3549270
    if check_output(["git", "status", "-s"]).strip():
        check_call(["git", "add", readme_md])
        check_call(["git", "commit", "-m", f"Bump README.md version to {rev}"])
    else:
        print("No change")


if __name__ == "__main__":
    main()
