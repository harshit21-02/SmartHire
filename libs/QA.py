### FOR QA GENERATION
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0.7, max_tokens = 1500)

qa_prompt_template = '''Create 5 Unique, conceptual questions for screening interview using the following Job Description: {jobdescription} 
and the following Resume Details of a Candidate: {resume}. Ask Questions that mainly focuses on candidate's experience and skills and how they will use it to fulfill the requirements in Job Description.'''

qa_chain = LLMChain(
    llm=qa_llm,
    prompt=PromptTemplate.from_template(qa_prompt_template)
)

qa_text = qa_chain.predict(jobdescription = job_desc,resume = resume)

final_questions = qa_text.split('\n')