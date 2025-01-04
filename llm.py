# from transformers import pipeline
# from resources import save_to_csv_file, read_text_file
#
# def chunk_text(text, chunk_size=512):
#     words = text.split()
#     for i in range(0, len(words), chunk_size):
#         yield " ".join(words[i:i + chunk_size])
#
#
# def summarize_text(content):
#     print("Started Summarizing text")
# # # loading the model for summarization
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
#     chunk_summaries = []
#     for chunk in chunk_text(content, chunk_size=512):
#         chunk_summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
#         chunk_summaries.append(chunk_summary[0]['summary_text'])
#
#     final_summary_list = summarizer(" ".join(chunk_summaries), max_length=200, min_length=50, do_sample=False)
#     final_summary = final_summary_list[0]['summary_text']
#     print("Final Summary:")
#     print(final_summary)
#     return final_summary
#
# def get_summarized_text(content, input_text):
#     # content = read_text_file()
#     final_summary = summarize_text(content)
#     save_to_csv_file(final_summary, "summary_files/" + input_text + ".txt")
