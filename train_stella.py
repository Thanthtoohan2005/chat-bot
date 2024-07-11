import json
import re
import random
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.8)
    return matches[0] if matches else None

def sanitize_input(user_input: str) -> str:
    # Remove leading and trailing whitespaces
    sanitized_input = user_input.strip()
    # Remove punctuation marks
    sanitized_input = re.sub(r'[^\w\s]', '', sanitized_input)
    return sanitized_input.lower()

def contains_punctuation(input_str: str) -> bool:
    # Check if the input contains any punctuation mark
    return any(char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' for char in input_str)

def get_random_response(responses: list[str]) -> str:
    return random.choice(responses)

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["question"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    random_responses = [
        "Hmm, interesting. But I don't know how to answer that question. Can teach me on how to respond?",
        "I'm not entirely sure, could you teach me how to answer that?",
        "That's an intriguing question! Mind giving me some context on how to respond?",
        "I'm not certain, could you explain further?",
        "As a learning model underdevelopment, I can not provide you the information you inquired. Can you teach me how to respond?",
    ]

    while True:
        user_input: str = input('You: ').strip().lower()

        if user_input.lower() == "quit":
            break

        sanitized_input = sanitize_input(user_input)

        best_match: str | None = find_best_match(sanitized_input, [q["question"] for q in knowledge_base["question"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print(f"Bot: {get_random_response(random_responses)}")
            new_answer: str = input('type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["question"].append({"question": sanitized_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank you! I learned a new response")

if __name__ == "__main__":
    chat_bot()
