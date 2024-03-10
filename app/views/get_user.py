from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from app.models import Location,User,StateTechnical,DistrictTechnical,TechnicalStaff

from rest_framework.views import APIView
   
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ListSerializer, ValidationError

from app.serializers.UserSerializer import UserSerializer
from app.serializers.LocationSerializer import LocationSerializer

import json
from urllib.parse import unquote


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPersonalDetails(request):
    try:
        user= request.user
        serializer = UserSerializer(user,many= False)
        return Response({"user":serializer.data})
    except Exception as e:
        print("GetUser ERR",e)
        return Response({"messages":"Error"},status=500)

def getUserByType(user_ref, filter):

    USER = {
        "user_type":"user"
    }
    ResponseData = []



    # UserSerializer with ListSerializer
    user_list = User.objects.filter(**filter)
    print(user_list)
    Userdata = UserSerializer(user_list, many=True)
    ResponseData += list(Userdata.data)

    return ResponseData

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserALL(request):
    if request.user.user_type == "technical":
        # Check Role

        try:
            # print("params",type(request.query_params.get("name")))
            # Get the encoded filter from the query parameters
            encoded_filter = request.query_params.get('filter', None)
            decoded_filter = {}
            try:
                # Decode and parse the JSON filter
                decoded_filter = json.loads(unquote(encoded_filter))
            except:
                decoded_filter = {}

            print("decoded_filter",decoded_filter)

            # Check if the decoded filter is a dictionary
            if not isinstance(decoded_filter, dict):
                decoded_filter={}

            ResponseData=getUserByType(request.user,decoded_filter)
            return Response(ResponseData)
        
        except Exception as e:
            print("Error", e)
            error_response = {
                'status': 500,
                'error': 'Check Filter',
                'message': 'Internal server error',
                'data': {}
            }
            return Response(error_response, status=500)
    else:
        error_response = {
                'status': 500,
                'error': 'Only Technical Team',
                'message': 'Internal server error',
                'data': {}
            }
        return Response(error_response, status=500)