# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
import os

data_loc = os.curdir + "/DataFolder"

#Have to think about how im setting this up... models etc

# Create your views here.
def index(request):
    return HttpResponse("This is where the app might spawn?")

def runapp(request, func):
    function_name = str(func)
    function_manifest = "manifest_of_" + function_name + ".py.txt"
    folder = data_loc + "/" + function_name + "/"
    filename = folder + function_manifest
    text_file = open(filename, 'r').read()#str(os.listdir(data_loc))
    return HttpResponse("Running Application: " + function_name + " Pulling from: " + folder + " Computing file: " + filename + " Manifest contains: " + text_file)
