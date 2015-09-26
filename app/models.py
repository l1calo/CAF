from django.db import models


class Run(models.Model):
    RunNumber = models.IntegerField(primary_key=True)
    DAQConfiguration = models.TextField()
    TotalTime = models.IntegerField()
    EORTime = models.IntegerField()
    SORTime = models.IntegerField()
    L2Events = models.IntegerField()
    CleanStop = models.BooleanField()
    EFEvents = models.IntegerField()
    DetectorMask = models.TextField()
    RecordingEnabled = models.BooleanField()
    L1Events = models.IntegerField()
    T0ProjectTag = models.TextField()
    RunType = models.TextField()
    RecordedEvents = models.IntegerField()
    PartitionName = models.TextField()
    GainStrategy = models.TextField()
 
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    Type = models.ForeignKey("RunType", related_name='Runs')
    Listeners = models.ManyToManyField('Listener', related_name='Runs')
    Analyses = models.ManyToManyField('Analysis', related_name='Runs')


class Listener(models.Model):
    Name = models.CharField(max_length=255, unique=True)

class RunType(models.Model):
    Name = models.CharField(max_length=255, unique=True)


class Analysis(models.Model):
    Name = models.CharField(max_length=255, unique=True)

class File(models.Model):
    Run = models.ForeignKey(Run, related_name='Files')
    Path = models.CharField(max_length=1024, unique=True)

class Job(models.Model):
    NEW = 'NEW'
    RUNNING = 'RUNNING'
    FAILURE = 'FAILURE'
    SUCCESS = 'SUCCESS'

    STATUS_CHOISES = (
        (NEW, NEW),
        (RUNNING, RUNNING),
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE),
    )

    Run = models.ForeignKey("Run", related_name='Jobs')
    Analysis = models.ForeignKey("Analysis", related_name='Jobs')

    Status = models.CharField(max_length=10,
                              choices=STATUS_CHOISES,
                              default=NEW)
    IsLocal = models.BooleanField(default=True)
    ExternalId = models.IntegerField(default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    def get_output_dir(self):
        return "%08d_%s_%d" % (self.Run.RunNumber, self.Analysis.Name, self.id)

