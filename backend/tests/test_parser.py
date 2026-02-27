import unittest

from app.utils.parser import detect_document_code, detect_revision, revision_to_order


class ParserTests(unittest.TestCase):
    def test_detect_document_code_from_text(self):
        text = "Documento DE-5275.00-2000-700-E6G-104"
        self.assertEqual(detect_document_code(text, "arquivo.pdf"), "DE-5275.00-2000-700-E6G-104")

    def test_detect_revision(self):
        self.assertEqual(detect_revision("REV B", "arquivo.pdf"), "B")
        self.assertEqual(detect_revision("sem revisão", "arquivo.pdf"), "0")

    def test_revision_order(self):
        self.assertEqual(revision_to_order("0"), 0)
        self.assertEqual(revision_to_order("5"), 5)
        self.assertEqual(revision_to_order("A"), 100)
        self.assertEqual(revision_to_order("C"), 102)


if __name__ == "__main__":
    unittest.main()
