#!/usr/bin/env python

import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict

import yaml
from yamale import YamaleError, make_data, make_schema, validate
from yamale.validators import DefaultValidators

OWNERS = Path("owners.yaml")
OWNERS_SCHEMA = Path("owners_schema.yaml")


def check_owners_file():
    for f in sys.argv[1:]:
        if f == str(OWNERS):
            return False
    return True


def validate_schema():
    validators = DefaultValidators.copy()
    schema = make_schema(OWNERS_SCHEMA, validators=validators)
    config_data = make_data(OWNERS)
    try:
        validate(schema=schema, data=config_data, strict=True)
    except YamaleError as e:
        exit(
            f"Error validating config from {str(OWNERS)}. Errors: {','.join([str(result) for result in e.results])}"
        )


def main():
    if check_owners_file():
        return

    validate_schema()
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
