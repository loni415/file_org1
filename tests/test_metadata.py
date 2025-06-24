from folder_organizer.metadata import generate_metadata


def test_generate_metadata(tmp_path):
    meta = generate_metadata("/tmp", "summary", ["a.txt"])
    assert meta["path"] == "/tmp"
    assert meta["summary"] == "summary"
    # tags are required by the schema
    assert "tags" in meta
    assert "created_at" in meta
