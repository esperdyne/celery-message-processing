import os

from fabric.api import local

from celery import chain, group
from celery.task.control import inspect
from proj.tasks import parse, deploy_db, deploy_es

def workers(action):
    """Issue command to start, restart, or stop celery workers"""
    
    # Prepare the directories for pids and logs
    local("mkdir -p celery-pids celery-logs")
    
    # Launch 4 celery workers for 4 queues (parse, db_deploy, es_deploy, and default)
    # Each has a concurrency of 2 except the default which has a concurrency of 1
    # More info on the format of this command can be found here:
    # http://docs.celeryproject.org/en/latest/reference/celery.bin.multi.html
    
    local("celery multi {} parse db_deploy es_deploy celery "\
          "-Q:parse parse -Q:db_deploy db_deploy -Q:es_deploy es_deploy -Q:celery celery "\
          "-c 2 -c:celery 1 "\
          "-l info -A proj "\
          "--pidfile=celery-pids/%n.pid --logfile=celery-logs/%n.log".format(action))
    
def inspect_workers():
    """Display information about workers and queues"""
    
    i = inspect()
    
    print i.scheduled()
    print i.active()
    
def process_one(filename=None):
    """Enqueues a mail file for processing"""
    
    res = chain(parse.s(filename), group(deploy_db.s(), deploy_es.s()))()
    
    print "Enqueued mail file for processing: {} ({})".format(filename, res)
    
def process(path=None):
    """Enqueues a mail file for processing. Optionally, submitting a
    directory will enqueue all files in that directory"""
    
    if os.path.isfile(path):
        process_one(path)
    elif os.path.isdir(path):
        for subpath, subdirs, files in os.walk(path):
            for name in files:
                process_one(os.path.join(subpath, name))
    
def query_es(query="*:*"):
    """Query the elastic search instance"""
    
    local("curl 'http://localhost:9200/_search?q={}&pretty=true'".format(query))
    
def query_db(query="SELECT COUNT(*) FROM messages"):
    """Query the MySQL database instance"""
    
    local("mysql -u root -e '{}' messages".format(query))
    
def purge():
    """Purge all data from Elastic Search index and MySQL table"""
    
    local("curl -XDELETE 'http://localhost:9200/messages/?pretty=true'")
    local("mysql -u root -e 'DROP TABLE IF EXISTS messages' messages")