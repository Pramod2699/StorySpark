# StorySpark ✨  

Transform your life experiences into powerful college application essays with the help of AI.  

---

## 🌟 Why StorySpark?  

Writing a personal statement is one of the toughest challenges for students. Between the pressure to stand out, writer’s block, and uncertainty about which stories matter most, many end up with generic essays that fail to capture their unique voice.  

**StorySpark** changes that. It’s a conversational AI tool that acts as your brainstorming partner—helping you reflect on meaningful experiences, uncover your personal narrative, and structure it into a compelling essay plan.  

Unlike static templates, StorySpark adapts to *you*—your background, academic interests, and goals—through an interactive dialogue. By guiding you step by step, it transforms a daunting task into a journey of self-discovery.  

---

## 🚀 How It Works  

1. **Personalized Setup**  
   Enter your name, academic stream, major, and target college. StorySpark uses this to generate your first tailored question.  

2. **Guided Conversation**  
   Answer three rounds of AI-driven questions designed to surface meaningful experiences and insights.  

3. **Essay Blueprint**  
   StorySpark converts your responses into a structured 350-word essay outline, complete with headings, bullet points, and suggested word counts—delivered in a rich-text editor.  

The result: a clear, strategic foundation to write your essay confidently in your own voice.  

---

## ✨ Key Features  

- 🤖 **AI-Powered Interview** – Dynamic, personalized questions instead of generic forms.  
- 🗣️ **Conversational Flow** – Explore past experiences, reflect on lessons, and connect them to future goals.  
- 📝 **Rich-Text Output** – Professionally formatted outlines with headings and bullet points.  
- 🌐 **Modern Web Interface** – Simple, responsive, and distraction-free.  
- 🐍 **Robust Backend** – Built on FastAPI for speed and reliability.  

---

## 🛠️ Tech Stack  

**Backend**  
- Python 3.10+  
- FastAPI & Uvicorn (API & server)  
- OpenAI GPT-4o (LLM)  
- Pydantic (data validation)  

**Frontend**  
- HTML5  
- Tailwind CSS (styling)  
- Vanilla JavaScript (logic & API calls)  
- Quill.js (rich-text editor)  
- Marked.js (Markdown → HTML rendering)  

---

## ⚙️ Installation  

### Prerequisites  
- Python 3.10+  
- `pip` or `uv` package manager  
- OpenAI API key  

### Setup  

Clone the repository:  
```bash
git clone https://github.com/your-username/StorySpark.git
cd StorySpark
```

Create a virtual environment and activate it:  
```bash
python -m venv .venv

# On Windows
.\.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

Install dependencies:  
```bash
pip install -r requirements.txt
# or
uv pip install -r requirements.txt
```

Add your OpenAI API key:  
- Open `src/config/config.json`  
- Insert your key under `credentials`  

Run the backend server:  
```bash
uvicorn app:app --reload
```

Launch the frontend:  
- Open `index.html` in your browser  

---

## 📁 Project Structure  

```
StorySpark/
├── .venv/              
├── src/                
│   ├── config/         
│   │   └── config.json 
│   ├── handlers/       
│   │   └── AnswerGenerator.py
│   ├── helpers/        
│   │   ├── OpenAIHelper.py
│   │   └── PromptTemplate.py
│   └── utils/          
│       └── Logger.py
├── app.py              # FastAPI backend
├── index.html          # Frontend UI
└── README.md
```

---

## 🎯 Outcome  

StorySpark doesn’t write your essay for you. Instead, it gives you a **clear, well-structured outline**—a personalized blueprint to help you write authentically, with confidence and clarity.  
