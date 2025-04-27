from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from app.langchain.initialize.chatModel import llm
from app.langchain.initialize.embedModel import embeddings
from app.langchain.initialize.astraModel import get_vector_store_for_chat
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader
from app.classes.Classes import Question, Answer
from langchain_core.vectorstores import InMemoryVectorStore
from fastapi.encoders import jsonable_encoder
import os
from langchain_core.prompts import PromptTemplate
import tempfile
from typing import Literal
from typing_extensions import Annotated

class Search(TypedDict):
    """Search query."""

    query: Annotated[str, ..., "Search query to run."]
    section: Annotated[
        Literal["beginning", "middle", "end"],
        ...,
        "Section to query.",
    ]

async def chat(question_input: Question, files: List[UploadFile] = None):
    # Check if the file is provided
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)
    
    docs = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in files:
            # Generate a temporary file path for each file
            temp_file_path = os.path.join(temp_dir, file.filename)
            
            # Write the content of each file to the temporary file
            with open(temp_file_path, 'wb') as temp_file:
                temp_file.write(await file.read())
            
            # Load PDF content using PyPDFLoader
            loader = PyPDFLoader(
                temp_file_path,
                mode="paged",
                pages_delimiter="\n-------THIS IS A CUSTOM END OF PAGE-------\n",
            )
            docs += loader.load()
        
    # Step 2: Split the documents into chunks for easier vectorization
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Max size of each chunk
        chunk_overlap=50,  # Overlap between chunks
        add_start_index=True  # Add index at the start of each chunk
    )
    all_splits = text_splitter.split_documents(docs)

    total_documents = len(all_splits)
    third = total_documents // 3

    # Step 1: Build helper to assign sections
    def assign_section(idx: int, total: int) -> str:
        third = total // 3
        if idx < third:
            return "beginning"
        elif idx < 2 * third:
            return "middle"
        else:
            return "end"
    
    # Step 2: Add section metadata
    total_documents = len(all_splits)
    for idx, document in enumerate(all_splits):
        document.metadata["section"] = assign_section(idx, total_documents)
        # Optional: If page number exists in metadata
        if "page" not in document.metadata:
            document.metadata["page"] = idx  # fallback page number if missing
    
    # Step 3: Insert into vector store
    vector_store = InMemoryVectorStore(embeddings)
    vector_store.add_documents(all_splits)

    # Define the prompt for question-answering
    prompt = custom_rag_prompt
    # Define state for application
    class State(TypedDict):
        question: str
        context: list[Document]
        query: Search
        answer: str
        
    def analyze_query(state: State):
        structured_llm = llm.with_structured_output(Search)
        query = structured_llm.invoke(state["question"])
        print("Structured query:", query)
        return {"query": query}
    
    # Define application steps for retrieve and generate
    def retrieve(state: State):
        query = state["query"]
        retrieved_docs = vector_store.similarity_search(
            query["query"],
            filter=lambda doc: doc.metadata.get("section") == query["section"],
        )
        return {"context": retrieved_docs}

    def generate(state: State):
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}
    
    
    # Compile the graph with retrieve and generate steps
    graph_builder = StateGraph(State).add_sequence([analyze_query, retrieve, generate])
    graph_builder.add_edge(START, "analyze_query")
    graph = graph_builder.compile()
    
    for step in graph.stream(
        {"question": "What does the end of the post say about Task Decomposition?"},
        stream_mode="updates",
    ):
        print(f"{step}\n\n----------------\n")
    result = graph.invoke({"question": question_input.question})
    final_answer = result["answer"]

    # Wrap the final answer in the Answer class
    answer = Answer(
        answer=final_answer,
        question=question_input.question
    )

    # Return the answer as a JSON-serializable response
    return jsonable_encoder(answer)
