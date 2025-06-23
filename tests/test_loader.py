from folder_organizer.loader import load_documents


def test_load_documents(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")
    docs = load_documents(str(file))
    assert docs
    assert docs[0].page_content == "hello"
