import os
from fabric.api import sudo, cd, put, local, run, env, settings


def prod():
    env.hosts = os.environ['SERVER_HOST']
    env.user = os.environ['SERVER_USER']
    if os.environ.get('SERVER_PEM'):
        env.key_filename = os.environ['SERVER_PEM']
    if os.environ.get('SERVER_PASSWORD'):
        env.password = os.environ['SERVER_PASSWORD']


def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)


def setup():
    sudo('apt-get install libapache2-mod-wsgi')
    sudo('a2enmod wsgi')
    put('deploy/magpie_api.conf', '/etc/apache2/sites-available/magpie_api.conf', use_sudo=True)
    sudo('a2ensite magpie_api.conf')
    sudo('service apache2 reload')
    with settings(warn_only=True):
        sudo('git clone https://github.com/SAAVY/magpie.git /var/www/magpie')
    with cd('/var/www/magpie'):
        sudo('git pull')
        sudo('virtualenv -p /usr/bin/python2.7 venv')


def deploy():
    # figure out the release name and version
    dist = local('python setup.py --fullname', capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    put('dist/%s.tar.gz' % dist, '/tmp/magpie.tar.gz')
    local('rm dist/%s.tar.gz' % dist)
    # create a place where we can unzip the tarball, then enter
    # that directory and unzip it
    run('mkdir -p /tmp/magpie')
    with cd('/tmp/magpie'):
        run('tar xzf /tmp/magpie.tar.gz')
        # now setup the package with our virtual environment's
        with cd('/tmp/magpie/' + dist):
            # python interpreter
            sudo('/var/www/magpie/venv/bin/pip install mock')
            sudo('/var/www/magpie/venv/bin/python setup.py install')
    # now that all is set up, delete the folder again
    sudo('rm -rf /tmp/magpie /tmp/magpie.tar.gz')
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    sudo('touch /var/www/magpie/magpie.wsgi')
