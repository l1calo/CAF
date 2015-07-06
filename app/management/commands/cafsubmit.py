import logging
import os
import shutil
import sh
import stat
import subprocess
from contextlib import nested

from app.selector import Selector
from app.models import Analysis, Run, Job
from django.conf import settings
from app import eos


from django.db.models import Max
from django.core.management.base import BaseCommand
from django.template.loader import get_template


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Submit jobs'

    def add_arguments(self, parser):
        pass

    def submit(self, run, analysis, cfg):
        ana_name, ana_template, ana_context, ana_post_exec = (
            cfg['name'],
            cfg['template'],
            cfg.get('context',{}),
            cfg.get('post_exec',None)
        )
        logger.info('Create job for run %d, analysys %s' %
                    (run.RunNumber, ana_name))

        job = Job(Run=run, Analysis=analysis)
        job.save()

        # Create directory
        job_dir = os.path.join(
            settings.CAF_OUTPUT,
            "%08d_%s_%d" % (run.RunNumber, ana_name, job.id)
        )
        try:
            os.makedirs(job_dir)
        except:
            logger.exception("Could not create directory %s", job_dir)
            job.delete()
            return 

        # Copy files for job
        tmpl = get_template('joboptions/%s.py.tmpl' % ana_template)
        ana_context.update({'files': run.Files.all()})
        jobo = tmpl.render(ana_context)

        jopo_path = os.path.join(job_dir, 'jobo.py')
        with open(jopo_path, 'w') as f:
            f.write(jobo)
  
        post_exec = ''
        if ana_post_exec:
            post_exec = get_template('%s.sh.tmpl' % ana_post_exec).render(
                {
                    'BASE_DIR': settings.BASE_DIR
                }
            )

        launcher = get_template('launcher.sh.tmpl').render(
            {
                'athena_version': settings.CAF_ATHENA,
                'asetup': settings.CAF_ASETUP,
                'post_exec': post_exec,
                'BASE_DIR': settings.BASE_DIR
            }
        )
        
        launcher_path = os.path.join(job_dir, 'launcher.sh')
        with open(launcher_path, 'w') as f:
            f.write(launcher)
        st = os.stat(launcher_path)
        os.chmod(launcher_path, st.st_mode | stat.S_IEXEC)

        output_path = os.path.join(job_dir, 'stdout.log')
        err_path = os.path.join(job_dir, 'stderr.log')
        
        with nested(open(output_path, 'w'), open(err_path, 'w')) as (out, err):
            process = subprocess.Popen(launcher_path, cwd=job_dir, stdout=out, stderr=err)
            pid_path = os.path.join(job_dir, 'pid')
            with open(pid_path, 'w') as pid:
                pid.write(str(process.pid))
            job.IsLocal = True
            job.ExternalId = process.pid
            job.Status = Job.RUNNING
            job.save()
        #cmd(_out=output_path, _err=err_path, _bg=True)


    def handle(self, *args, **options):
        Job.objects.all().delete()
        for f in os.listdir(settings.CAF_OUTPUT):
            p = os.path.join(settings.CAF_OUTPUT, f)
            if os.path.isfile(p):
                os.unlink(p)
            elif os.path.isdir(p):
                shutil.rmtree(p)

        for analysis in Analysis.objects.all():
            logger.info("=" * 80)
            logger.info("Process %s analysis" % analysis.Name)
            runs_no_jobs = Run.objects.filter(
                Jobs__isnull=True,
                Analyses__id=analysis.id
            )

            if not runs_no_jobs:
                logger.info("No new runs")
                continue

            logger.info("New runs: %s" %
                        str([x.RunNumber for x in runs_no_jobs])
                        )

            for run in runs_no_jobs:
                self.submit(
                    run,
                    analysis,
                    settings.CAF_ANALYSES[analysis.Name]
                )
