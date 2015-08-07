"""
Provisioning an app server:

* Use the chef libraries to get the server ready
* fab -H <new server> deploy_updateable:<TAG TO DEPLOY>
* fab -H <new server> activate_tag:<TAG TO_DEPLOY>

"""
from fabric.api import cd, env, hosts, local, run, runs_once, sudo, prefix, settings
from fabric.contrib.files import exists, sed, append
import os
import datetime

DEPLOY_ROOT = '/var/www/'
env.site_name = 'calloway'
env.site_root = "%scallowaysite/" % DEPLOY_ROOT
env.repo_url = "callowaysiterepo:callowayproject/callowaysite.git"
env.forward_agent = True

#TEST_HOST = "webdev@166.78.113.207"
TEST_HOST = "webdev@45.33.77.6"
DATABASE_HOST = TEST_HOST
PROD_HOST = [TEST_HOST, ]

if 'site_root' not in env:
    print "You must specify a path in the env.site_root variable."

if 'repo_url' not in env:
    print "You must specify the URL of the repository in the env.repo_url variable."


@hosts(PROD_HOST)
def _list_sites(force_update=False):
    if not hasattr(env, 'site_list') or force_update:
        output = run('ls -1 %s/current_deploy/sites/' % env.site_root)
        env.site_list = [x.strip() for x in output.split("\n") if not x.startswith("_")]
    return env.site_list


def _make_link_cmd(source, link):
    """
    Generates the command string to make a link (if it doesn't exist)
    """
    return "[ ! -L %s ] && ln -s %s %s" % (link, source, link)


def _read_key_file(key_file):
    key_file = os.path.expanduser(key_file)

    if not key_file.endswith('pub'):
        raise RuntimeWarning('Trying to push non-public part of key pair')
    with open(key_file) as f:
        return f.read()


def push_key(key_file='~/.ssh/id_rsa.pub'):
    key_text = _read_key_file(key_file)
    if not exists('~/.ssh'):
        run('mkdir -p ~/.ssh && touch ~/.ssh/authorized_keys && chmod 700 ~/.ssh')
    append('~/.ssh/authorized_keys', key_text)


@hosts(TEST_HOST)
def make_test_instance(branchname, instance_name="", sitename=""):
    """
    Make a stand-alone instance with name of branchname on the test server
    """
    if not instance_name:
        instance_name = branchname
    if sitename:
        site = sitename
        sitename = os.path.join("sites", sitename)
    instance_dir = env.site_root + instance_name
    if not exists(instance_dir):
        with cd(env.site_root):
            run('git clone %s %s' % (env.repo_url, instance_name))
        with cd(instance_dir):
            run('git checkout %s' % branchname)
    else:
        with cd(instance_dir):
            run("git pull")

    settings_template = os.path.join(instance_dir, 'settings', 'test.py.template')
    settings_path = os.path.join(instance_dir, 'settings', 'test.py')
    if sitename:
        settings_template = os.path.join(instance_dir, 'settings', 'local_settings.py.template')
        settings_path = os.path.join(instance_dir, sitename, 'settings', 'local_settings.py')
        if not exists(settings):
            run('cp %s %s' % (settings_template, settings_path))
            sed(settings_path, '\\{sitename\\}', site)
    if not exists(settings_path):
        run('cp %s %s' % (settings_template, settings_path))
    run('mkdir -p %s' % os.path.join(instance_dir, 'staticmedia', 'CACHE'))
    sudo('chmod -R a+w %s' % os.path.join(instance_dir, 'staticmedia', 'CACHE'))
    if sitename:
        bootstrap(instance_name, 'sites.%s.settings.base' % site)
    else:
        bootstrap(instance_name, 'test')

    upstart_conf_templ = os.path.join(instance_dir, sitename, 'conf', 'upstart-test.conf.template')
    upstart_conf = os.path.join(instance_dir, sitename, 'conf', 'upstart-test.conf')
    if not exists(upstart_conf):
        run('cp %s %s' % (upstart_conf_templ, upstart_conf))
        sed(upstart_conf, '\\{branchname\\}', instance_name)
        if sitename:
            sed(upstart_conf, '\\{site\\}', site)
    upstart_link = "/etc/init/%s.conf" % instance_name
    if not exists(upstart_link):
        sudo('ln -s %s %s' % (upstart_conf, upstart_link))
    sudo('initctl reload-configuration')
    sudo('start %s' % instance_name)

    apache_config_templ = os.path.join(instance_dir, 'conf', 'nginx-test.conf.template')
    apache_config = os.path.join(instance_dir, sitename, 'conf', 'nginx-test.conf')
    if not exists(apache_config):
        run('cp %s %s' % (apache_config_templ, apache_config))
        sed(apache_config, '\\{branchname\\}', instance_name)
    apache_name = '/etc/nginx/sites-available/%s' % instance_name
    if not exists(apache_name):
        sudo('ln -s %s %s' % (apache_config, apache_name))
        sudo('nxensite %s' % instance_name)
    sudo('chgrp -R www-data %s%s/staticmedia' % (env.site_root, instance_name))
    sudo('chmod -R g+w %s%s/staticmedia' % (env.site_root, instance_name))
    _make_link_cmd('/home/natgeo/media', 'media')
    sudo('/etc/init.d/nginx reload')


