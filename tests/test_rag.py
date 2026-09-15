from src.rag import build_retrieval_context
from src.retriever import Document, TfidfRetriever


def test_build_retrieval_context():
    retriever = TfidfRetriever()

    retriever.add_documents(
        [
            Document(
                doc_id="health",
                text="AI can analyze medical images.",
                metadata={"category": "health"},
            ),
            Document(
                doc_id="education",
                text="AI tutors can help students learn.",
                metadata={"category": "education"},
            ),
        ]
    )

    context = build_retrieval_context(
        retriever,
        "medical images",
        top_k=1,
    )

    assert "health" in context
    assert "medical images" in context
    assert "Relevance:" in context


def test_empty_retrieval_context():
    retriever = TfidfRetriever()

    context = build_retrieval_context(
        retriever,
        "test query",
    )

    assert context == "No relevant documents were found."
