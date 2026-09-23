from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import OLLAMA_LLM_MODEL

def get_llm(model: str = OLLAMA_LLM_MODEL):
    return ChatOllama(
        model=model,
        temperature=0.0,
    )

def classify_sentiment(transcript: str, model: str = OLLAMA_LLM_MODEL) -> str:
    # Classifies the found transcript as semantically positive or negative
    llm = get_llm(model)
    prompt = ChatPromptTemplate.from_template(
        '''You are a sentiment classifier.

Classify the overall sentiment of the following transcript as exactly one of:
- positive
- negative

Rules:
- Reply with ONLY one word: positive OR negative
- No explanations, no punctuation, no extra text
- Base your decision on the overall tone and message of the transcript

Transcript:
{transcript}''')

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({'transcript': transcript}).strip().lower()
    if "positive" in result:
        return "positive"
    if "negative" in result:
        return "negative"

    return "unknown"