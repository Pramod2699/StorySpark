import customtkinter as ctk
import sys
import os

# Adjust path to import from the root of the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Backend and UI Imports ---
from src.handlers.AnswerGenerator import AnswerGenerator
from src.utils.Logger import Logger
from src.config.ConfigHelper import ConfigHelper
from src.ui.user_details_dialog import UserDetailsDialog

class EssayBrainstormerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Essay Brainstormer")
        self.geometry("800x700")
        ctk.set_appearance_mode("Light")

        # --- Backend Initialization ---
        self.logger = Logger()
        self.config = ConfigHelper().config
        self.answer_generator = AnswerGenerator()

        self._configure_layout()
        self._create_widgets()
        
        # --- Start the session flow ---
        self.after(200, self.start_new_session)

    def _configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def _create_widgets(self):
        # --- 1. Header Frame ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(self.header_frame, text="helloivy", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=(0, 20), sticky="w")
        ctk.CTkLabel(self.header_frame, text="New Essay Brainstorming", font=ctk.CTkFont(size=20)).grid(row=0, column=1, sticky="w")

        # --- 2. Instructions Frame ---
        self.instructions_frame = ctk.CTkFrame(self, fg_color="#F9F9F9", border_width=1, border_color="#E0E0E0", corner_radius=10)
        self.instructions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        instructions_text = "Instructions\n\nWelcome! Please provide your details to begin the personalized brainstorming session."
        self.instructions_label = ctk.CTkLabel(self.instructions_frame, text=instructions_text, justify="left", wraplength=600)
        self.instructions_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        # --- 3. Main Content Frame ---
        self.main_content_frame = ctk.CTkFrame(self, corner_radius=15, border_width=2, border_color="#EAD9FF")
        self.main_content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.main_content_frame.grid_rowconfigure(1, weight=1)
        self.main_content_frame.grid_columnconfigure(0, weight=1)
        self.chat_history_frame = ctk.CTkScrollableFrame(self.main_content_frame, fg_color="transparent")
        self.chat_history_frame.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")

        # --- Input Area ---
        self.input_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.response_entry = ctk.CTkTextbox(self, height=40, border_color="#E0E0E0", border_width=1, corner_radius=10)
        self.response_entry.grid(row=0, column=0, sticky="ew", in_=self.input_frame)
        self.response_entry.insert("1.0", "Your answers will go here...")
        self.response_entry.configure(state="disabled")

        self.send_button = ctk.CTkButton(self, text="Send ✉️", width=40, height=40, command=self.send_user_message)
        self.send_button.grid(row=0, column=1, padx=(10, 0), in_=self.input_frame)
        self.send_button.configure(state="disabled")

    def start_new_session(self):
        """Opens the dialog to get user details and starts the brainstorming session."""
        dialog = UserDetailsDialog(self)
        details = dialog.get_details()

        if not details:
            self.logger.info("User cancelled the session setup. Closing application.")
            self.destroy()
            return
        
        self.logger.info("Starting session with user details...")
        first_question = self.answer_generator.start_session(**details)
        
        self.add_chat_message(f"Great, {details['name']}! Let's begin. Here is your first question:", "ai")
        self.add_chat_message(first_question, "ai")
        
        # Enable the input fields now that the session has started
        self.response_entry.configure(state="normal")
        self.response_entry.delete("1.0", "end")
        self.send_button.configure(state="normal")

    def send_user_message(self):
        """Handles sending the user's reply to the backend."""
        user_input = self.response_entry.get("1.0", "end-1c").strip()
        if not user_input:
            return

        self.add_chat_message(user_input, "user")
        self.response_entry.delete("1.0", "end")

        # Disable input while waiting for the AI's response
        self.response_entry.configure(state="disabled")
        self.send_button.configure(state="disabled")
        self.update_idletasks() # Ensure UI updates

        # Call the backend chat method
        ai_response = self.answer_generator.chat(user_input)
        
        self.add_chat_message(ai_response, "ai")

        # Re-enable input unless the session is complete
        if self.answer_generator.conversation_stage != "COMPLETED":
            self.response_entry.configure(state="normal")
            self.send_button.configure(state="normal")

    def add_chat_message(self, message, user_type):
        """Helper function to add a message to the chat history frame."""
        if user_type == "ai":
            anchor, avatar, fg_color = "w", "🤖", "#F3F3F3"
        else: # user
            anchor, avatar, fg_color = "e", "🗣️", "#E1F0FF"
        
        message_frame = ctk.CTkFrame(self.chat_history_frame, fg_color="transparent")
        message_frame.pack(anchor=anchor, pady=5, padx=10, fill="x")

        # Make the user's message align right
        if user_type == "user":
            message_frame.grid_columnconfigure(0, weight=1)

        avatar_label = ctk.CTkLabel(message_frame, text=avatar, width=30, height=30, font=ctk.CTkFont(size=20))
        message_label = ctk.CTkLabel(message_frame, text=message, fg_color=fg_color, corner_radius=10, padx=10, pady=5, wraplength=500, justify="left")
        
        if user_type == "ai":
            avatar_label.grid(row=0, column=0, sticky="n")
            message_label.grid(row=0, column=1, padx=10, sticky="w")
        else:
            message_label.grid(row=0, column=0, padx=10, sticky="e")
            avatar_label.grid(row=0, column=1, sticky="n")
