from typing import Optional
import ast


class PromptTemplate:
    def __init__(self, logger):
        self.__loggerObj = logger

    def generate_snapshot_question_prompt(self, name: str, education_stream: str, major: Optional[str] = None) -> str:
        """
        Generates a prompt to create the FIRST personalized question (The Snapshot Moment).
        Args:
            name (str): The student's name.
            education_stream (str): The student's general field (e.g., STEM, Humanities, Arts).
            major (Optional[str]): The student's specific major, if provided.
        Returns:
            str: A prompt for the LLM to generate a personalized question.
        """
        prompt = f"""
You are an expert and creative college essay coach. Your task is to generate one single, inspiring brainstorming question for a student named {name}.

**Student's Profile:**
- **Name:** {name}
- **Educational Stream:** {education_stream}
- **Major:** {major or 'Not specified'}

**Your Goal:**
Generate a question that asks the student about a specific past moment, project, or challenge they faced. The question's tone and vocabulary should be tailored to their educational stream. For a STEM student, use words like 'problem,' 'experiment,' or 'build.' For a Humanities student, use words like 'idea,' 'story,' or 'perspective.'

**Instructions:**
- The output must be ONLY the question itself.
- Do not add any introductory text like "Here is your question:".
- The question should be encouraging and open-ended.

**Generated Question:**
        """
        return prompt

    def generate_lesson_question_prompt(self, name: str, education_stream: str, first_answer: str) -> str:
        """
        Generates a prompt to create the SECOND personalized question (The Core Lesson).
        Args:
            name (str): The student's name.
            education_stream (str): The student's field.
            first_answer (str): The student's answer to the first question.
        Returns:
            str: A prompt for the LLM to generate a personalized follow-up question.
        """
        prompt = f"""
You are an expert and insightful college essay coach. You are in a conversation with a student named {name} from the {education_stream} stream.

**The student just told you this story:**
"{first_answer}"

**Your Task:**
Generate one single, thoughtful follow-up question. The question must ask the student to reflect on the deeper lesson, value, or skill they learned from that specific experience. Tailor the language to their stream.

**Instructions:**
- The output must be ONLY the question itself.
- Do not add any introductory text.
- The question should logically follow their story and prompt introspection.

**Generated Question:**
        """
        return prompt
        
    def generate_blueprint_question_prompt(self, name: str, college_name: str, second_answer: str) -> str:
        """
        Generates a prompt to create the THIRD personalized question (The Future Blueprint).
        Args:
            name (str): The student's name.
            college_name (str): The name of the college the student is applying to.
            second_answer (str): The student's answer about the lesson they learned.
        Returns:
            str: A prompt for the LLM to generate a final personalized question.
        """
        prompt = f"""
You are an expert and forward-thinking college essay coach talking to {name}.

**The student just shared this core lesson/value they learned:**
"{second_answer}"

**Your Task:**
Generate one single, final question that asks the student to connect this specific lesson to their future at **{college_name}**. The question should prompt them to describe a tangible contribution or action they want to take on campus.

**Instructions:**
- The output must be ONLY the question itself.
- Do not add any introductory text.
- The question must be action-oriented and specific to the college.

**Generated Question:**
        """
        return prompt

    def generate_essay_outline_prompt(self, essay_prompt: str, answer_1: str, answer_2: str, answer_3: str) -> str:
        """
        Generates a final prompt to synthesize all answers into a structured essay outline.
        Args:
            essay_prompt (str): The original essay prompt the student is working on.
            answer_1 (str): The student's answer about their "snapshot moment".
            answer_2 (str): The student's answer about their "core lesson".
            answer_3 (str): The student's answer about their "future blueprint".
        Returns:
            str: A prompt for the LLM to generate the final essay outline.
        """
        prompt = f"""
You are an expert college essay coach. Your task is to analyze a student's answers to three brainstorming questions and generate a compelling 350-word essay structure for the following essay prompt: "{essay_prompt}"

**Student's Brainstorming Answers:**

1.  **Story/Snapshot Moment:**
    "{answer_1}"

2.  **Core Lesson Learned:**
    "{answer_2}"

3.  **Future Blueprint/Goal at College:**
    "{answer_3}"

**Your Task:**
Based ONLY on the answers provided, create a strategic, 4-part essay outline. The outline should guide the student on how to write a powerful and coherent essay.

**Output Instructions:**
- The total word count of the structure should be exactly 350 words.
- Structure the output into four distinct sections:
  1. **The Hook:** An engaging opening based on their story.
  2. **The Action:** The main narrative of their experience.
  3. **The Reflection:** A section focusing on the lesson they learned.
  4. **The Bridge to the Future:** A conclusion connecting their lesson to their college goal.
- Assign an approximate word count to each section (e.g., *Approx. 50 words*).
- For each section, provide 1-2 bullet points of clear, actionable advice on what to write.
- The tone should be strategic, encouraging, and clear.
- Do not include any introductory text. Begin directly with the title of the outline.
        """
        return prompt