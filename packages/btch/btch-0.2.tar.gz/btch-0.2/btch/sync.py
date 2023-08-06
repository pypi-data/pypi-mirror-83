from .job import search_jobs, JobStatus, update_job_status
from boto3 import client
from .logger import logger

MAX_JOBS_CHUNK = 80

batch_client = client("batch")

def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def sync_jobs():
    transient_statuses = [x for x in JobStatus if x.value[1]]
    outstanding_jobs = [ x[0] for x in search_jobs(*transient_statuses)]
    for ids in chunk(outstanding_jobs, MAX_JOBS_CHUNK):
        logger.info(f"Fetching fresh statuses for: {len(ids)} jobs")
        for job in batch_client.describe_jobs(jobs = ids)["jobs"]:
            status = next(x for x in JobStatus if x.value[0] == job["status"])
            update_job_status(job["jobId"], status = status)