from folder_organizer.summarizer import summarize_documents
from folder_organizer.loader import load_documents


class FakeChain:
    def invoke(self, params):
        return {"output_text": "summary"}



def test_summarize_documents(monkeypatch, tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello world")
    docs = load_documents(str(file))

    monkeypatch.setattr(
        "folder_organizer.summarizer.load_summarize_chain",
        lambda llm, chain_type=None: FakeChain(),
    )
    monkeypatch.setattr(
        "folder_organizer.summarizer.ChatOllama",
        lambda model=None: None,
    )

    summary = summarize_documents(docs)
    assert summary == "summary"
