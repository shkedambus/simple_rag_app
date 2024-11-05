from my_ollama.llm import answer_question_with_context
from my_ollama.parser import process_query
import os

os.environ["USER_AGENT"] = "MyApp/1.0 (Python 3.10; Windows 10)"

process_query()
question = input("What do you want to ask?\n")
answer = answer_question_with_context(question)
print("Answer:\n", answer, end="\n")