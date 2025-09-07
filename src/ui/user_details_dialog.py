import customtkinter as ctk

class UserDetailsDialog(ctk.CTkToplevel):
    """
    A modal dialog to capture user details before starting the session.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("Start New Session")
        self.lift()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.grab_set() # Make this window modal

        self.details = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Enter your details to begin:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        ctk.CTkLabel(self, text="Name:").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(self, placeholder_text="e.g., Priya")
        self.name_entry.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Education Stream:").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.stream_entry = ctk.CTkEntry(self, placeholder_text="e.g., STEM, Humanities")
        self.stream_entry.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Major:").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.major_entry = ctk.CTkEntry(self, placeholder_text="e.g., Computer Science")
        self.major_entry.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="College Name:").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.college_entry = ctk.CTkEntry(self, placeholder_text="e.g., MIT")
        self.college_entry.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

        self.submit_button = ctk.CTkButton(self, text="Start Brainstorming", command=self._on_submit)
        self.submit_button.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

    def _on_submit(self):
        """Called when the user clicks the submit button."""
        self.details = {
            "name": self.name_entry.get(),
            "stream": self.stream_entry.get(),
            "major": self.major_entry.get(),
            "college": self.college_entry.get()
        }
        # Basic validation to ensure no fields are empty
        if all(self.details.values()):
            self.grab_release()
            self.destroy()
        else:
            self.details = None
            # You can add a proper error message label here
            print("Error: All fields are required.")

    def _on_closing(self):
        """Handle case where user closes the dialog window."""
        self.details = None
        self.grab_release()
        self.destroy()

    def get_details(self):
        """This method is called to display the dialog and wait for user input."""
        self.master.wait_window(self)
        return self.details