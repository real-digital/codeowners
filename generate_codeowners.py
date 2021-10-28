#!/usr/bin/env python

import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict

import yaml

OWNERS = Path("owners.yaml")


def main():
    if sys.argv[1] != str(OWNERS):
        exit(f"missing owners file in {sys.argv}")

    with OWNERS.open("r") as ows:
        try:
            paths_file = yaml.safe_load(ows)
        except yaml.YAMLError as exc:
            exit(str(exc))
        codeowners_root = ""
        codeowners = ""
        groups: Dict[str, Dict[str, str]] = defaultdict(dict)
        for path in paths_file["paths"]:
            group = "root"
            if "group" in path:
                group = path["group"]
            groups[group][path["path"]] = path["owners"]
        for k, group in groups.items():
            if k == "root":
                for path, owners in group.items():
                    join_owners = " ".join([f"@{o}" for o in owners])
                    codeowners_root += f"{path} {join_owners}\n"
            else:
                codeowners += f"\n[{k}]\n"
                for path, owners in group.items():
                    join_owners = " ".join([f"@{o}" for o in owners])
                    codeowners += f"{path} {join_owners}\n"
        with Path("CODEOWNERS").open("w") as owners:
            owners.write(codeowners_root + "\n")
            owners.write(codeowners)


if __name__ == "__main__":
    main()
