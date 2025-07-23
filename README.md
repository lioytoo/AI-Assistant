Do you have a hard time forcing yourself to go to sleep? and you just wish that there was someone to help you understand how important it is for you in the future?
If YES then AI Assistant is for YOU!

You can set the time for your preference and it will give you a warning 30 minutes before the time up so you will stop using any screens. When the time comes you can request one time for more 10 mintes.
In addition to that, you will have a GUI that has your AI chat history and start and stop buttons.



<ins>**Writing down how diffrent pieces of code works:**</ins>
```python
        # Choose what microphone to use
        working_indexes = sr.Microphone.list_working_microphones()
        all_names = sr.Microphone.list_microphone_names()


        # Build a list of (index, name) tuples for working mics
        self.working_mics = [(i, all_names[i]) for i in working_indexes if i < len(all_names)]

        # Stores the selected microphone index
        self.selected_mic_index = tk.IntVar()
        self.selected_mic_index.set(self.working_mics[0][0])  # Default to first mic ---- TODO: make it save the mic option after closing the app

        # To display the menu
        mic_dropdown = tk.OptionMenu(btn_frame, self.selected_mic_index, *[mic[0] for mic in self.working_mics])
        mic_dropdown.config(bg="#2B2D31", fg="white", activebackground="#3A3D42", activeforeground="white", highlightthickness=1, bd=0)
        mic_dropdown.pack(anchor="se", side=tk.RIGHT, padx=10, pady=5)


        # Show the name of the selected mic in a label
        self.mic_label = tk.Label(btn_frame, text = self.working_mics[0][1], bg="#2B2D31", fg="white")
        self.mic_label.pack(side=tk.RIGHT, padx=10)

        self.selected_mic_index.trace_add("write", self.update_mic_label)
```
First, it calls ```sr.Microphone.list_working_microphones()```, which returns a dictionary for microphones that are currently working, 
then it also retrieves all of the available microphones using ```sr.Microphones.list_microphone_names()```, 
witch returns a list where each index corresponds to a device index.

To display only the working microphones, it builds  a list of tuples (index, name) for each working microphone.

A Tkinter ```tk.IntVar()``` is created to store the selected microphone index, and it's initialized to the first working microphone by default.

Next we have a temporary solution to know the name of the microphone:
```python
    def update_mic_label(self, *args):
        selected_index = self.selected_mic_index.get()
        
        # Look for the mic name matching the selected index
        mic_name = "unknown" 
        for index, name in self.working_mics:
            if index == selected_index:
                mic_name = name

        self.mic_label.config(text=mic_name)
```
First, we assign selected_index to get the microphone index, then we have a tuple which is (index, name)
that we are checking with it, if the index is equal to ```selected_index``` and if yes, we assign ```mic_name``` to be from that index's name pair.
