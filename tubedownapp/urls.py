from django.urls import path

from tubedownapp.views import DownloadApiview, DownloadStatusAPIView, DownloadFileAPIView, home

urlpatterns = [
    path('download/', DownloadApiview.as_view(), name='download'),
    path('download/status/<str:task_id>/',DownloadStatusAPIView.as_view(), name='download_status'),
    path('download/file/<str:task_id>/',DownloadFileAPIView.as_view(), name='download_file'),
    path('', home, name='home')

]