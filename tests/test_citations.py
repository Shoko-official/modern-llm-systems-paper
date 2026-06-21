import sys
import unittest
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_repo import validate_citations

class TestCitationsValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp_dir.name)
        
        # Create standard layout stubs
        (self.root_path / "references").mkdir(parents=True, exist_ok=True)
        (self.root_path / "sections").mkdir(parents=True, exist_ok=True)
        (self.root_path / "paper").mkdir(parents=True, exist_ok=True)
        
        # Create default empty files
        (self.root_path / "paper" / "main.md").write_text("", encoding="utf-8")
        
        # We need to mock ledger directory
        self.ledger_dir = self.root_path.parent / "llm-systems-research-ledger"
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        (self.ledger_dir / "claims").mkdir(parents=True, exist_ok=True)
        (self.ledger_dir / "sources").mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()
        # Clean up ledger dir if created
        try:
            import shutil
            shutil.rmtree(self.ledger_dir)
        except Exception:
            pass

    def write_index(self, content: str) -> None:
        (self.root_path / "references" / "index.md").write_text(content, encoding="utf-8")

    def test_valid_empty_table(self) -> None:
        # No entries, no section files cited. Should pass.
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
""")
        validate_citations(self.root_path)

    def test_duplicate_key_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | N/A | ready_for_bibliography | None |
| key-1 | source-2 | claim-2 | N/A | ready_for_bibliography | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("Duplicate citation key 'key-1'", str(cm.exception))

    def test_invalid_key_format_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key@1 | source-1 | claim-1 | N/A | ready_for_bibliography | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("Invalid Citation Key format 'key@1'", str(cm.exception))

    def test_invalid_state_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | N/A | invalid_state | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("Invalid state 'invalid_state'", str(cm.exception))

    def test_ready_with_detail_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | N/A | ready_for_bibliography | missing page number |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("marked 'ready_for_bibliography' but has missing citation detail", str(cm.exception))

    def test_missing_detail_without_detail_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | N/A | missing_citation_detail | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("marked 'missing_citation_detail' but lacks specific detail", str(cm.exception))

    def test_target_section_not_exist_fails(self) -> None:
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/nonexistent.md | ready_for_bibliography | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("does not exist", str(cm.exception))

    def test_target_exists_but_not_cited_fails(self) -> None:
        target_file = self.root_path / "sections" / "introduction.md"
        target_file.write_text("No citation here", encoding="utf-8")
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-1 | claim-1 | sections/introduction.md | ready_for_bibliography | None |
""")
        with self.assertRaises(SystemExit) as cm:
            validate_citations(self.root_path)
        self.assertIn("lists target 'sections/introduction.md' but is not cited in that file", str(cm.exception))

    def test_valid_citation_flow(self) -> None:
        target_file = self.root_path / "sections" / "introduction.md"
        target_file.write_text("Factual sentence [@key-1].", encoding="utf-8")
        self.write_index("""
## Current Entries

| Citation Key | Ledger Source ID | Ledger Claim ID | Paper Section Target | Readiness State | Missing Citation Detail |
|---|---|---|---|---|---|
| key-1 | source-attention-2017 | claim-attention-parallelism | sections/introduction.md | ready_for_bibliography | None |
""")
        # Mocking ledger files to test alignment
        (self.ledger_dir / "claims" / "claim-attention-parallelism.md").write_text("Supported claim.", encoding="utf-8")
        (self.ledger_dir / "sources" / "source-attention-2017.md").write_text("Source details.", encoding="utf-8")
        
        validate_citations(self.root_path)

if __name__ == "__main__":
    unittest.main()
