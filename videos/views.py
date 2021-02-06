from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .serializers import *
from rest_framework.response import Response
from .models import * 
from django.db.models import Q
from .utils import *

@api_view(['POST'])
def getVideosList(request):
    respV=[]
    try:    
        topics = request.data.get('topics').split(",")
        lang=request.data.get('lang').split(",")
        keyword=request.data.get('keyword',None)
        btopics=request.data.get('bookmarked topics').split(",")
        start=(int(request.data.get('page'))*10)-10
        end=start+int(request.data.get('count'))
    except Exception as e:
        return Response({'success':False}, status=status.HTTP_400_BAD_REQUEST)
    filteredtopics = []
    print(topics,btopics)
    try:
        for char in range(len(topics)):
            flag=True
            for charbt in range(len(btopics)):
                if topics[char] == btopics[charbt]:
                    flag=False
                    break;
            if flag== True:
                filteredtopics.append(topics[char])
        if keyword:
            bvideos= VideosTopics.objects.filter(Q(topic_id__in=btopics),Q(video_id__lang__in=lang), Q(video_id__name__icontains=keyword) | Q(video_id__description__icontains=keyword)).values("video_id")
            videos= VideosTopics.objects.filter(Q(topic_id__in=filteredtopics),Q(video_id__lang__in=lang), Q(video_id__name__icontains=keyword) | Q(video_id__description__icontains=keyword)).order_by('-video_id__upload_date').values("video_id")
        else:
            bvideos= VideosTopics.objects.filter(Q(topic_id__in=btopics),Q(video_id__lang__in=lang)).values("video_id")
            videos= VideosTopics.objects.filter(Q(topic_id__in=filteredtopics),Q(video_id__lang__in=lang)).order_by('-video_id__upload_date').values("video_id")
        for video in bvideos:
            respV.append(video['video_id'])
        for video in videos:
            respV.append(video['video_id'])
        respV=respV[start:end]
    except Exception as e:
        print(e)
        return Response({'success':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({'success':True,'Video List':respV}, status=status.HTTP_200_OK)

@api_view(['POST'])
def getVideo(request):
    try:
        id = request.data.get('id')
    except Exception as e:
        return Response({'success':False}, status=status.HTTP_400_BAD_REQUEST)
    try:
        video= Videos.objects.get(video_id=id)
        videotopics=VideosTopics.objects.filter(video_id=video)
        return Response({'success':True, 'Videos':prepareVideoResponsePacket(video,videotopics)}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'success':False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

