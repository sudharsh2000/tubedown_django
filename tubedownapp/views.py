import os

from celery.result import AsyncResult
from django.http import FileResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tubedownapp.serializers import DownloadSerializer
from tubedownapp.tasks import download_video, download_audio
class home(APIView):
    def get(self, request):
        return Response({'message': 'Welcome to TubeDownApp!'})

class DownloadApiview(APIView):

    def post(self, request):

        serializer = DownloadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        url = serializer.validated_data["link"]
        file_format = serializer.validated_data["format"]

        try:

            if file_format == "mp4":

                resolution = serializer.validated_data.get(
                    "resolution",
                    720
                )

                task = download_video.delay(
                    url,
                    resolution
                )
                print(f"Task ID: {task.id}")

                return Response(
                    {
                        "message": "Download started",
                        "task_id": task.id
                    },
                    status=status.HTTP_202_ACCEPTED
                )

            elif file_format == "mp3":
                task = download_audio.delay(
                    url
                )

                return Response(
                    {
                        "message": "Download started",
                        "task_id": task.id
                    },
                    status=status.HTTP_202_ACCEPTED
                )

            else:

                return Response(
                    {
                        "error": "Invalid format."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class DownloadStatusAPIView(APIView):

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        if task.state == "PENDING":
            return Response({
                "status": "pending"
            })

        if task.state == "STARTED":
            return Response({
                "status": "downloading"
            })

        if task.state == "SUCCESS":
            return Response({
                "status": "completed"
            })

        if task.state == "FAILURE":
            return Response({
                "status": "failed",
                "error": str(task.result)
            })

        return Response({
            "status": task.state.lower()
        })
class DownloadFileAPIView(APIView):

    def get(self, request, task_id):

        task = AsyncResult(task_id)

        if task.state != "SUCCESS":
            return Response(
                {
                    "error": "File is not ready."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        result = task.result

        file_path = result["file_path"]
        title = result["title"]

        if not os.path.exists(file_path):
            return Response(
                {
                    "error": "File not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        response = FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=f"{title}.mp4",
            content_type="video/mp4"
        )

        return response