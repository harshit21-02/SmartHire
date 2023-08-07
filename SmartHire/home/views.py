from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .models import Resume
# Create your views here.

def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        # Create a new instance of MyModel
        my_model_instance = Resume()
        my_model_instance.save()

        # Save the uploaded files to the model instance
        for file in files:
            print(file)
            my_model_instance.files.add(file)
        # Process the uploaded files here (e.g., save to a folder or perform other operations)

    return render(request, 'index.html')
