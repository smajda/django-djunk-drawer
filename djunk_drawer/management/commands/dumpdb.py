import os
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Dump default db to file in settings.DB_BACKUP_DIR.

    DB_BACKUP_DIR defaults to ${HOME}/tmp/[name of virtualenv or 'django']

    TODO:
    - how to gzip the file? i.e. 'mysqldump | gzip > foo.sql.gz'?
    - more than default db?
    """
    def handle(self, *args, **options):
        # get backup_dir
        default_backup = u"{0}/tmp/{1}".format(
            os.environ.get('HOME'),
            os.environ.get('VIRTUAL_ENV', 'django').split('/')[-1],
            )
        backup_dir = os.environ.get('DB_BACKUP_DIR', default_backup)

        # create if need be and cd
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        os.chdir(backup_dir)

        # get db info
        db = settings.DATABASES['default']
        db_type = db['ENGINE']
        backup_path = u"{0}/{1}.{2}.sql".format(
            backup_dir,
            db['NAME'],
            datetime.now().strftime('%Y%m%d-%H%M')
            )

        MYSQL_BACKENDS = ('django.db.backends.mysql', )
        PG_BACKENDS = ('django.db.backends.postgres_psycopg', )

        if db_type in MYSQL_BACKENDS:
            command = u"mysqldump -u {USER} -p{PASSWORD} {NAME}".format(**db)
        elif db_type in PG_BACKENDS:
            command = u"export PGPASSWORD='{PASSWORD}' && pg_dump -Fc -U {USER} {NAME}".format(**db)
        else:
            self.stderr.write("Unsupported database backend\n")
            return None

        # now run it
        with open(backup_path, 'w') as backup_f:
            p = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=backup_f,
                    stderr=backup_f,
                    )

        # print the path so we can then use this in other scripts
        self.stdout.write(backup_path)
