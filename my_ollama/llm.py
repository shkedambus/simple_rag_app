from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from my_qdrant.db import similarity_search

model = ChatOllama(
    model="llama3.1:8b",
)

RAG_TEMPLATE = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

<context>
{context}
</context>

Answer the following question:

{question}"""

def answer_question_with_context(question):
    context = similarity_search(question)
    rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)
    qa_chain = (
        rag_prompt
        | model
        | StrOutputParser()
    )

    answer = qa_chain.invoke({"context": context, "question": question})
    return answer