from folder_organizer.loader import load_documents


def test_load_documents(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    docs = load_documents(str(file))
    assert docs
    assert docs[0].page_content == "hello"


def test_load_documents_skips_unknown(tmp_path):
    """Files with unsupported extensions should be ignored."""
    file = tmp_path / "data.bin"
    file.write_bytes(b"\x00\x01")
    docs = load_documents(str(file))
    assert docs == []


def test_load_documents_skips_zip(tmp_path):
    """Archive files should be ignored."""
    file = tmp_path / "data.zip"
    file.write_bytes(b"PK\x03\x04")
    docs = load_documents(str(file))
    assert docs == []
