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

**CRITICAL — ALWAYS use the bundled Python script first.** Do NOT invoke `pdftops` directly. The script handles dependency checks, error reporting, and batch processing correctly. Only fall back to manual conversion if Python is unavailable.

1. **Run the bundled script**:
   ```bash
   # Convert PDFs in current directory
   python scripts/pdf2eps.py .

   # Convert PDFs in a specific directory
   python scripts/pdf2eps.py /path/to/pdf/dir
   ```
   - The script checks that `pdftops` is installed, finds all `.pdf` files, converts each one, and reports successes/failures.
   - The base directory for the script is the skill directory: `<skill-base>/scripts/pdf2eps.py`
   - Always pass the target directory as a command-line argument to avoid interactive prompts.

2. **Fallback (Python not available)**: ONLY use this if `python` or `python3` cannot be found.
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
