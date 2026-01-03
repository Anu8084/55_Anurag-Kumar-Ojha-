from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI


# -----------------------------
# Simple Python Text Chunker
# -----------------------------
def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks


# -----------------------------
# Create Vector Store (FREE)
# -----------------------------
def create_vectorstore(text: str):
    chunks = chunk_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(chunks, embeddings)
    return vectorstore


# -----------------------------
# Ask Question using Gemini
# -----------------------------
def ask_question(vectorstore, query: str, system_prompt: str):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "Not found in the document."

    context = "\n".join(doc.page_content for doc in docs)

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # free-tier friendly
        temperature=0.3
    )

    prompt = f"""
{system_prompt}

Answer ONLY using the context below.
If the answer is not present, say "Not found in the document."

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content