@hosts(TEST_HOST)
def remove_test_instance(instance_name):
    """
    Remove a test instance and remove all support scripts and configs
    """
    nginx_name = '/etc/nginx/sites-enabled/%s' % instance_name
    if exists(nginx_name):
        sudo('nxdissite %s' % instance_name)
        sudo('/etc/init.d/nginx reload')
    nginx_name = '/etc/nginx/sites-available/%s' % instance_name
    if exists(nginx_name):
        sudo('rm %s' % nginx_name)

    upstart_link = "/etc/init/%s.conf" % instance_name
    if exists(upstart_link):
        with settings(warn_only=True):
            sudo('stop %s' % instance_name)
            sudo('rm %s' % upstart_link)
            sudo('initctl reload-configuration')

    instance_dir = env.site_root + instance_name
    if exists(instance_dir):
        sudo('rm -Rf %s' % instance_dir)


@hosts(TEST_HOST)
def stop_test_instance(test_name=None):
    """
    Stop all the test instances
    """
    env.warn_only = True
    if test_name is not None:
        instances = [test_name]
    else:
        output = run('ls -1 %s' % env.site_root)
        instances = [x.strip() for x in output.split("\n")]
    for item in instances:
        sudo("stop %s" % item.strip())


@hosts(TEST_HOST)
def start_test_instance(test_name=None):
    """
    Start all the test instances
    """
    env.warn_only = True
    if test_name is not None:
        instances = [test_name]
    else:
        output = run('ls -1 %s' % env.site_root)
        instances = [x.strip() for x in output.split("\n")]
    for item in instances:
        sudo("start %s" % item.strip())


@hosts(TEST_HOST)
def list_test_instances():
    """
    List all the test instances on the test server
    """
    run('ls -1 %s' % env.site_root)


@hosts(TEST_HOST)
def reload_test(test_name):
    """
    Reload the <test_name> deployment on the test server
    """
    sudo("restart %s" % test_name)


@hosts(TEST_HOST)
def update_instance(instance, settings_path):
    """
    Update the <instance> deployment usings <settings> settings
    """
    test_dir = env.site_root + instance
    with cd(test_dir):
        run("git pull")

        with prefix('source virtualenv/bin/activate'):
            run("pip install -r requirements.txt")
            run("./manage.py collectstatic --noinput --verbosity 0 --settings " + settings_path)
            run("./manage.py migrate --noinput --settings " + settings_path)
            sudo("restart %s" % instance)


@hosts(TEST_HOST)
def update_test(test_name, site_name=""):
    """
    Update the <test_name> deployment on the test server
    """
    settings = "settings.test"
    if site_name:
        settings = "sites.%s.settings.base" % site_name
    update_instance(test_name, settings)
    if test_name == 'test':
        instance_dir = '%stest' % env.site_root
        with cd(instance_dir):
            with prefix('source virtualenv/bin/activate'):
                output = run('ls -1 sites/')
                sites = [x.strip() for x in output.split("\n") if not x.startswith("_")]

                for site in sites:
                    if exists("sites/%s/static" % site):
                        run("./manage.py collectstatic --noinput --verbosity 0 --settings sites.%s.settings.base" % site)
                    run("./manage.py migrate --noinput --settings sites.%s.settings.base" % site)
                    sudo("restart %s" % site)


