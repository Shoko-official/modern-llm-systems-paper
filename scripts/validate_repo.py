from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "Makefile",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/paper_task.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
    "figures/README.md",
    "figures/generate_figures.py",
    "figures/kv_cache_memory_curve.png",
    "paper/main.md",
    "paper/README.md",
    "references/bibliography.bib",
    "references/index.md",
    "references/README.md",
    "scripts/figures/README.md",
    "sections/abstract.md",
    "sections/agents-and-tool-use.md",
    "sections/conclusion.md",
    "sections/decision-matrix.md",
    "sections/evaluation.md",
    "sections/inference-and-serving.md",
    "sections/introduction.md",
    "sections/observability.md",
    "sections/retrieval-and-memory.md",
    "sections/README.md",
    "sections/security-and-governance.md",
    "sections/system-layers.md",
    "sections/training-and-adaptation.md",
    "tests/README.md",
    "tests/test_citations.py",
]

REQUIRED_DIRECTORIES = [
    ".github",
    ".github/ISSUE_TEMPLATE",
    ".github/workflows",
    "figures",
    "paper",
    "references",
    "scripts",
    "scripts/figures",
    "sections",
    "tests",
]

FOUNDATION_MARKERS = {
    "paper/README.md": [
        "# Paper",
        "## Expected Role",
        "## Repository Boundary",
        "## Current Limits",
    ],
    "paper/main.md": [
        "# Modern LLM Systems 2026",
        "## Assembly Inputs",
        "## Current Status",
        "not a scientific draft",
        "No scientific prose",
    ],
    "sections/README.md": [
        "# Sections",
        "## Expected Role",
        "## Section Inventory",
        "## Current Limits",
        "| Section | Purpose | Draft status |",
        "| Abstract |",
        "| Conclusion |",
    ],
    "references/README.md": [
        "# References",
        "## Expected Role",
        "## Citation Handoff",
        "## Readiness States",
        "## Paper Drafting Rules",
        "## Current Limits",
        "missing_evidence",
        "missing_citation_detail",
    ],
    "references/index.md": [
        "# Reference Index",
        "## Future Entry Shape",
        "## Current Entries",
        "| Citation Key | Ledger Source ID |",
    ],
    "figures/README.md": [
        "# Figures",
        "## Expected Role",
        "## Current Limits",
        "Mermaid",
        "Python-generated images",
    ],
}

SECTION_STUB_FILES = [
    "sections/abstract.md",
    "sections/agents-and-tool-use.md",
    "sections/conclusion.md",
    "sections/decision-matrix.md",
    "sections/evaluation.md",
    "sections/inference-and-serving.md",
    "sections/introduction.md",
    "sections/observability.md",
    "sections/retrieval-and-memory.md",
    "sections/security-and-governance.md",
    "sections/system-layers.md",
    "sections/training-and-adaptation.md",
]

SECRET_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"AKIA[0-9A-Z]{16}",
        r"gho_[A-Za-z0-9_]+",
        r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----",
        r"(?i)\b(password|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}",
    ]
]


