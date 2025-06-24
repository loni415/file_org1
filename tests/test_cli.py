import sys
from folder_organizer import cli


def test_cli_accept_after_regenerate(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["prog", "--path", str(tmp_path)])
    monkeypatch.setattr(cli, "load_documents", lambda path: ["doc"])
    summaries = iter(["s1", "s2"])
    monkeypatch.setattr(cli, "summarize_documents", lambda docs: next(summaries))
    prompts = iter(["r", "a"])
    monkeypatch.setattr(cli, "prompt", lambda msg, default=None: next(prompts))
    captured = {}

    def fake_generate(path, summary, files):
        captured["summary"] = summary
        return {}

    monkeypatch.setattr(cli, "generate_metadata", fake_generate)
    monkeypatch.setattr(cli, "list_files", lambda path: [])

    cli.main()
    assert captured["summary"] == "s2"


def test_cli_edit_cancel(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["prog", "--path", str(tmp_path)])
    monkeypatch.setattr(cli, "load_documents", lambda path: ["doc"])
    monkeypatch.setattr(cli, "summarize_documents", lambda docs: "orig")
    prompts = iter(["e", "edited", "c"])
    monkeypatch.setattr(cli, "prompt", lambda msg, default=None: next(prompts))
    calls = []

    def fake_generate(path, summary, files):
        calls.append(True)
        return {}

    monkeypatch.setattr(cli, "generate_metadata", fake_generate)
    monkeypatch.setattr(cli, "list_files", lambda path: [])

    cli.main()
    assert not calls
