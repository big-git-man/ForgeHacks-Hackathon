from src.retriever import TfidfRetriever


def build_retrieval_context(
    retriever: TfidfRetriever,
    query: str,
    top_k: int = 3,
) -> str:
    results = retriever.retrieve(query, top_k=top_k)

    if not results:
        return "No relevant documents were found."

    sections = []

    for document, score in results:
        sections.append(
            f"Document ID: {document.doc_id}\n"
            f"Relevance: {score:.3f}\n"
            f"Content: {document.text}"
        )

    return "\n\n".join(sections)
