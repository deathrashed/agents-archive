#!/usr/bin/env python3
"""Generate shields.io badge HTML from YAML config."""

import argparse
import yaml


def generate_badge(name, label, msg, base_color="1e1e1e", logo_color="white", logo=""):
    url = f"https://img.shields.io/badge/{label.replace(' ', '%20')}-{msg.replace(' ', '%20')}-{base_color}?style=for-the-badge"
    if logo:
        url += f"&logo={logo}&logoColor={logo_color}"
    return f"[![{name}]({url})]({name})"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    for badge in config.get("badges", []):
        print(generate_badge(**badge))
