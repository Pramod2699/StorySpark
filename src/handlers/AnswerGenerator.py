from src.helpers.OpenAIHelper import AIHelper
from src.helpers.PromptTemplate import PromptTemplate
from src.utils.Logger import Logger
from src.config.ConfigHelper import ConfigHelper

class AnswerGenerator:
    """
    Manages the multi-step conversation for essay brainstorming.
    This class guides the user through a series of personalized questions
    and generates a final essay outline based on their answers.
    """
    def __init__(self):
        self.__config = ConfigHelper().config
        self.__logger = Logger()
        self.__prompt_template = PromptTemplate(self.__logger)
        self.__ai_helper = AIHelper(config=self.__config)
        
        # State management for the conversation
        self.reset_state()

    def reset_state(self):
        """Resets the conversation to its initial state."""
        self.__logger.info("Resetting conversation state.")
        self.conversation_stage = "AWAITING_USER_DETAILS"
        self.user_details = {}
        self.questions = []
        self.answers = []

    def start_session(self, name: str, stream: str, major: str, college: str) -> str:
        """
        Starts a new brainstorming session with the user's details and returns the first question.
        """
        self.reset_state()
        self.user_details = {
            "name": name,
            "education_stream": stream,
            "major": major,
            "college_name": college,
        }
        self.__logger.info(f"New session started for: {self.user_details}")
        return self._generate_first_question()

    def chat(self, user_input: str) -> str:
        """
        Main method to handle the user's message. It routes the input
        to the appropriate handler based on the current conversation stage.
        """
        self.__logger.info(f"Current conversation stage: {self.conversation_stage}")

        if self.conversation_stage == "AWAITING_USER_DETAILS":
            # In a real application, you'd parse this from the UI.
            # For this example, we'll assume the initial input contains the details.
            # Example input: "Pramod, IT, AI/ML, MIT"
            try:
                name, stream, major, college = [item.strip() for item in user_input.split(',')]
                self.user_details = {
                    "name": name,
                    "education_stream": stream,
                    "major": major,
                    "college_name": college,
                }
                self.__logger.info(f"User details captured: {self.user_details}")
                return self._generate_first_question()
            except ValueError:
                self.reset_state()
                return "Sorry, I didn't understand that. Please provide your details in the format: Name, Stream, Major, College Name"

        elif self.conversation_stage == "AWAITING_ANSWER_1":
            self.answers.append(user_input)
            return self._generate_second_question()

        elif self.conversation_stage == "AWAITING_ANSWER_2":
            self.answers.append(user_input)
            return self._generate_third_question()

        elif self.conversation_stage == "AWAITING_ANSWER_3":
            self.answers.append(user_input)
            return self._generate_final_outline()

        else:
            self.reset_state()
            return "Thank you! The session is complete. Please start a new session to begin again."

    def _generate_first_question(self) -> str:
        """Generates and returns the first personalized question."""
        self.__logger.info("Generating the first question.")
        prompt = self.__prompt_template.generate_snapshot_question_prompt(
            name=self.user_details["name"],
            education_stream=self.user_details["education_stream"],
            major=self.user_details["major"]
        )
        question = self.__ai_helper.genrate_from_prompt(
            model=self.__config['openai']['models']['default'],
            prompt=prompt
        )
        self.questions.append(question)
        self.conversation_stage = "AWAITING_ANSWER_1"
        return question

    def _generate_second_question(self) -> str:
        """Generates and returns the second personalized question."""
        self.__logger.info("Generating the second question.")
        prompt = self.__prompt_template.generate_lesson_question_prompt(
            name=self.user_details["name"],
            education_stream=self.user_details["education_stream"],
            first_answer=self.answers[0]
        )
        question = self.__ai_helper.genrate_from_prompt(
            model=self.__config['openai']['models']['default'],
            prompt=prompt
        )
        self.questions.append(question)
        self.conversation_stage = "AWAITING_ANSWER_2"
        return question

    def _generate_third_question(self) -> str:
        """Generates and returns the third personalized question."""
        self.__logger.info("Generating the third question.")
        prompt = self.__prompt_template.generate_blueprint_question_prompt(
            name=self.user_details["name"],
            college_name=self.user_details["college_name"],
            second_answer=self.answers[1]
        )
        question = self.__ai_helper.genrate_from_prompt(
            model=self.__config['openai']['models']['default'],
            prompt=prompt
        )
        self.questions.append(question)
        self.conversation_stage = "AWAITING_ANSWER_3"
        return question

    def _generate_final_outline(self) -> str:
        """Generates and returns the final essay outline."""
        self.__logger.info("Generating the final essay outline.")
        
        # The essay prompt is hardcoded as per the project requirements.
        essay_prompt = "How has your life experience contributed to your personal story—your character, values, perspectives, or skills—and what you want to pursue at this college?"

        prompt = self.__prompt_template.generate_essay_outline_prompt(
            essay_prompt=essay_prompt,
            answer_1=self.answers[0],
            answer_2=self.answers[1],
            answer_3=self.answers[2]
        )
        outline = self.__ai_helper.genrate_from_prompt(
            model=self.__config['openai']['models']['default'],
            prompt=prompt
        )
        self.conversation_stage = "COMPLETED"
        return f"Excellent! Here is the structured outline for your essay:\n\n{outline}"
