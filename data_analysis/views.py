from django.shortcuts import render
import os
# Create your views here.
def home(request):
    module_dir = os.path.dirname(__file__)
    print module_dir
    # file_path = os.path.join(module_dir,'static\info\info.log')
    return render(request,"data_analysis.html")
