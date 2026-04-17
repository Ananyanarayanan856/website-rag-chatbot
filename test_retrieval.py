import os
import sys

# Add the parent directory to sys.path so we can import chatbot
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from chatbot.chatbot import retrieve_context

def test():
    query = "what is the name of company"
    context = retrieve_context(query)
    print(f"--- Context for '{query}' ---")
    print(context)
    print("--------------------------------")

if __name__ == "__main__":
    test()
