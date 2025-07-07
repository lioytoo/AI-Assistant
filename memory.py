import json
import os

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