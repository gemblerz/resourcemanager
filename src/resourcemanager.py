import os
import argparse
import time

class ResourceManager():
    LOG
    def __init__(self, docker_url='unix://var/run/docker.sock'):
        self.docker_url = docker_url

    def get_current_containers(self):
        return []

    def get_containers(self):
        return []

    def try_stop(self, containers):
        return []

    def try_run(self, containers):
        return []

    def run(self):
        while True:
            containers_being_running = self.get_current_containers()
            scheduled_containers = self.get_containers()
            containers_to_start, containers_to_stop = self.diff(
                containers_being_running,
                scheduled_containers
            )

            containers_failed_to_run = self.try_stop(containers_to_stop)
            if len(containers_failed_to_run) > 0:
                self.log('failed to stop:'
            self.try_run(containers_to_start)

            time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('--input-sensor', action='store_true', help='Data from the sensor board')
    #parser.add_argument('--hrf', action='store_true', help='Print in human readable form')
    args = parser.parse_args()
    rm = ResourceManager()
    rm.run()
