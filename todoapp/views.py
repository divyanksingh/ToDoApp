from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from datetime import datetime

@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        try:
            sequence = data.get('sequence')
            if sequence <= 0:
                raise ValueError
            start = datetime.now()
            result = fib(sequence)                
            end = datetime.now()
            time_taken = end - start
            return HttpResponse(json.dumps({"sequence_member": result, "time_taken": time_taken.total_seconds()*1000}))
        except ValueError as ve:
            return HttpResponse(json.dumps({"message": "Input sequence number should be greater than 0"}), status = 422)


    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))
