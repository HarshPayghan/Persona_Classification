import os
from pydoc import text
from urllib import response

import chromadb
from pypdf import PdfReader
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K_RESULTS
)


class LocalRAGPipeline:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.chroma_client = chromadb.PersistentClient(
            path=CHROMA_DB_PATH
        )

        self.collection = self.chroma_client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    def get_embedding(self, text: str):
        """
        Generate Gemini embedding.
        """

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values

    def read_pdf(self, filepath):
        try:
            reader = PdfReader(filepath)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text

        except Exception as e:
            print(f"Error reading PDF {filepath}: {e}")
            return ""

    def load_document(self, filepath):
        """
        Load txt/md/pdf file.
        """

        extension = os.path.splitext(filepath)[1].lower()

        if extension == ".pdf":
            return self.read_pdf(filepath)

        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def chunk_text(self, text):
        """
        Split large text into chunks.
        """

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        return splitter.split_text(text)

    def ingest_document(self, filepath):
        """
        Add a document into vector database.
        """

        filename = os.path.basename(filepath)

        print(f"Ingesting {filename}...")

        text = self.load_document(filepath)

        if not text.strip():
            print(f"Skipping empty document: {filepath}")
            return

        chunks = self.chunk_text(text)

        for idx, chunk in enumerate(chunks):

            embedding = self.get_embedding(chunk)

            chunk_id = f"{filename}_{idx}"

            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                {
                    "source": filename,
                    "chunk_index": idx
                }
            ]
        )

        print(f"Stored {len(chunks)} chunks.")

    def ingest_data_folder(self, folder_path="data"):
        """
        Index all files in data folder.
        """

        for file in os.listdir(folder_path):

            if file.endswith(
                (
                    ".txt",
                    ".md",
                    ".pdf"
                )
            ):
                filepath = os.path.join(
                    folder_path,
                    file
                )

                self.ingest_document(filepath)

    def retrieve_context(
        self,
        query,
        top_k=TOP_K_RESULTS
    ):
        """
        Retrieve top-k relevant chunks.
        """
        
        query_embedding = self.get_embedding(query)

        results = self.collection.query(
        query_embeddings=[query_embedding],
        n_results=1
        )
        retrieved_chunks = []

        if results["documents"]:

            for i in range(
                len(results["documents"][0])
            ):

                score = 1.0

                if (
                    "distances" in results
                    and results["distances"]
                ):
                    score = (
                        1.0
                        - results["distances"][0][i]
                    )

                retrieved_chunks.append(
                    {
                        "text":
                        results["documents"][0][i],

                        "source":
                        results["metadatas"][0][i]["source"],

                        "score":
                        round(score, 4)
                    }
                )

        return retrieved_chunks


if __name__ == "__main__":

    rag = LocalRAGPipeline()

    rag.ingest_data_folder()

    query = "How can I reset my password?"

    results = rag.retrieve_context(query)

    print("\nRetrieved Context:\n")

    for item in results:
        print(item)
        print("-" * 50)