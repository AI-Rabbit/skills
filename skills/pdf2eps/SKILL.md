---
name: pdf2eps
description: Convert PDF files to EPS (Encapsulated PostScript) format. Use this skill whenever the user wants to convert PDF files to EPS, batch convert PDFs in a directory, or mentions pdftops, PDF to PostScript conversion, or embedding PDF graphics as EPS. Trigger this skill even if the user only says "convert these PDFs" in a context where EPS is the expected output (e.g., LaTeX workflows).
---

# PDF to EPS Converter

This skill converts all PDF files in a specified directory to EPS format using the `pdftops` command-line tool.

## Prerequisites

The `pdftops` utility must be installed and available in the system PATH. Common sources:
- **Windows**: MiKTeX, TeX Live, or Xpdf
- **Linux**: `poppler-utils` package (e.g., `apt install poppler-utils`)
- **macOS**: `poppler` via Homebrew (e.g., `brew install poppler`) or MacTeX

## Workflow

1. **Run the bundled script** (preferred):
   ```bash
   python scripts/pdf2eps.py
   ```
   - The script will interactively prompt the user to choose between:
     1. Current working directory
     2. A user-specified custom path
   - If the chosen path is invalid, the script exits with an error.

2. **Fallback without Python**: If Python is not available, perform the conversion manually:
   - Check that `pdftops` is installed.
   - Find all `.pdf` files in the target directory.
   - For each PDF, run:
     ```
     pdftops -eps "<input.pdf>" "<output.eps>"
     ```
   - Quote file paths to handle spaces and preserve base filenames.
   - Continue through all files even if one fails, then report the total count, successes, and failures.

## Error Handling

- **Missing dependency**: Explain what `pdftops` is and how to install it for the user's OS.
- **No PDFs found**: Clearly state that no `.pdf` files were detected in the target directory.
- **Partial failures**: Do not stop the batch on a single failure; complete all conversions and report which ones failed at the end.
