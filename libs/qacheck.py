### FOR QA EVALUATION
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0.7, max_tokens = 1500)

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
    llm=qa_llm,
    prompt=PromptTemplate.from_template(ans_eval_prompt_template)
)

qa_eval_text = qa_eval_chain.predict(question = ques,answer = ans)