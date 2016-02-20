from django.shortcuts import render
#from django.views.generic import TemplateView
# Create your views here.

#class IndexView(TemplateView):
#    template_name = 'index.html'
    
def index(request):
   return render(request, 'salestda/index.html')