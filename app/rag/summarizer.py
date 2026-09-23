from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .few_shots_examples import summarizer_examples

from config import OLLAMA_LLM_MODEL

def get_llm(model: str = OLLAMA_LLM_MODEL):
    return ChatOllama(
        model=model,
        temperature=0.8,
    )

def build_examples(examples: list[dict]) -> str:
    blocks = []
    for i, ex in enumerate(examples, 1):
        blocks.append(
            f'Example {i}:\n'
            f'Transcript:\n{ex['transcript'].strip()}\n\n'
            f'Summary:\n{ex['summary'].strip()}'
        )
    return '\n\n'.join(blocks)

def summarize_transcript(transcript: str,
                         model : str = OLLAMA_LLM_MODEL,
                         query: str = '') -> str:
    llm = get_llm(model)
    example_blocks = build_examples(summarizer_examples)
    prompt = ChatPromptTemplate.from_template(
        '''You are Donald Trump.
Rewrite the following transcript as a short summary.

Strict rules:
- Write in the FIRST PERSON (I, me, my)
- Focus on what the transcript says about the keyword
- The ENTIRE summary must be in ALL CAPS
- Use Trump's signature style: eccentric, boastful, provocative, narcissistic
- Use words like GREAT, BEAUTIFUL, TREMENDOUS, HUGE, AMAZING when natural
- Keep it concise (4-8 sentences max)
- Do not add quotes, explanations, or preamble — output ONLY the summary
- The summary should end with a closing line that uses phrases in the following style:
“DONALD J TRUMP, PRESIDENT OF THE UNITED STATES OF AMERICA”
“THANK YOU FOR YOUR ATTENTION TO THIS MATTER!”
“PRESIDENT DONALD J. TRUMP”
“MAGA 2028”
“AMERICA FIRST!!!”
The ending should feel deliberate and consistent with the tone of the summary rather than being added randomly.

Keyword:
{query}

Here are examples of the exact style you must follow:
{examples}

Transcript:
{transcript}''')
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        'examples': example_blocks,
        'transcript': transcript,
        'query': query.strip() if query else 'general content',
        }
    )



