from transformers import pipeline, BartTokenizer
import streamlit as st
from resources import read_text_file
from crawling import get_crawled_text

@st.cache_resource
def load_summarizer():
    summarizer = pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        revision="main"
    )
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    return summarizer, tokenizer

# Load the summarizer once at startup
summarizer, tokenizer = load_summarizer()

def summarize_text(content):
        def chunk_text(text, tokenizer, max_tokens=1000):
            tokens = tokenizer.encode(text)
            for i in range(0, len(tokens), max_tokens):
                yield tokenizer.decode(tokens[i: i + max_tokens], skip_special_tokens=True)

        chunks = list(chunk_text(content, tokenizer))

        chunk_summaries = summarizer(chunks, max_length=150, min_length=30, do_sample=True, batch_size=4)
        chunk_summaries_texts = [summary['summary_text'] for summary in chunk_summaries]
        combined_summary = " ".join(chunk_summaries_texts)
        print("Combined summary is completed")
        print("Chunked Summary: ",combined_summary )
        if len(tokenizer.encode(combined_summary)) > 1000:
            final_chunks = list(chunk_text(combined_summary, tokenizer))
            final_summary_list = summarizer(
                final_chunks, max_length=200, min_length=100, do_sample=True, batch_size=4
            )
            final_summary_texts = [summary['summary_text'] for summary in final_summary_list]
            return " ".join(final_summary_texts)

        else:
            # If within token limit, summarize directly
            final_summary = summarizer(
                combined_summary, max_length=200, min_length=100, do_sample=False
            )
            return final_summary[0]['summary_text']

import streamlit as st

def main():
    # App title and layout
    st.title("📖 Text Summarization App")
    st.markdown("Welcome to the **Text Summarization App**. Enter your text below, and we'll summarize it for you!")

    # Sidebar for better navigation
    st.sidebar.title("Options")
    st.sidebar.markdown("Use this sidebar to adjust settings in the future.")

    # Input text area for users
    input_text = st.text_input("📝 Enter text to summarize:", "", help="Paste or type the text you want to summarize.")

    # Placeholders for dynamic content
    message_placeholder = st.empty()
    summary_placeholder = st.empty()  # Placeholder for summary content

    # Button to trigger summarization
    if st.button("✨ Summarize"):
        # Clear previous content
        message_placeholder.empty()
        summary_placeholder.empty()

        if input_text.strip():
            # Debugging: Show the input text
            st.write("Input Text:", input_text)

            # Loading messages
            message_placeholder.info("🔄 Crawling content... Please wait.")
            content = get_crawled_text(input_text)
            print("Content:")
            print(content)
            message_placeholder.info("💡 Summarizing the content... Please wait.")
            summary = summarize_text(content)

            # Clear loading message and display the summary
            message_placeholder.empty()
            summary_placeholder.subheader("📝 Summary:")
            summary_placeholder.success(summary)

        else:
            st.error("🚨 Please enter some text to summarize.")




if __name__=="__main__":
    main()