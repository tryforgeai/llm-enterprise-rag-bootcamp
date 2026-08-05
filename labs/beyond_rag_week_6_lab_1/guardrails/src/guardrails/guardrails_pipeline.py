# Import required modules
from pathlib import Path
import sqlite3
import time
from rich import print as rprint
from guardrails import config

# rag-to-riches imports
from rag_to_riches.corpus.animals import Animals
from rag_to_riches.vectordb.embedded_vectordb import EmbeddedVectorDB
from rag_to_riches.vectordb.embedder import SimpleTextEmbedder

# gibberish-detector imports
from gibberish_detector.gibberish_detector import GibberishGuardrail

# toxicity-detector imports
from toxicity_detector.toxicity_detector import ToxicityGuardrail

# query-normalization imports
from query_normalization.query_normalization import TwoStageQueryNormalization

# relevance-detector imports
from rel_detector.classification.relevance_detector import RelevanceDetector

# context-detection imports
from context_detection.context_detection import ContextNeedDetector

# conversation-summarizer imports
from conversation_summarizer.summarizer import abstractive_summarize_conversation

# query-rewriter imports
from query_rewriter.rewriter import rewrite_query_with_context

REWRITING_MODEL = "llama3.2:latest"
print("Modules imported successfully!")
print("Current working directory:", Path.cwd())

print("Initializing Shared Components")
print("=" * 60)

# Initialize Vector Database (shared instance)
print("Initializing Vector Database (Qdrant)...")
vector_db = EmbeddedVectorDB()
print("     Vector database connected and ready for reuse")

# Initialize Text Embedder (shared instance)  
print("\n       Initializing Text Embedder (Sentence Transformers)...")
embedder = SimpleTextEmbedder(model_name="sentence-transformers/all-MiniLM-L6-v2")
print(f"     Embedder loaded: {embedder.model_name}")
print(f"     Vector dimensions: {embedder.get_vector_size()}")
print(f"     Distance metric: {embedder.get_distance_metric()}")

# 📚 Load and Index Animal Quotes Using Shared Components
print("  Creating Animals corpus loader using shared components...")
animals = Animals(
    vector_db=vector_db,  # Reusing shared vector_db instance
    embedder=embedder,    # Reusing shared embedder instance
)
animals.recreate_collection()
# Load and index all quotes in one call
animals.load_and_index(config["animals"]["jsonl_path"])

# Initialize Guardrails and Models
gibberish_guardrail = GibberishGuardrail()
toxicity_guardrail = ToxicityGuardrail()
query_normalizer = TwoStageQueryNormalization()
relevance_detector = RelevanceDetector()
relevance_detector.load_model(model_path=config["relevance_detector"]["model_path"])
context_detector = ContextNeedDetector()

# --- Gibberish Detector ---
def is_gibberish(query:str):
    return gibberish_guardrail.is_gibberish(query)

# --- Toxicity Detector ---
def is_toxic(query:str):
    return toxicity_guardrail.is_toxic(query)

# --- Query Normalization: Spelling, Grammar, etc.
def normalize_query(query: str) -> str:
    """
    Normalize the input query using the QueryNormalization class.
    Returns the normalized query string.
    """
    # Use the main normalization method (grammar correction + basic normalization)
    return query_normalizer.normalize(query)['final_normalized']

# --- Relevance Detection Model ---
def is_relevant(text: str) -> bool:
    """
    Uses the loaded RelevanceDetector to determine if the input text is relevant.
    Returns True if relevant, False otherwise.
    """
    result = relevance_detector.predict(text)
    return result["is_relevant"]


# --- Contextual Query Detection Example Integration ---
def needs_contextualization(query: str) -> bool:
    """Simplified context detection using only LLM assessment"""
    result = context_detector.needs_contextualization(query)
    rprint(result)
    return (result['needs_context'], result['context_type'])

# --- Retrieval for context ---
def retrieve_with_vector_search(query: str, limit: int = 4):
    """Use your existing Animals corpus for vector-based retrieval"""
    try:
        results = animals.search(query, limit=limit)
        return results
    except Exception as e:
        print(f"⚠️  Vector search error: {e}")
        return []

def main():
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect("conversation_history.db")
    cursor = conn.cursor()
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT NOT NULL,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    print("Welcome to the Animal Wisdom Chat! (type 'exit' to quit)\n")
    while True:
        user_query = input("You: ").strip()
        if user_query.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        t0 = time.perf_counter()
        if is_gibberish(user_query):
            print(f"User Query is gibberish  [{time.perf_counter() - t0:.3f}s]")
            continue
        print(f"  [gibberish check] {time.perf_counter() - t0:.3f}s")

        t0 = time.perf_counter()
        if is_toxic(user_query):
            print(f"User Query is toxic  [{time.perf_counter() - t0:.3f}s]")
            continue
        print(f"  [toxicity check] {time.perf_counter() - t0:.3f}s")

        t0 = time.perf_counter()
        if not is_relevant(user_query):
            print(f"User Query is not relevant  [{time.perf_counter() - t0:.3f}s]")
            continue
        print(f"  [relevance check] {time.perf_counter() - t0:.3f}s")

        t0 = time.perf_counter()
        normalized = normalize_query(user_query)
        print(f"  [normalize query] {time.perf_counter() - t0:.3f}s")

        t0 = time.perf_counter()
        need_context, context_type = needs_contextualization(normalized)
        print(f"  [context detection] {time.perf_counter() - t0:.3f}s")
        print(f"Needs context: {need_context}")
        print(f"Context type: {context_type}")
        final_query = normalized

        if need_context:
            t0 = time.perf_counter()
            if str(context_type) == "ContextType.CONVERSATIONAL":
                summary = abstractive_summarize_conversation() #"Abstractive summarization of conversation would take place here."
                final_query = rewrite_query_with_context(query=final_query, summary=summary)
            else:
                retrieved = retrieve_with_vector_search(final_query)
                final_query = rewrite_query_with_context(query=final_query, retrievals=retrieved)
                # response = "Retrieval to get context would take place here."
            print(f"  [context + rewrite] {time.perf_counter() - t0:.3f}s")

        # Use the Animals corpus to perform a full RAG pipeline (retrieval + LLM generation)
        # Use simple response type to avoid Instructor API issues
        t0 = time.perf_counter()
        rag_result = animals.rag(final_query, response_type="simple")
        print(f"  [RAG] {time.perf_counter() - t0:.3f}s")
        # Extract the actual response text from the RAG result
        if isinstance(rag_result, dict) and 'llm_response' in rag_result:
            response = rag_result['llm_response']
        else:
            response = str(rag_result)

        print("="*60)
        print(f"Bot: {response}\n\n")
        print("="*60)

        # Store only valid query and response
        cursor.execute(
            "INSERT INTO conversation (user_query, response) VALUES (?, ?)",
            (user_query, response)
        )
        conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
    vector_db.client.close()
