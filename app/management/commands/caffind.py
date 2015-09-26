import logging
import os
import subprocess

from app import eos
from app.selector import Selector
from app.models import RunType, Listener, Run, Analysis, File

from django.conf import settings


from django.db.models import Max
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Find new calibration runs'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        selector = Selector(settings.CAF_SCANS["tdaqdbname"],
                            settings.CAF_SCANS["trigdbname"])

        for scan in settings.CAF_SCANS["scans"]:
            if not 'analyses' in scan:
                continue

            logger.info("=" * 40)
            logger.info("Scan for {0} runs".format(scan['name']))

            listener, _ = Listener.objects.get_or_create(Name=scan['name'])
            run_type, _ = RunType.objects.get_or_create(Name=scan['runtype'])
            analyses = []
            for a in scan.get('analyses', []):
                analysis, _ = Analysis.objects.get_or_create(Name=a)
                analyses.append(analysis)

            selector.set_selection(
                RunType=run_type.Name,
                PartitionName__in=scan.get('daqpartition', None),
                RecordingEnabled=scan.get('reconly', True),
                CleanStop=scan.get('cleanstop', True)
            )

            # Initial run
            max_run = Run.objects.filter(
                Listeners__id=listener.id).aggregate(Max("RunNumber"))
            run1 = max_run['RunNumber__max'] + \
                1 if max_run['RunNumber__max'] else scan["initialrun"]
            logger.info("Initial run #%d" % run1)
            runs = selector.runs_by_range(run1=run1)
            count = 0

            for run_number in runs:
                logger.info("Process run %d" % run_number)

                file_names = []
                for path in settings.CAF_SOURCE:
                    folder = path.format(run_number="%08d" % run_number)
                    run_folders = eos.ls(folder)
                    if run_folders:
                        raw_folder = None
                        for run_folder in run_folders:
                            if run_folder[:-1].endswith("RAW"):
                                raw_folder = os.path.join(
                                    folder, run_folder[:-1])
                                break
                        print(raw_folder)
                        if raw_folder:
                            file_names = eos.ls(raw_folder)
                            if file_names:
                                file_names = [
                                    "%s/%s/%s" % (settings.CAF_EOS_PREFIX,
                                                  raw_folder, f[:-1])
                                    for f in file_names
                                ]
                            break

                files = []
                if not file_names:
                    # Do nothing
                    logger.error("No files found for run %d" % run_number)
                    continue
                else:
                    logger.info("Files found %s for run %d" %
                                (str(file_names), run_number)
                                )

                runs[run_number]['Type'] = run_type
                run, created = Run.objects.get_or_create(**runs[run_number])

                if created:
                    for file_name in file_names:
                        file, _ = File.objects.get_or_create(Run=run,
                                                             Path=file_name)

                if not run.Listeners.filter(id=listener.id):
                    run.Listeners.add(listener)
                    count += 1

                for analysis in analyses:
                    if not run.Analyses.filter(id=analysis.id):
                        run.Analyses.add(analysis)

                    # run.save()
                run.delete()
            if runs:
                logger.info("Runs: %s" %
                            str(sorted(runs.keys(), reverse=True)))
            logger.info("New runs %d" % count)
