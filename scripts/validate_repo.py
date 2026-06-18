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
    "paper/main.md",
    "paper/README.md",
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
        "No reference entries yet.",
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
    required_markers = ["Draft status: Not drafted.", "Purpose:", "Evidence requirement:"]
    for relative_path in SECTION_STUB_FILES:
        text = read_text(ROOT / relative_path)
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


def run_validate() -> None:
    validate_required_paths()
    validate_foundation_files()
    validate_section_stubs()


def run_lint() -> None:
    lint_text()


def run_test() -> None:
    run_validate()
    run_lint()


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