def fail(message: str) -> None:
    raise SystemExit(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_text_files() -> list[Path]:
    excluded_parts = {".git", "__pycache__"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if excluded_parts.intersection(path.parts):
            continue
        if path.suffix.lower() in {".md", ".yml", ".yaml", ".py", ""}:
            files.append(path)
    return files


def validate_required_paths() -> None:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    missing_dirs = [path for path in REQUIRED_DIRECTORIES if not (ROOT / path).is_dir()]
    if missing_files or missing_dirs:
        details = []
        if missing_files:
            details.append("missing files: " + ", ".join(missing_files))
        if missing_dirs:
            details.append("missing directories: " + ", ".join(missing_dirs))
        fail("; ".join(details))


def validate_foundation_files() -> None:
    for relative_path, markers in FOUNDATION_MARKERS.items():
        text = read_text(ROOT / relative_path)
        missing_markers = [marker for marker in markers if marker not in text]
        if missing_markers:
            fail(
                f"{relative_path} is missing expected marker(s): "
                + ", ".join(missing_markers)
            )


def validate_section_stubs() -> None:
    required_markers = ["Purpose:", "Evidence requirement:"]
    for relative_path in SECTION_STUB_FILES:
        text = read_text(ROOT / relative_path)
        if "Draft status: Not drafted." not in text and "Draft status: Drafted." not in text:
            fail(f"{relative_path} is missing Draft status marker ('Not drafted.' or 'Drafted.')")
        missing_markers = [marker for marker in required_markers if marker not in text]
        if missing_markers:
            fail(
                f"{relative_path} is missing expected marker(s): "
                + ", ".join(missing_markers)
            )


def lint_text() -> None:
    for path in iter_text_files():
        text = read_text(path)
        relative = path.relative_to(ROOT)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible secret in {relative}: {pattern.pattern}")


def validate_citations(root_path: Path = ROOT) -> None:
    index_path = root_path / "references" / "index.md"
    if not index_path.is_file():
        fail("references/index.md is missing")
    
    text = read_text(index_path)
    lines = text.splitlines()
    
    citation_keys = set()
    citation_records = []
    
    allowed_states = {"ready_for_bibliography", "missing_citation_detail", "missing_evidence", "blocked"}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("|") and i + 1 < len(lines) and lines[i+1].startswith("|---"):
            headers = [h.strip().lower() for h in line.split("|")[1:-1]]
            
            key_idx = -1
            source_idx = -1
            claim_idx = -1
            section_idx = -1
            state_idx = -1
            detail_idx = -1
            
            for idx, h in enumerate(headers):
                if "citation key" in h or "key" in h:
                    key_idx = idx
                elif "source" in h:
                    source_idx = idx
                elif "claim" in h:
                    claim_idx = idx
                elif "section" in h:
                    section_idx = idx
                elif "state" in h or "status" in h:
                    state_idx = idx
                elif "detail" in h:
                    detail_idx = idx
            
            if key_idx != -1:
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    row_line = lines[j]
                    row_parts = [p.strip() for p in row_line.split("|")[1:-1]]
                    
                    if len(row_parts) > key_idx:
                        key = row_parts[key_idx].replace("`", "")
                        if key and not key.startswith("---") and key.lower() != "citation key":
                            if key in citation_keys:
                                fail(f"Duplicate citation key '{key}' in references/index.md")
                            citation_keys.add(key)
                            
                            source_id = row_parts[source_idx].replace("`", "") if source_idx != -1 else ""
                            claim_id = row_parts[claim_idx].replace("`", "") if claim_idx != -1 else ""
                            section_target = row_parts[section_idx].replace("`", "") if section_idx != -1 else ""
                            state = row_parts[state_idx].replace("`", "") if state_idx != -1 else ""
                            detail = row_parts[detail_idx].replace("`", "") if detail_idx != -1 else ""
                            
                            citation_records.append({
                                "key": key,
                                "source_id": source_id,
                                "claim_id": claim_id,
                                "section_target": section_target,
                                "state": state,
                                "detail": detail
                            })
                    j += 1
                i = j
            else:
                i += 1
        else:
            i += 1

    # Check inline citations reference existing bibliography keys
    files_to_check = [root_path / f for f in SECTION_STUB_FILES] + [root_path / "paper" / "main.md"]
    inline_citations_found = {}
    
    for path in files_to_check:
        if not path.is_file():
            continue
        content = read_text(path)
        inline_citations = re.findall(r"\[@([a-zA-Z0-9_\-]+)\]", content)
        for key in inline_citations:
            if key not in citation_keys:
                fail(f"Inline citation [@{key}] in {path.relative_to(root_path)} does not match any entry in references/index.md")
            if key not in inline_citations_found:
                inline_citations_found[key] = []
            inline_citations_found[key].append(path)

    # Check ledger alignment
    ledger_dir = root_path.parent / "llm-systems-research-ledger"
    ledger_claims_dir = ledger_dir / "claims"
    ledger_sources_dir = ledger_dir / "sources"
    
    has_ledger_claims = False
    if ledger_claims_dir.is_dir():
        claim_files = [p for p in ledger_claims_dir.glob("*.md") if p.name.lower() != "readme.md"]
        if claim_files:
            has_ledger_claims = True
            
    has_ledger_sources = False
    if ledger_sources_dir.is_dir():
        source_files = [p for p in ledger_sources_dir.glob("*.md") if p.name.lower() != "readme.md"]
        if source_files:
            has_ledger_sources = True
            
    for record in citation_records:
        key = record["key"]
        source_id = record["source_id"]
        claim_id = record["claim_id"]
        section_target = record["section_target"]
        state = record["state"]
        detail = record["detail"]
        
        if not re.match(r"^[a-zA-Z0-9_\-]+$", key):
            fail(f"Invalid Citation Key format '{key}' in references/index.md")
            
        if state and state not in allowed_states:
            fail(f"Invalid state '{state}' for citation key '{key}' in references/index.md")
            
        if state == "ready_for_bibliography":
            if detail and detail.lower() not in {"none", "n/a", ""}:
                fail(f"Citation key '{key}' is marked 'ready_for_bibliography' but has missing citation detail: '{detail}'")
        elif state == "missing_citation_detail":
            if not detail or detail.lower() in {"none", "n/a", ""}:
                fail(f"Citation key '{key}' is marked 'missing_citation_detail' but lacks specific detail in references/index.md")
                
        if section_target and section_target != "N/A":
            target_path = root_path / section_target
            if not target_path.is_file():
                fail(f"Section target '{section_target}' for citation key '{key}' does not exist")
            files_used = inline_citations_found.get(key, [])
            rel_files_used = [str(p.relative_to(root_path)).replace("\\", "/") for p in files_used]
            if section_target not in rel_files_used:
                fail(f"Citation key '{key}' lists target '{section_target}' but is not cited in that file")
            
        if claim_id and claim_id != "N/A":
            if not re.match(r"^claim-[A-Za-z0-9_\-]+$", claim_id):
                fail(f"Invalid Claim ID format '{claim_id}' for citation key '{key}' in references/index.md")
            if has_ledger_claims:
                claim_file = ledger_claims_dir / f"{claim_id}.md"
                if not claim_file.is_file():
                    fail(f"Referenced claim file {claim_id}.md does not exist in ledger repository")
                    
        if source_id and source_id != "N/A":
            if not re.match(r"^source-[A-Za-z0-9_\-]+$", source_id):
                fail(f"Invalid Source ID format '{source_id}' for citation key '{key}' in references/index.md")
            if has_ledger_sources:
                source_file = ledger_sources_dir / f"{source_id}.md"
                if not source_file.is_file():
                    fail(f"Referenced source file {source_id}.md does not exist in ledger repository")


def validate_figure_generation() -> None:
    output_file = ROOT / "figures" / "kv_cache_memory_curve.png"
    if output_file.is_file():
        output_file.unlink()
        
    sys.path.insert(0, str(ROOT / "figures"))
    try:
        import generate_figures
        # Reload if already imported
        import importlib
        importlib.reload(generate_figures)
        generate_figures.main()
    except Exception as e:
        fail(f"Failed to execute figures/generate_figures.py: {e}")
    finally:
        if str(ROOT / "figures") in sys.path:
            sys.path.remove(str(ROOT / "figures"))
        
    if not output_file.is_file():
        fail("figures/generate_figures.py failed to produce figures/kv_cache_memory_curve.png")


def validate_latex_compilation() -> None:
    try:
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import compile_paper
        import importlib
        importlib.reload(compile_paper)
        compile_paper.compile_latex()
        compile_paper.package_arxiv()
    except Exception as e:
        fail(f"LaTeX compile or packaging failed: {e}")
    finally:
        if str(ROOT / "scripts") in sys.path:
            sys.path.remove(str(ROOT / "scripts"))


def run_validate() -> None:
    validate_required_paths()
    validate_foundation_files()
    validate_section_stubs()
    validate_citations()
    validate_figure_generation()
    validate_latex_compilation()


def run_lint() -> None:
    lint_text()


def run_unit_tests() -> None:
    import unittest
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        fail("Unit tests failed.")


def run_test() -> None:
    run_validate()
    run_lint()
    run_unit_tests()


def main(argv: list[str]) -> int:
    if len(argv) == 1:
        command = "test"
    elif len(argv) == 2 and argv[1] in {"validate", "lint", "test"}:
        command = argv[1]
    else:
        print("usage: validate_repo.py {validate|lint|test}", file=sys.stderr)
        return 2

    if command == "validate":
        run_validate()
    elif command == "lint":
        run_lint()
    else:
        run_test()

    print(f"{command} ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
