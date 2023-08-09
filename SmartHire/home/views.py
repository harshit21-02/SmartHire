from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import uuid
from .models import Job, Resume
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
# Create your views here.
import io
import json
from django.urls import reverse
# from .sort_resume import ResumeSearch

subscription_key = "9b7bc13b2fb0479c9ff6869409d9cdc1"
endpoint = "https://pibit-azure-ocr-paid.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key))


### FOR QA GENERATION -----------------------------------------
# from langchain import PromptTemplate, LLMChain
# from langchain.callbacks import get_openai_callback
# from langchain.chat_models import ChatOpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature = 0.7, max_tokens = 1500)

# qa_prompt_template = '''Create 5 Unique, conceptual questions for screening interview using the following Job Description: {jobdescription} 
# and the following Resume Details of a Candidate: {resume}. Ask Questions that mainly focuses on candidate's experience and skills and how they will use it to fulfill the requirements in Job Description.'''

# qa_chain = LLMChain(
#     llm=qa_llm,
#     prompt=PromptTemplate.from_template(qa_prompt_template)
# )
##########--------------------------------------




def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('resume')
        description = request.POST.get('description')
        
        job_instance = Job()
        job_instance.description = description
        job_instance.save()

        # Save the uploaded files to the model instance
        item_list=[]
        ranking=[]
        for file in files:
            resume_item = Resume(job=job_instance, file=file)
            resume_item.save()
            ranking.append(resume_item.id)
            item = pdf_to_text(resume_item)
            item_list.append(item)
            # print(item)

        # res_search = ResumeSearch()
        # top_10 = res_search.get_top_10(description, item_list)
        # ranking = res_search.rerank_resumes(description, top_10)
    
        for num in ranking:
            resume = Resume.objects.get(id=num)
            resume.shortlisted=True
            resume.save()
            print(resume.id)
        redirect_url = reverse('cv_ranking', kwargs={'pk': job_instance.id})
        return redirect(redirect_url)
    return render(request, 'index.html')


def cv_ranking(request, pk):

    job=Job.objects.get(id=pk)
    resume_list = Resume.objects.filter(job=job,shortlisted=True)

    for resume in resume_list:
        print(resume.id)

    return render(request, 'cv_ranking.html',{"resume": resume_list})



def pdf_to_text(resume):
        file_path = resume.file.path
        with open(file_path, "rb") as reader:
                    file = reader.read()
        reader = io.BytesIO(file)
        read_response = computervision_client.read_in_stream(reader, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        # Grab the ID from the URL
        operation_id = read_operation_location.split("/")[-1]

        # Call the "GET" API and wait for it to retrieve the results
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ["notStarted", "running"]:
                break

        textract_response=azure_to_aws(read_result)
        text_list = []
        for block in textract_response['Blocks']:
            if block['BlockType']=='WORD':
                    text_list.append(block['Text'])
        text = ' '.join(text_list)

        item = dict()
        item['id']=resume.id
        item['text']=text

        return item

def azure_to_aws(read_result):
    image_width = read_result.as_dict()["analyze_result"]["read_results"][0]["width"]
    image_height = read_result.as_dict()["analyze_result"]["read_results"][0]["height"]
    azure_response = read_result.as_dict()["analyze_result"]["read_results"][0]["lines"]
    textract_response = {
        "DocumentMetadata": {"Pages": 1},
        "Blocks": [],
        "AnalyzeDocumentModelVersion": "",
        "ResponseMetadata": {},
    }
    for line in azure_response:
        TextType = line["appearance"]["style"]["name"]
        if TextType == "handwritting":
            TextType = 'HANDWRITTING'
        else:
            TextType = 'PRINTED'
        for word in line["words"]:
            b_box = word["bounding_box"]
            x_coords = b_box[::2]
            y_coords = b_box[1::2]
            left = min(x_coords)
            top = min(y_coords)
            width = max(x_coords) - min(x_coords)
            height = max(y_coords) - min(y_coords)
            geometry = {
                "BoundingBox": {
                    "Width": width / image_width,
                    "Height": height / image_height,
                    "Left": left / image_width,
                    "Top": top / image_height,
                },
                "Polygon": [
                    {"X": x_coords[0] / image_width, "Y": y_coords[0] / image_height},
                    {"X": x_coords[1] / image_width, "Y": y_coords[1] / image_height},
                    {"X": x_coords[2] / image_width, "Y": y_coords[2] / image_height},
                    {"X": x_coords[3] / image_width, "Y": y_coords[3] / image_height},
                ],
            }
            block = {
                "BlockType": "WORD",
                "Geometry": geometry,
                "Text": word["text"],
                "Id": str(uuid.uuid4()),
                "Confidence": word["confidence"],
                "TextType": str(TextType),
            }
            textract_response["Blocks"].append(block)
    return textract_response