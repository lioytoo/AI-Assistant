
def check_bedtime_warning(current_mode, memory):
    import datetime
    from datetime import datetime
    from motion_detection import detect_motion_in_bed
    from AI_voice import speak, listen, ask_local_model
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    hour = now.hour
    minute = now.minute
    #print(f"Current time: {hour}:{minute}")


    from memory import mmory
    # Need to understand what it does or even if I need it
    if "checks" not in memory:
        memory["checks"] = {}


    if today not in memory["checks"]:
        memory["checks"][today] = {}

    
    # 🔔 At 23:30 - Tell the user to stop using screens
    if (hour == 23 and minute == 30) or True: # and not memory["checks"][today].get("23:30"): testing 
        # Check motion
        in_bed = detect_motion_in_bed(debug = True)

        if not in_bed:
            prompt = "Tell the user they have 30 minutes left before bedtime so they need to stop using screens."
            reply = ask_local_model(prompt, current_mode)
            speak(reply, current_mode)

        # Save this check so it doesn't repeat
        memory["checks"][today]["23:30"] = True
        mmory.save_memory(memory)

    # ⏰ Check again at midnight
    elif hour == 0 and minute == 0 and not memory["checks"][today].get("00:00"):
        in_bed = detect_motion_in_bed(debug = True)
        
        if not in_bed:
            prompt2 = "Say strictly to the user that it's midnight and it's time to go to sleep now."
            reply2 = ask_local_model(prompt2, current_mode)
            speak(reply2, current_mode)


            # Listen for excuses
            speak("Do you want 10 more minutes?", current_mode)
            resp = listen()

            if "10 more" in resp:
                if today not in memory.get("bedtime_delayed", {}):
                    speak("Okay, last 10 minutes.", current_mode)
                    memory.setdefault("bedtime_delayed", {})[today] = True
                    mmory.save_memory(memory)

                else:
                    speak("No more delays. Go to sleep now.", current_mode)


            elif "going to sleep" in resp:
                speak("Good job. Sleep well.", current_mode)
                memory.get("bedtime_delayed", {}).pop(today, None)
            else:
                speak("Alright. Good night", current_mode)
            

        memory["checks"][today]["00:00"] = True
        mmory.save_memory(memory)
