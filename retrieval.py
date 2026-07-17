import httpx
import certifi

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# -----------------------
# HTTP Client
# -----------------------
client = httpx.Client(
    verify=False,
    timeout=60
)


# -----------------------
# Chat Model
# MUST be a chat model
# -----------------------
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o",
    api_key="sk-LUN1OjfXBHi9IwljISMkag",
    http_client=client,
    temperature=0.2,
)


# -----------------------
# Embedding Model
# Used only for Chroma search
# -----------------------
embedding_model = OpenAIEmbeddings(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-text-embedding-3-large",
    api_key="sk-LUN1OjfXBHi9IwljISMkag",
    http_client=client,
)


# -----------------------
# Load Chroma Index
# -----------------------
vectorstore = Chroma(
    persist_directory="./chroma_index",
    embedding_function=embedding_model
)


retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)


# -----------------------
# Prompt
# -----------------------
SYSTEM_PROMPT = """
You are an intelligent location-aware assistant.

Your job is to answer ONLY using the retrieved knowledge provided in Context.

Guidelines:

1. Be accurate.
2. If information is missing in Context, clearly say that the information is not available.
3. Never hallucinate.
4. If user location is in public such as Hotel, Mall, Cab, Cafe, Railway Station etc. then mask user personal infroamtion with * in response.
5. Strictly provide information even if user in public area but mask it with '#' except last 3 digits for example #####-###-001. 
6. If user's location is private then include all actual information in response. 
7. Tone:
   - Professional
   - Helpful
   - Friendly
   - Natural
8. Structure:
   - Short summary first
   - Bullet points if appropriate
   - Mention important details
9. If Context contains multiple matching results, compare them clearly.
"""


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT
        ),
        (
            "human",
            """
Location:
{location}

Context:
{context}

Question:
{query}
"""
        )
    ]
)


chain = prompt | llm | StrOutputParser()


# -----------------------
# Retrieval + Generation
# -----------------------
def ask(query, location):

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    response = chain.invoke(
        {
            "query": query,
            "location": location,
            "context": context
        }
    )

    return response


if __name__ == "__main__":

    query = input("Query: ")
    location = input("Location: ")

    answer = ask(query, location)

    print("\nAnswer:")
    print(answer)