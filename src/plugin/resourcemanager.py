import os
import argparse
from pathlib import Path
import time
import subprocess

#from waggle.plugin import Plugin

# This may be deprecated in the future
# as resource manager will use Waggle protocol for messaging
def message_parser(message):
    try:
        command, arguments = message
    except:
        return None, []

class ResourceManager(object):
    flag_apply = 'apply'
    def __init__(self, config_dir='/wagglerw/config', docker_url='unix://var/run/docker.sock'):
        # self.plugin = Plugin()
        self.docker_url = docker_url
        self.root = config_dir

    def log(self, message, level='Error'):

        print('[{0}] {1}'.format(level, message), flush=True)

    def get_current_containers(self):
        return []

    def get_containers(self):
        return []

    def try_stop(self, containers):
        return []

    def try_run(self, containers):
        return []

    def schedule(self):
        containers_being_running = self.get_current_containers()
        scheduled_containers = self.get_containers()
        containers_to_start, containers_to_stop = self.diff(
            containers_being_running,
            scheduled_containers
        )

        containers_failed_to_run = self.try_stop(containers_to_stop)
        if len(containers_failed_to_run) > 0:
            self.log('failed to stop:')
        self.try_run(containers_to_start)

    def apply(self):
        try:
            docker_compose_path = Path(self.root, 'docker-compose.yml')
            if not docker_compose_path.is_file():
                self.log('{0} does not exist'.format(docker_compose_path))
                return False
            plugin_compose = list(Path(self.root).glob('docker-compose.*.yml'))

            command = ['docker-compose', '-p', 'waggle', '-f', str(docker_compose_path)]
            for service in plugin_compose:
                command.extend(['-f', str(service)])
            command.extend(['up', '-d', '--remove-orphans'])

            # update running services
            subprocess.check_call(command)
            self.log('Configuration updated', level='Info')
            return True
        except Exception as ex:
            self.log('On apply:' + str(ex))
            return False

    def run_simple(self):
        while True:
            flag_apply = Path(self.root, self.flag_apply)
            if os.path.exists(flag_apply):
                if self.apply() is True:
                    os.remove(flag_apply)
                else:
                    self.log('Failed to apply the configuration. Retrying in 5 seconds...')
                    time.sleep(5)

            time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_dir', help='Path to plugin configuration')
    #parser.add_argument('--hrf', action='store_true', help='Print in human readable form')
    args = parser.parse_args()
    rm = ResourceManager(args.config_dir)
    rm.run_simple()
