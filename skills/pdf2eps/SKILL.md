---
name: pdf2eps
description: 将 PDF 文件转换为 EPS（Encapsulated PostScript）格式。当用户想要将 PDF 文件转换为 EPS、批量转换目录中的 PDF、提到 pdftops、PDF 转 PostScript 转换或嵌入 PDF 图形为 EPS 时使用此技能。即使用户只说"转换这些 PDF"但上下文表明预期输出是 EPS（例如 LaTeX 工作流），也应触发此技能。
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
