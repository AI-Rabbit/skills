#!/usr/bin/env python3
"""Batch convert PDF files in a directory to EPS format using pdftops.

Usage:
    python pdf2eps.py                     # interactive prompt (falls back to cwd if non-TTY)
    python pdf2eps.py <directory>         # convert all PDFs in <directory>
    python pdf2eps.py .                   # convert all PDFs in current directory
"""

import argparse
import subprocess
import sys
from pathlib import Path


def check_pdftops() -> str:
    """Verify pdftops is available and return its path."""
    for cmd in ("pdftops",):
        try:
            subprocess.run([cmd, "-v"], capture_output=True, check=True)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    print("Error: pdftops command not found!")
    print("Please ensure one of the following is installed:")
    print("  - MiKTeX / TeX Live / MacTeX")
    print("  - poppler-utils (Linux)")
    print("  - poppler (macOS via Homebrew)")
    print("  - Xpdf")
    sys.exit(1)


def prompt_directory() -> Path:
    """Prompt user for directory. Falls back to cwd if stdin is not a TTY."""
    if not sys.stdin.isatty():
        print("No directory specified, using current directory.")
        return Path.cwd()

    print("Select the directory to convert:")
    print("  1. Current directory")
    print("  2. Enter a custom path")
    print()
    try:
        choice = input("Enter choice (1 or 2): ").strip()
    except EOFError:
        print("No input available, using current directory.")
        return Path.cwd()

    if choice == "1":
        return Path.cwd()
    elif choice == "2":
        try:
            path_str = input("Enter the directory path: ").strip()
        except EOFError:
            print("No input available, using current directory.")
            return Path.cwd()
        target = Path(path_str)
        if not target.is_dir():
            print(f"Error: '{target}' is not a valid directory.")
            sys.exit(1)
        return target
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch convert PDF files to EPS format using pdftops."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="Directory containing PDF files (default: prompt or current directory)",
    )
    args = parser.parse_args()

    if args.directory:
        target_dir = Path(args.directory)
        if not target_dir.is_dir():
            print(f"Error: '{target_dir}' is not a valid directory.")
            sys.exit(1)
    else:
        target_dir = prompt_directory()

    pdftops = check_pdftops()

    pdf_files = sorted(target_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in '{target_dir}'.")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s) in '{target_dir}'")
    print("Starting conversion...\n")

    converted = 0
    failed = 0

    for pdf in pdf_files:
        eps = pdf.with_suffix(".eps")
        print(f"Converting: {pdf.name}")
        result = subprocess.run(
            [pdftops, "-eps", str(pdf), str(eps)],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  Success: {eps.name}")
            converted += 1
        else:
            print(f"  Failed: {pdf.name}")
            if result.stderr:
                print(f"    {result.stderr.strip()}")
            failed += 1

    print("\n" + "=" * 20)
    print("Conversion completed!")
    print(f"Success: {converted}")
    print(f"Failed:  {failed}")
    print("=" * 20)

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
