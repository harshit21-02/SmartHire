#### JOB DESCRIPTION EVALUATION
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

eval_llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature = 0.7, max_tokens = 1500)

prompt_template = '''Rate the Job Description that is being provided out of 10 on the and if you rate it below 9, Write a modified version 
of the job description to make it a 10/10. and also mention the changes that you made in the end: {jobdescription}.
The criteria to rate is that the following things should be mentioned in the job description: 
Job Title and Overview, Role and Responsibilities, Qualifications and Requirements, Reporting Structure and Team, Work Environment, 
Company Overview, Compensation and Benefits, Application Process, Contact Information, Geographic or Travel Requirements.

'''

eval_llm_chain = LLMChain(
    llm=eval_llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

eval_text = eval_llm_chain(job_desc)

print(eval_text['text'])