
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
from datetime import datetime
import threading
from assistant import bedtime_warning
gui_app = None
# For changing speak modes
global current_mode
current_mode = "jarvis" # Default mode
print("Assistant started. Use the GUI to interact with the assistant.")


client = OpenAI(api_key="lmstudio", base_url="http://127.0.0.1:1234/v1")


def ask_local_model(prompt, mode="jarvis", model_name="mistral-7b-instruct-v0.2"):
    global gui_app
    print("→ Sending prompt to local model:", prompt)
    if gui_app is not None:
        gui_app.update_chat(f"User: {prompt}" )

    # Choose system prompt based on mode
    if mode == "jarvis":
        styled_prompt = (
            "JARVIS is a helpful and respectful AI assistant.\n"
            f"You have been asked: {prompt}\n"
            "JARVIS:"
        )
    else:
        styled_prompt = prompt    
    
    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": styled_prompt}],
            temperature=0.7,
            max_tokens=200
        )
        content = resp.choices[0].message.content
        print("← Received reply:", content)
        if gui_app is not None:
            gui_app.update_chat(f"{current_mode}: {content}")
        return content
    except Exception as e:                      # If the reply is empty, the problem is before TTS
        print("Error calling local model:", e)
        return ""



def get_voice_by_name(name_fragment):
    for voice in voices:
        if name_fragment.lower() in voice.name.lower():
            return voice.id
        

# TTS ("speak") Setup
engine = pyttsx3.init()    
voices = engine.getProperty("voices")

# For changing voices
def speak(text, mode = "jarvis"): # for default

    if mode == "jarvis": # Jarvis voice
        voice_index = get_voice_by_name("george")
        # Format address politly, add a small prefix
        engine.setProperty('rate', 250)  # adjust as you like
        engine.setProperty('volume', 1.0)
        message = f"sir, {text}"


    elif mode == "friendly":    # Friendly / Strict Male voice
        voice_index = get_voice_by_name("david")
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        message = text
    

    elif mode == "female":    # Friendly Female voice
        voice_index = get_voice_by_name("hazel")
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        message = f"Hey {text}"
    
    else:
        voice_index = voices[0].id
        message = text

    if voice_index:
        engine.setProperty("voice", voice_index)
    
    else:
        print("Warning: Voice not found, using default")

    engine.say(message)
    engine.runAndWait()



# Speach Recognition ("listen") Setup
def listen(timeout = 10, phrase_time_limit = 15):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Assistant]: I'm listening...")
        audio = r.listen(source, phrase_time_limit = phrase_time_limit, timeout = timeout)
    try:
        text = r.recognize_google(audio).lower()
        return text
    except sr.UnknownValueError:
        print("❌ Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        print("Could not request results - check your network connection.")
        return ""
    except Exception as e:
        print(f"Unexpected error in listen(): {e}")
        return "" 





# Assistant Logic
def run_assistant():
    def loop():
        from memory import mmory
        global current_mode, gui_app
        while is_running:
            # After we check if it's not the time for bed we starting a conversation
            gui_app.update_chat("[Assistant]: I'm listening...")
            print("I'm listening...")
            user_input = listen()
            if user_input:
                facts = mmory.load_facts()
                memory = mmory.load_memory()

                # Handle commands
                if "switch to friendly" in user_input:
                    current_mode = "friendly"
                    speak("Switched to friendly mode.", current_mode)

                elif "switch to jarvis" in user_input:
                    current_mode = "jarvis"
                    speak("Switched to jarvis mode.", current_mode)

                elif "switch to female" in user_input:
                    current_mode = "female"
                    speak("Switched to female mode.")
                    
                elif "go to sleep" in user_input: # TODO: optional add if user said stop it will stop aswell
                    gui_app.update_chat("user: go to sleep")
                    speak("Okay. Good night.", current_mode)
                    print("Okay. Good night")
                    stop_assistant()
                
                elif user_input.startswith("no,") or "it's actually" in user_input or "correction:" in user_input:
                    
                    corrected = user_input.replace("no,", "").replace("it's actually", "").replace("correction:", "").strip()
                    gui_app.update_chat("what topic is this correction for?")
                    speak("What topic is this correction for?", current_mode)
                    topic = listen()
                    if topic:
                        facts[topic] = corrected
                        mmory.save_facts(facts)
                        gui_app.update_chat(f"Okay, I've update the fact: {topic}.")
                        speak(f"Okay, I've updated the fact: {topic}.", current_mode)
                
                else:
                    enhanced_prompt = mmory.inject_fact_memory(user_input, facts)
                    reply = ask_local_model(enhanced_prompt, current_mode)
                    

                    speak(reply, current_mode)


            #time.sleep(0.5) # Optional pause
    thread = threading.Thread(target = loop)
    thread.start()


# GUI
import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
import json
import os

# Assistant GUI
class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Assistant")
        self.window.geometry("800x600")
        self.window.configure(background="#2B2D31")

        # Create chat display ONCE
        self.chat_dp = scrolledtext.ScrolledText(self.window, wrap = tk.WORD, state = 'disabled')
        self.chat_dp.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_dp.configure(font=21, fg="white", background="#2B2D31")

        btn_frame = tk.Frame(self.window)
        btn_frame.pack( anchor= "s", pady=10)

        #self.update_chat("GUI loaded successfully") was to check if any text shows in the GUI.
        
        #     < ------ Buttons ------ >
        # Press start Button to activate assistant 
        start_btn = tk.Button(btn_frame, text = "Activate Assistant", command = start_assistant, bg="green", fg="white", width=20, height=2)
        start_btn.pack(side = tk.TOP, padx=10)
        
        # Press stop Button to deactive assistant
        stop_btn = tk.Button(btn_frame, text = "Stop Assistant", command = stop_assistant, bg="red", fg="white", width=20, height=2)
        stop_btn.pack(side = tk.TOP, padx=10)


        # Load chat history from this code in the file on startup (optional) - For now I'm okay with this
        if os.path.exists("chat_history.json"):
            with open("chat_history.json", "r") as file:
                try:
                    history = json.load(file)
                    for line in history:
                        self.update_chat(line["message"], save = False) # Only show the messages, don't save again
                except:
                    pass
        self.window.after(1000, self.check_bedtime)


    def update_chat(self, text, save = True):
        def do_update():
            self.chat_dp.config(state = "normal")
    
            # Handle dict vs string
            if isinstance(text, dict) and "text" in text:
                display_text = text["text"]
    
            else:
                display_text = str(text)
    
            self.chat_dp.insert(tk.END, display_text + '\n')
            self.chat_dp.yview(tk.END)
            self.chat_dp.config(state = "disabled")

            # We need to load the chat history
            if save:
                from memory import mmory

                # Save to json file
                mmory.save_chat(display_text)
        self.window.after(0, do_update)


    # Import the logic for checking the time for the AI camera
    def check_bedtime(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        if hour == 23 and minute == 30: #(hour == 0 and minute == 0):
            from memory import mmory
            memory = mmory.load_memory()
            bedtime_warning(current_mode, memory)
            
        self.window.after(60000, self.check_bedtime) # after 6 sec it will trigger the check motion in bed


is_running = False
def start_assistant():
    global is_running, gui_app
    is_running = True
    if gui_app is not None:
        gui_app.update_chat("Assistant activated.")
    run_assistant()


def stop_assistant():
    global is_running, gui_app
    is_running = False
    if gui_app is not None:
        gui_app.update_chat("Assistant stopped.")

# Assistant GUI
if __name__ == "__main__":
    gui_app = GUI()
    gui_app.window.mainloop()

