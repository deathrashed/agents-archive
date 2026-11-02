#!/usr/bin/env python3
"""Read-only macOS allocated-space inventory; JSON goes to stdout."""
import argparse
import datetime
import json
import os
import subprocess


def inventory(root, depth, timeout=None):
    root = os.path.abspath(os.path.expanduser(root))
    result = {"root": root, "resolved_path": os.path.realpath(root)}
    if os.path.islink(root):
        result.update(skipped="symlink root; measure target separately",
                      target_exists=os.path.exists(root))
        return result
    if not os.path.exists(root):
        result["error"] = "path does not exist"
        return result
    result["device"] = os.stat(root).st_dev
    result["symlinks"] = []
    if os.path.isdir(root):
        try:
            with os.scandir(root) as entries:
                for entry in entries:
                    if entry.is_symlink():
                        result["symlinks"].append({
                            "path": entry.path, "target": os.readlink(entry.path),
                            "resolved_target": os.path.realpath(entry.path),
                            "target_exists": os.path.exists(entry.path)})
        except OSError as error:
            result["listing_error"] = str(error)
    command = ["/usr/bin/du", "-P", "-x", "-k", "-d", str(depth), root]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
        result["complete"] = returncode == 0
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
        stdout, stderr, returncode = decode(error.stdout), decode(error.stderr), None
        result.update(complete=False, timed_out=True, timeout_seconds=timeout)
    rows = []
    unparsed = []
    for line in stdout.splitlines():
        size, sep, path = line.partition("\t")
        if sep and size.isdigit():
            rows.append({"path": path, "allocated_bytes": int(size) * 1024})
        else:
            unparsed.append(line)
    result.update(entries=sorted(rows, key=lambda row: row["allocated_bytes"], reverse=True),
                  returncode=returncode, errors=stderr.splitlines())
    if unparsed:
        result["unparsed_output"] = unparsed
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", help="Explicit roots; links are not followed")
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=None,
                        help="Maximum seconds per root; preserve partial rows and mark incomplete")
    args = parser.parse_args()
    if args.depth < 0:
        parser.error("depth must be non-negative")
    if args.timeout is not None and args.timeout <= 0:
        parser.error("timeout must be positive")
    print(json.dumps({
        "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "measurement": "allocated KiB from du; parent/child and overlapping roots are not additive",
        "roots": [inventory(root, args.depth, args.timeout) for root in args.roots]
    }, indent=2))


if __name__ == "__main__":
    main()
