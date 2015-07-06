import logging
import os


from app.models import Job
from django.conf import settings


from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check jobs status'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        jobs = Job.objects.filter(Status = Job.RUNNING)
        for job in jobs:
            job_output_dir = os.path.join(settings.CAF_OUTPUT, job.get_output_dir())
            error_file = os.path.join(job_output_dir, 'error')
            pid_file = os.path.join(job_output_dir, 'pid')

            if os.path.exists(error_file):
                job.Status = Job.FAILURE
                job.save()
                continue
            
            if os.path.exists(pid_file):
                continue
                
            job.Status = Job.SUCCESS
            job.save()  





