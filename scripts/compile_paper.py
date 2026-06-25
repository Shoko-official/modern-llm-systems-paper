#!/usr/bin/env python3
import os
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
SECTIONS_DIR = ROOT / "sections"
PAPER_DIR = ROOT / "paper"
REFERENCES_DIR = ROOT / "references"
FIGURES_DIR = ROOT / "figures"

SECTION_FILES_ORDER = [
    "abstract.md",
    "introduction.md",
    "system-layers.md",
    "training-and-adaptation.md",
    "inference-and-serving.md",
    "retrieval-and-memory.md",
    "agents-and-tool-use.md",
    "agent-runtime.md",
    "deployment.md",
    "evaluation.md",
    "security-and-governance.md",
    "observability.md",
    "decision-matrix.md",
    "conclusion.md",
]

def clean_markdown_for_latex(text: str) -> str:
    # Remove metadata/headers like Draft status, Purpose, Evidence requirement
    lines = text.splitlines()
    cleaned_lines = []
    skip_headers = {"draft status:", "purpose:", "evidence requirement:"}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        lower_line = line.strip().lower()
        
        # Skip specific headers or metadata lines
        if any(lower_line.startswith(h) for h in skip_headers):
            # Skip this line and all subsequent non-empty lines (multi-line metadata paragraph)
            i += 1
            while i < len(lines) and lines[i].strip() != "":
                i += 1
            # Also skip the trailing empty line if present
            if i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
            
        cleaned_lines.append(line)
        i += 1
        
    text = "\n".join(cleaned_lines)
    
    # Convert main title heading (# Title) -> \section{Title}
    text = re.sub(r"^#\s+(.+)$", r"\\section{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s+(.+)$", r"\\subsection{\1}", text, flags=re.MULTILINE)
    text = re.sub(r"^###\s+(.+)$", r"\\subsubsection{\1}", text, flags=re.MULTILINE)
    
    # Convert bold text **word** -> \textbf{word}
    text = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", text)
    
    # Convert citation markers [@key] -> \cite{key}
    text = re.sub(r"\[@([a-zA-Z0-9_\-]+)\]", r"\\cite{\1}", text)
    
    # Convert bullet points to list environments
    lines = text.splitlines()
    in_list = False
    latex_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("* ") or stripped.startswith("- "):
            if not in_list:
                latex_lines.append("\\begin{itemize}")
                in_list = True
            item_text = stripped[2:]
            latex_lines.append(f"  \\item {item_text}")
        else:
            if in_list:
                latex_lines.append("\\end{itemize}")
                in_list = False
            latex_lines.append(line)
            
    if in_list:
        latex_lines.append("\\end{itemize}")
        
    return "\n".join(latex_lines)

def compile_latex() -> None:
    print("Assembling paper from markdown sources...")
    
    # Create dist directory
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    latex_document = []
    
    # Standard LaTeX preamble
    latex_document.append("\\documentclass[11pt]{article}")
    latex_document.append("\\usepackage[utf8]{inputenc}")
    latex_document.append("\\usepackage{amsmath}")
    latex_document.append("\\usepackage{graphicx}")
    latex_document.append("\\usepackage{booktabs}")
    latex_document.append("\\usepackage{cite}")
    latex_document.append("\\usepackage{hyperref}")
    latex_document.append("")
    latex_document.append("\\title{Modern LLM Systems 2026}")
    latex_document.append("\\author{Shoko-official}")
    latex_document.append("\\date{\\today}")
    latex_document.append("")
    latex_document.append("\\begin{document}")
    latex_document.append("")
    latex_document.append("\\maketitle")
    latex_document.append("")
    
    # Append abstract and sections
    for filename in SECTION_FILES_ORDER:
        filepath = SECTIONS_DIR / filename
        if not filepath.is_file():
            raise FileNotFoundError(f"Section file not found: {filepath}")
            
        section_text = filepath.read_text(encoding="utf-8")
        
        # Format for latex
        latex_section = clean_markdown_for_latex(section_text)
        
        if filename == "abstract.md":
            # Extract content from Abstract for standard abstract env
            latex_section = latex_section.replace("\\section{Abstract}", "")
            latex_document.append("\\begin{abstract}")
            latex_document.append(latex_section.strip())
            latex_document.append("\\end{abstract}")
            latex_document.append("")
        else:
            latex_document.append(latex_section)
            latex_document.append("")
            
    # Add bibliography
    latex_document.append("\\bibliographystyle{plain}")
    latex_document.append("\\bibliography{bibliography}")
    latex_document.append("")
    latex_document.append("\\end{document}")
    
    # Write output tex file
    output_tex_path = DIST_DIR / "paper.tex"
    output_tex_path.write_text("\n".join(latex_document), encoding="utf-8")
    print(f"Generated LaTeX source at {output_tex_path}")
    
    # Copy bibliography
    bib_src = REFERENCES_DIR / "bibliography.bib"
    bib_dst = DIST_DIR / "bibliography.bib"
    if bib_src.is_file():
        shutil.copy2(bib_src, bib_dst)
        print(f"Copied bibliography to {bib_dst}")
    else:
        print(f"Warning: Bibliography file not found at {bib_src}")
        
    # Copy figures if they exist
    fig_src = FIGURES_DIR / "kv_cache_memory_curve.png"
    fig_dst = DIST_DIR / "kv_cache_memory_curve.png"
    if fig_src.is_file():
        shutil.copy2(fig_src, fig_dst)
        print(f"Copied figure to {fig_dst}")
    else:
        print(f"Warning: Figure not found at {fig_src}")
        
    fig_obs_src = FIGURES_DIR / "observability_latency_overhead.png"
    fig_obs_dst = DIST_DIR / "observability_latency_overhead.png"
    if fig_obs_src.is_file():
        shutil.copy2(fig_obs_src, fig_obs_dst)
        print(f"Copied figure to {fig_obs_dst}")
    else:
        print(f"Warning: Figure not found at {fig_obs_src}")
        
    print("LaTeX source generation complete.")

def package_arxiv() -> None:
    print("Packaging submission for arXiv...")
    
    # Ensure compile was run
    output_tex_path = DIST_DIR / "paper.tex"
    if not output_tex_path.is_file():
        raise FileNotFoundError(f"LaTeX file not found at {output_tex_path}. Please run compile first.")
        
    zip_path = DIST_DIR / "arxiv_submission.zip"
    
    # Files to include in zip
    files_to_zip = [
        "paper.tex",
        "bibliography.bib",
        "kv_cache_memory_curve.png",
        "observability_latency_overhead.png"
    ]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for filename in files_to_zip:
            filepath = DIST_DIR / filename
            if filepath.is_file():
                zip_file.write(filepath, arcname=filename)
                print(f"Added {filename} to package.")
            else:
                print(f"Warning: File {filename} not found in dist, skipping.")
                
    print(f"arXiv package created at {zip_path}")

def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts/compile_paper.py {compile|package}")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    if command == "compile":
        compile_latex()
    elif command == "package":
        compile_latex()
        package_arxiv()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
