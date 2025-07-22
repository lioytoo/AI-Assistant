Do you have a hard time forcing yourself to go to sleep? and you just wish that there was someone to help you understand how important it is for you in the future?
If YES then AI Assistant is for YOU!

You can set the time for your preference and it will give you a warning 30 minutes before the time up so you will stop using any screens. When the time comes you can request one time for more 10 mintes.
In addition to that, you will have a GUI that has your AI chat history and start and stop buttons.



<ins>**Writing down how diffrent pieces of code works:**</ins>
```python
# Choose what microphone to use
working_indexes = sr.Microphone.list_working_microphones()
all_names = sr.Microphone.list_microphone_names()

# using this for selecting only the working devices (microphones)
# Build a list of (index, name) tuples for working mics
working_mics = [(i, all_names[i]) for i in working_indexes if i < len(all_names)]

mic_name = sr.Microphone.list_working_microphones()
self.selected_mic_index = tk.IntVar()
self.selected_mic_index.set(working_mics[0][0])  # Default to first mic ---- TODO: make it save the mic option

mic_dropdown = tk.OptionMenu(btn_frame, self.selected_mic_index, *[mic[0] for mic in working_mics])
mic_dropdown.config(bg="#2B2D31", fg="white", activebackground="#3A3D42", activeforeground="white", highlightthickness=1, bd=0)
mic_dropdown.pack(anchor="se", side=tk.RIGHT, padx=10, pady=5)

# Show the name of the selected mic in a label
mic_label = tk.Label(btn_frame, text = working_mics[0][1], bg="#2B2D31", fg="white")
```
First, it calls ```sr.Microphone.list_working_microphones()```, which returns a dictionary for microphones that are currently working, 
then it also retrieves all of the available microphones using ```sr.Microphones.list_microphone_names()```, 
witch returns a list where each index corresponds to a device index.

To display only the working microphones, it builds  a list of tuples (index, name) for each working microphone.

A Tkinter ```tk.IntVar()``` is created to store the selected microphone index, and it's initialized to the first working microphone by default.
