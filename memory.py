import json
import os
import datetime
from datetime import datetime
# To add a function to save/load memory for bedtime
class mmory: # Memory


    def save_memory(memory):
        with open("bedtime_memory.json", "w") as file:
            json.dump(memory, file)


    def load_memory():
        if os.path.exists("bedtime_memory.json"):
            with open("bedtime_memory.json", "r") as file:
                return json.load(file)
        else:
            return {}


    # Storing fact for the AI to remember so it will stop saying wrong information
    def save_facts(facts):
        with open("facts.json", "w") as file:
            json.dump(facts, file, indent = 2)


    def load_facts():
        if os.path.exists("facts.json"):
            with open("facts.json", "r") as file:
                return json.load(file)
        else:
            return {}


    def inject_fact_memory(prompt, facts):
        if not facts:
            return prompt
        for topic, fact in facts.items():
            if topic.lower() in prompt.lower():
                return f"Remember: {topic} is {fact}. Answer the following: \n{prompt}"
        return prompt
    


    def save_chat(txt, file_path = "chat_history.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    chat_log = json.load(file)
                    if not isinstance(chat_log, list):
                        chat_log = [] # Fallback if file isn't a list
                except json.JSONDecodeError:
                    chat_log = []

        else:
            chat_log = [] # Starts with empty list

        chat_log.append({
            "timestamp": datetime.now().strftime("%d-%m-%Y, %H:%M"),
            "message": txt
        })

        with open("chat_history.json", "w") as file:
            json.dump(chat_log, file, indent = 2)

    def load_chat(file_path = "chat_history.json"):
        if os .path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    message = json.load(file)
                    return message if isinstance(message, list) else []
                except json.JSONDecodeError:
                    return []
        return []




    # Load and show chat history
    # saved_chats = load_chat()
    # for msg in saved_chats:


    
