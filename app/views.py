from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.conf import settings
from collections import defaultdict
import os
import re
import logging
import mimetypes
from django.http import FileResponse

from app.models import Job

logger = logging.getLogger(__name__)

mimetypes.add_type('text/plain','.log')

def index(request):

    jobs = Job.objects.order_by('-Updated')
    rows = []
    for job in jobs:
        files = settings.CAF_ANALYSES.get(job.Analysis.Name,{}).get('files',[])
        row = {'job': job, 'files': files}
        rows.append(row)

    return render_to_response('index.html', {'rows': rows})

def job_file(request, jobid, file):
    job = get_object_or_404(Job, pk=jobid)
    ana = job.Analysis.Name
    nrun = job.Run.RunNumber
    name = "%08d_%s_%d" % (nrun, ana, job.id)
    file_name = os.path.join(settings.CAF_OUTPUT, name, file)
    mime = mimetypes.guess_type(file)
    return FileResponse(open(file_name, 'rb'), content_type=mime[0])
