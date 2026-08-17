from django.shortcuts import render

def knowledge_hub(request):
    # Dynamic or pre-defined clinical articles for the patient resource library
    # Organized to avoid screen fatigue (clear text layout)
    return render(request, 'knowledge_hub.html')
