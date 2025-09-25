from django.shortcuts import render

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Job
from rest_framework import generics
from .models import Job
from .serializers import JobSerializer
class JobListView(ListView):
    model = Job
    template_name = 'posts/job_list.html'
    context_object_name = 'jobs'  # default is object_list

class JobDetailView(DetailView):
    model = Job
    template_name = 'posts/job_detail.html'
    context_object_name = 'job'

class JobCreateView(CreateView):
    model = Job
    template_name = 'posts/job_form.html'
    fields = [
        'title', 'description', 'status', 'jobtype', 'jobtime',
        'shift', 'required_skills', 'domain'
    ]
    success_url = reverse_lazy('job_list')

class JobUpdateView(UpdateView):
    model = Job
    template_name = 'posts/job_form.html'
    fields = [
        'title', 'description', 'status', 'jobtype', 'jobtime',
        'shift', 'required_skills', 'domain'
    ]
    success_url = reverse_lazy('job_list')

class JobDeleteView(DeleteView):
    model = Job
    template_name = 'posts/job_confirm_delete.html'
    success_url = reverse_lazy('job_list')


class JobListCreateAPIView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
