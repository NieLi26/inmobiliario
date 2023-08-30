from django.core.management import call_command


def db_backup_job():
    try:
        call_command('dbbackup')
    except:
        pass
    