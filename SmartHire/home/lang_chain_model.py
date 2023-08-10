#### JOB DESCRIPTION EVALUATION
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model_name="gpt-3.5-turbo-0613", temperature = 1, max_tokens = 1500)

###########################################################################################
# The code below is for Evaluating the Job Description
prompt_template_job_desc = '''Rate the Job Description that is being provided out of 10 on the and if you rate it below 9, Write a modified version 
of the job description to make it a 10/10. and also mention the changes that you made in the end: {jobdescription}.
The criteria to rate is that the following things should be mentioned in the job description: 
Job Title and Overview, Role and Responsibilities, Qualifications and Requirements, Reporting Structure and Team, Work Environment, 
Company Overview, Compensation and Benefits, Application Process, Contact Information, Geographic or Travel Requirements.

'''

eval_llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template_job_desc)
)
### This is text returned after evaluating the Job Description
def evaluate_description(job_desc):
    eval_text = eval_llm_chain(job_desc)   # Put the job description string in place job_desc
    return eval_text

###########################################################################################
## The code below is for Question Generation

qa_prompt_template = '''Create 5 Unique, conceptual questions for screening interview using the following Job Description: {jobdescription} 
and the following Resume Details of a Candidate: {resume}. Ask Questions that mainly focuses on candidate's experience and skills and how they will use it to fulfill the requirements in Job Description.'''

qa_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(qa_prompt_template)
)
### This outputs a string of questions after taking Job Description and Resume 
def get_question(job_desc,resume):
    qa_text = qa_chain.predict(jobdescription = job_desc,resume = resume)## Input Job description in place of job_desc and  Resume string in place of resume
    # This outputs a list of the 5 questions
    final_questions = qa_text.split('\n')
    return final_questions

###########################################################################################
# The code below is for Evaluating the interviewee's answer
ans_eval_prompt_template = '''You are given a screening interview question for a job (delimited by <qse></qse>) and a candidate's answer to that question (delimited by <ans></ans>). 
Evaluate the answer by checking the relevancy of the answer with respect to the question and give it a score on a scale of 1-10 and provide feedback for the answer:
------
<qse>
{question}
</qse>
------
<ans>
{answer}
</ans>
------
Rating and Feedback:'''

qa_eval_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(ans_eval_prompt_template)
)

# This outputs a string that Contains the rating and feedback for the answer to the question by candidate
def interview_response(ques,ans):
    qa_eval_text = qa_eval_chain.predict(question = ques,answer = ans) # Put question string in place of ques and answer string in place of ans.
    return qa_eval_text