from os import makedirs, environ, getcwd
from datetime import datetime
from os.path import isfile
from json import loads
from secrets import token_bytes
from base64 import b32encode, b64decode
from functools import cache
from boto3 import client
from docker import from_env
from sqlite3 import connect, Row

from .logger import logger

DOCKER = from_env()
ECR = client("ecr")
BATCH = client("batch")

def _generate_uuid():
    random_str = b32encode(token_bytes(10)).decode("utf-8").lower()
    return f"u{random_str}"

@cache
def _get_job_db():
    makedirs(".btch", exist_ok = True)
    conn = connect(".btch/jobdb")
    conn.row_factory = Row
    logger.debug(f"Ensuring job_db table is created.")
    conn.cursor().execute(f"""
        CREATE TABLE IF NOT EXISTS job (
            group_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            aws_job_id TEXT NOT NULL,
            status TEXT NULL,
            aws_log_stream TEXT NULL,
            last_created_at TIMESTAMP NOT NULL,
            last_updated_at TIMESTAMP NOT NULL,
            PRIMARY KEY(group_id, tag)
        );
    """)
    conn.cursor().execute(f"""
        CREATE UNIQUE INDEX IF NOT EXISTS aws_job_id_ix ON job(aws_job_id);
    """)
    conn.commit()
    return conn

@cache
def _get_json_config():
    with open("btch.json") as f:
        return loads(f.read())

def _get_cpu():
    return _get_json_config()["cpu"]

def _get_memory():
    return _get_json_config()["memory"]

def _get_job_queue():
    return environ["JOB_QUEUE"]

def _get_ecr_repository_name():
    return environ["REPO_NAME"]

def _get_role_arn():
    return environ["ROLE_ARN"]

@cache
def _setup_project_uuid():
    makedirs(".btch", exist_ok = True)
    if not isfile(".btch/uuid"):
        uuid = _generate_uuid()
        logger.debug(f"Setting project UUID: {uuid}.")
        with open(".btch/uuid", "w") as f:
            f.write(uuid)

@cache
def _get_project_uuid():
    _setup_project_uuid()
    with open(".btch/uuid") as f:
        return f.read()

@cache
def _get_authorization_details():
    logger.info("Fetching container registry auth details.")
    token = ECR.get_authorization_token()
    username, password = b64decode(token['authorizationData'][0]['authorizationToken']).decode().split(':')
    registry = token['authorizationData'][0]['proxyEndpoint'][8:]
    return (username, password, f"{registry}/{_get_ecr_repository_name()}")

def _get_docker_image_tag():
    _user, _pass, repository = _get_authorization_details()
    return f"{repository}:{_get_project_uuid()}"

def _build_docker_image():
    logger.info(f"Building image: {_get_docker_image_tag()}.")
    DOCKER.images.build(
        tag = _get_docker_image_tag(),
        quiet = False,
        path = getcwd()
    )

def _push_docker_image():
    logger.info(f"Pushing image: {_get_docker_image_tag()}.")
    username, password, repository = _get_authorization_details()
    DOCKER.login(username = username, password = password, registry = repository)
    DOCKER.images.push(repository, tag = _get_project_uuid())
    
def _register_job_definition():
    logger.info(f"Registering job definition: {_get_project_uuid()}.")
    BATCH.register_job_definition(
        jobDefinitionName = _get_project_uuid(),
        type = "CONTAINER",
        containerProperties = dict(
            image = _get_docker_image_tag(),
            vcpus = _get_cpu(),
            memory = _get_memory(),
            command = ["echo", "hello world"],
            jobRoleArn = _get_role_arn(),
            executionRoleArn = _get_role_arn()
        )
    )["jobDefinitionArn"]

def _submit_job(command, group_id, tag):
    cmd_str = " ".join(command)
    job_id = f"{group_id}:{tag}"
    logger.info(f"Submitting job: {job_id} with command: {cmd_str}.")
    aws_job_id = BATCH.submit_job(
        jobName = tag,
        jobQueue = _get_job_queue(),
        jobDefinition = _get_project_uuid(),
        containerOverrides = dict(
            command = command,
            environment = [dict(name = "JOB_ID", value = job_id)]
        )
    )["jobId"]
    db = _get_job_db()
    db.cursor().execute(f"""
        INSERT INTO job VALUES (?,?,?,NULL,NULL,?,?);
    """,(group_id, tag, aws_job_id, datetime.utcnow(), datetime.utcnow()))
    db.commit()

def _chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def _sync():
    db = _get_job_db()
    rows = db.cursor().execute("SELECT * FROM job").fetchall()
    transient_jobs = [row["aws_job_id"] for row in rows if row["status"] not in ["SUCCEEDED", "FAILED"]]
    for ids in _chunk(transient_jobs, 80):
        logger.info(f"Fetching fresh statuses for: {len(ids)} jobs")
        for job in BATCH.describe_jobs(jobs = ids)["jobs"]:
            print(job)
            db.cursor().execute("""
                UPDATE job 
                SET status = ?, last_updated_at = ?, aws_log_stream = ?
                WHERE aws_job_id = ?
            """, (job["status"], datetime.utcnow(), job["container"].get("logStreamName"), job["jobId"]))
        db.commit()

def jobs(commands):
    _build_docker_image()
    _push_docker_image()
    group_id = _generate_uuid()
    _register_job_definition()
    for tag, command in commands:
        _submit_job(command, group_id, tag)
    return group_id

def dump():
    _sync()
    db = _get_job_db()
    rows = db.cursor().execute("SELECT * FROM job ORDER BY last_updated_at DESC").fetchall()
    return [dict(x) for x in rows]