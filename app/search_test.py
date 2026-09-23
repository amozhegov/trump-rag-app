from rag.retriever import search
from rag.summarizer import summarize_transcript
from rag.classifier import classify_sentiment

def main():
    while True:
        query = input('Input a keyword (or enter "/bye"): ').strip()
        if query.lower() in ('exit', 'quit', 'bye'):
            break
        docs = search(query, k=1)

        if not docs:
            print('Nothing is found')
            continue



        transcript = docs[0].page_content
        print("\n" + "=" * 60)
        print("Found transcript:")
        print("=" * 60)
        print(transcript[:1500])  # first 1500 symbols
        if docs[0].metadata:
            print("\nMetadata:", docs[0].metadata)
        print("=" * 60)
        print('TRUMP STYLE SUMMARY: ')
        print("=" * 60)

        try:
            summary = summarize_transcript(transcript, query = query)
            print(summary)
        except Exception as e:
            print(f'Error while summarizing: {e}')
        print("=" * 60)

        try:
            classification = classify_sentiment(transcript)
        except Exception as e:
            classification = f'Error while classifying: {e}'
        print("=" * 60)
        print('Sentiment: ', classification.upper())

if __name__ == "__main__":
    main()