@runs_once
def make_tag(tag):
    """
    Create a tag in the local repository and push it to origin
    """
    local('git tag %s;git push --tags' % tag)


@hosts(PROD_HOST)
def link_configs():
    """
    Link configurations
    """
    cur_deploy_path = "%scurrent_deploy/" % env.site_root

    nginx_conf_link = "/etc/nginx/sites-available/%s" % env.site_name
    nginx_conf_path = "%sconf/nginx.conf" % cur_deploy_path
    if not exists(nginx_conf_link):
        sudo(_make_link_cmd(nginx_conf_path, nginx_conf_link))
    if not exists("/etc/nginx/sites-enabled/%s" % env.site_name):
        nginx_conf_link = "/etc/nginx/sites-enabled/%s" % env.site_name
        nginx_conf_path = "/etc/nginx/sites-available/%s" % env.site_name
        sudo(_make_link_cmd(nginx_conf_path, nginx_conf_link))
        sudo("/etc/init.d/nginx reload")
    upstart_link = "/etc/init/%s.conf" % env.site_name
    if not exists(upstart_link):
        upstart_path = "%sconf/upstart.conf" % cur_deploy_path
        sudo(_make_link_cmd(upstart_path, upstart_link))
        sudo('initctl reload-configuration')
        sudo('start %s' % env.site_name)


def bootstrap(tag, settings_path='settings'):
    """
    Bootstrap a deployment. Useful if something fails, or if you just want to.
    """
    deploy_dir = "%s%s" % (env.site_root, tag)
    virtualenv = "%s/virtualenv" % deploy_dir
    settings_file = settings_path
    if 'settings' not in settings_path:
        settings_file = 'settings.%s' % settings_path

    # Bootstrap the code
    with cd(deploy_dir):
        # run("python bootstrap.py")
        with prefix('source %s/bin/activate' % virtualenv):
            run("./manage.py collectstatic --noinput --verbosity 0 --settings %s" % settings_file)
            run("./manage.py migrate --noinput --settings %s" % settings_file)


@hosts(PROD_HOST)
def deploy_updateable(tag):
    """
    Deploy a checkout of the repository.
    """
    if not exists(env.site_root):
        sudo('mkdir -m 0755 -p %s' % env.site_root)
        sudo('chown webdev:www-data %s' % env.site_root)

    deploy_dir = "%s%s" % (env.site_root, tag)
    if exists(deploy_dir):
        print "%s is already deployed." % tag
        return
    with cd(env.site_root):
        run('git clone %s %s' % (env.repo_url, tag))
    with cd(deploy_dir):
        run('git checkout %s' % tag)
    sudo(_make_link_cmd(deploy_dir, '%scurrent_deploy' % env.site_root))
    bootstrap(tag)


@hosts(PROD_HOST)
def update(tag=None):
    """
    Update the current_deploy to tag
    """
    deploy_dir = "%scurrent_deploy" % env.site_root
    virtualenv = "%s/virtualenv" % deploy_dir
    if tag is None and not env.get('tag', False):
        tag = datetime.datetime.now().strftime("D%Y%m%d%H%M")
        env.tag = tag
        make_tag(tag)

    with cd(deploy_dir):
        run('git fetch --tags')
        run('git reset --hard HEAD')
        run('git checkout %s' % tag)

        with prefix('source %s/bin/activate' % virtualenv):
            run("pip install -r requirements.txt")
            run("./manage.py collectstatic --noinput --verbosity 0 --settings settings.production")

            settings_files = [("education", "settings.production",), ]
            settings_files.extend(
                [('education_%s' % x, 'sites.%s.settings.base' % x) for x in _list_sites()]
            )
            sudo("supervisorctl restart rqworker")
            sudo("supervisorctl restart rqscheduler")
            for site_name, site_settings in settings_files:
                if exists("sites/%s/static" % site_name):
                    run("./manage.py collectstatic --noinput --verbosity 0 --settings %s" % site_settings)
                run("./manage.py migrate --noinput --settings %s" % site_settings)
                sudo("restart %s" % site_name)


@hosts(DATABASE_HOST)
def _create_database(sitename):
    sudo('createdb education_%s -E UTF8 -O ngdm_wpf' % sitename, user='postgres')
