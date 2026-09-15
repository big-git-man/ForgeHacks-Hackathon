from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Document:
    doc_id: str
    text: str
    metadata: dict


class TfidfRetriever:
    def __init__(self):
        self.documents: list[Document] = []
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )
        self.matrix = None

    def add_documents(self, documents: list[Document]) -> None:
        self.documents.extend(documents)

        texts = [document.text for document in self.documents]

        if texts:
            self.matrix = self.vectorizer.fit_transform(texts)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[tuple[Document, float]]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if not self.documents or self.matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(
            query_vector,
            self.matrix,
        )[0]

        ranked_indices = scores.argsort()[::-1][:top_k]

        return [
            (
                self.documents[index],
                float(scores[index]),
            )
            for index in ranked_indices
        ]
