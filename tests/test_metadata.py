from folder_organizer.metadata import generate_metadata


def test_generate_metadata(tmp_path):
    meta = generate_metadata("/tmp", "summary", ["a.txt"])
    assert meta["path"] == "/tmp"
    assert meta["summary"] == "summary"
    assert "created_at" in meta
