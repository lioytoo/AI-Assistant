
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
from datetime import datetime
import threading


# For changing speak modes
global current_mode
current_mode = "jarvis" # Default mode
print("Assistant started. Use the GUI to interact with the assistant.")


client = OpenAI(api_key="lmstudio", base_url="http://127.0.0.1:1234/v1")


def ask_local_model(prompt, mode="jarvis", model_name="mistral-7b-instruct-v0.2"):
    print("→ Sending prompt to local model:", prompt)

    # Choose system prompt based on mode
    if mode == "jarvis":
        styled_prompt = (
            "JARVIS is a helpful and respectful AI assistant.\n"
            f"Human: {prompt}\n"
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
        return content
    except Exception as e:
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




# Remove the blocking CLI loop and rely on the GUI buttons to start/stop the assistant.
# The run_assistant() function will handle the assistant logic in a separate thread when activated from the GUI.

# Dummy assistant logic for demo
is_running = False
#chat_h = [] # Chat History




def start_assistant():
    global is_running
    is_running = True
    update_chat("Assistant activated.")
    run_assistant()


def stop_assistant():
    global is_running
    is_running = False
    update_chat("Assistant stopped.")


# Assistant Logic
def run_assistant():
    def loop():
        global current_mode
        while is_running:
            # Import the logic for checking the time for the AI camera
            


            now = datetime.now()
            today = now.strftime("%Y-%m-%d") # Not used right now, but will be used later to schedule
            hour = now.hour
            minute = now.minute

            if (hour == 23 and minute == 50) or (hour == 0 and minute == 0):
                from assistant import check_bedtime_warning
                from memory import mmory
                memory = mmory.load_memory()
                check_bedtime_warning(current_mode, memory)
            

            # After we check if it's not the time for bed we starting a conversation
            update_chat("[Assistant]: I'm listening...")
            print("I'm listening...")
            user_input = listen()
            if user_input:
                # Import the memory logic
                from memory import mmory
                update_chat(f"You said: {user_input}")
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
                    
                elif "go to sleep" in user_input:
                    speak("Okay. Good night.", current_mode)
                    stop_assistant()
                
                elif user_input.startswith("no,") or "it's actually" in user_input or "correction:" in user_input:
                    
                    corrected = user_input.replace("no,", "").replace("it's actually", "").replace("correction:", "").strip()
                    speak("What topic is this correction for?", current_mode)
                    topic = listen()
                    if topic:
                        facts[topic] = corrected
                        mmory.save_facts(facts)
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

def update_chat(text):
    chat_h = [] # Chat History
    chat_h.append(text) 
    chat_dp.config(state = "normal")
    chat_dp.insert(tk.END, text + '\n')
    chat_dp.yview(tk.END)
    chat_dp.config(state = "disabled")


# Assistant GUI
window = tk.Tk()
chat_dp = scrolledtext.ScrolledText(window, wrap = tk.WORD, state = 'disabled')
chat_dp.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

window.title("AI Assistant")
window.geometry("800x600")
btn_frame = tk.Frame(window)
btn_frame.pack( anchor= "w",pady=10)


# Start Button 
start_btn = tk.Button(btn_frame, text = "Activate Assistant", command = start_assistant, bg="green", fg="white", width=20, height=2)
start_btn.pack(side = tk.TOP, padx=10, pady=5)


# Stop Button
stop_btn = tk.Button(btn_frame, text = "Stop Assistant", command = stop_assistant, bg="red", fg="white", width=20, height=2)
stop_btn.pack(side = tk.TOP, padx=10, pady=5)


#tk.Button(window, text="Quit", command=window.quit).pack(side="right")
window.mainloop()

