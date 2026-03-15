from langchain_core.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert assistant.

Answer the question using ONLY the provided context.

If the answer is not present, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
)