from src.retriever import Document, TfidfRetriever


def test_retriever_returns_relevant_documents():
    retriever = TfidfRetriever()

    documents = [
        Document(
            doc_id="health",
            text="AI can help doctors analyze medical images.",
            metadata={"category": "health"},
        ),
        Document(
            doc_id="education",
            text="AI tutors can help students learn mathematics.",
            metadata={"category": "education"},
        ),
        Document(
            doc_id="climate",
            text="Machine learning can help predict climate patterns.",
            metadata={"category": "climate"},
        ),
    ]

    retriever.add_documents(documents)

    results = retriever.retrieve(
        "medical images and doctors",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0][0].doc_id == "health"
    assert results[0][1] > 0


def test_empty_query_is_rejected():
    retriever = TfidfRetriever()

    try:
        retriever.retrieve("")
        assert False
    except ValueError as exc:
        assert "empty" in str(exc).lower()


def test_empty_retriever_returns_no_results():
    retriever = TfidfRetriever()

    results = retriever.retrieve(
        "test query"
    )

    assert results == []
