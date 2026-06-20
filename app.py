import streamlit as st

from src.classifier import PersonaClassifier
from src.rag_pipeline import LocalRAGPipeline
from src.generator import AdaptiveResponseGenerator

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="Persona Adaptive Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Persona-Adaptive Customer Support Agent")

st.markdown(
    "Customer Support Agent powered by Gemini + RAG + ChromaDB"
)

# -----------------------------
# Initialize Components
# -----------------------------

@st.cache_resource
def load_components():

    classifier = PersonaClassifier()

    rag = LocalRAGPipeline()

    generator = AdaptiveResponseGenerator()

    return classifier, rag, generator


classifier, rag, generator = load_components()

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Knowledge Base")

if st.sidebar.button("Index Documents"):

    with st.spinner("Indexing documents..."):

        rag.ingest_data_folder("data")

    st.sidebar.success(
        "Documents indexed successfully."
    )

# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Chat History
# -----------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------

user_query = st.chat_input(
    "Ask your support question..."
)

if user_query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )

    with st.chat_message("user"):

        st.markdown(user_query)

    with st.spinner("Processing..."):

        # ----------------------
        # Persona Classification
        # ----------------------

        persona_result = classifier.classify(
            user_query
        )

        persona = persona_result["persona"]

        # ----------------------
        # Context Retrieval
        # ----------------------

        context_chunks = rag.retrieve_context(
            user_query
        )

        # ----------------------
        # Response Generation
        # ----------------------

        result = generator.generate_response(
            user_query=user_query,
            persona=persona,
            context_chunks=context_chunks
        )

        response_text = result["response"]

    with st.chat_message("assistant"):

        st.markdown(response_text)

        st.divider()

        st.subheader("Detected Persona")

        st.write(persona)

        st.subheader("Classification Confidence")

        st.write(
            persona_result["confidence"]
        )

        st.subheader("Reasoning")

        st.write(
            persona_result["reasoning"]
        )

        if result["escalated"]:

            st.error(
                "Conversation Escalated"
            )

            st.subheader(
                "Human Handoff JSON"
            )

            st.code(
                result["handoff"],
                language="json"
            )

        else:

            st.success(
                "Resolved Automatically"
            )

            st.subheader(
                "Retrieved Context"
            )

            for chunk in context_chunks:

                with st.expander(
                    f"{chunk['source']} "
                    f"(Score: {chunk['score']})"
                ):

                    st.write(
                        chunk["text"]
                    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )