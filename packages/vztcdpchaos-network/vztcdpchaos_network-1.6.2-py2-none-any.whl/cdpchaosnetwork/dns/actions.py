# -*- coding: utf-8 -*-

import itertools
import os
import signal
import psutil
import time
import random
import subprocess
import multiprocessing
from multiprocessing import Pool
from types import *
import datetime
import logzero
from logzero import logger
from time import ctime, sleep
from time import sleep
import itertools
import threading
from datetime import timedelta
import configparser
from configparser import ConfigParser
from chaoslib.exceptions import FailedActivity
import glob, os
from chaoslib.types import Configuration

__all__ = ["simulate_dns_failure"]


def simulate_dns_failure(input_base_path, input_arguments_file):
    logger.info(f'Loading input arguments from path: {input_base_path}, arguments file: {input_arguments_file}')
    logger.info(f'Loading scripts from path: {input_base_path}')
    os.chdir(input_base_path)
    config = ConfigParser()
    config.read(max(glob.glob(os.getcwd() + "/**/input.ini", recursive = True), key=os.path.getctime))
    logger.debug(f'Configuration sections: {config.sections()}')

    if "dns-failure" in config:
        duration_seconds = int(config["dns-failure"]["duration_seconds"])
        blast_radius = int(config["dns-failure"]["blast_radius"])
    else:
        duration_seconds = 60
        blast_radius = 1
    try:
        start_time = datetime.datetime.now()
        response = {}
        response['status'] = 'Success'
        startScript = max(glob.glob(os.getcwd() + "/**/startFailDnsSingleServer.sh", recursive = True), key=os.path.getctime)
        endScript = max(glob.glob(os.getcwd() + "/**/endFailDnsSingleServer.sh", recursive = True), key=os.path.getctime)
        if blast_radius == 2:
            startScript = max(glob.glob(os.getcwd() + "/**/startFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
            endScript = max(glob.glob(os.getcwd() + "/**/endFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
        if blast_radius > 2:
            startScript = max(glob.glob(os.getcwd() + "/**/startFailDns.sh", recursive = True), key=os.path.getctime)
            endScript = max(glob.glob(os.getcwd() + "/**/endFailDns.sh", recursive = True), key=os.path.getctime)
        if (duration_seconds > 0):
            logger.info(f'Started DNS failure simulation for duration: {duration_seconds}, blastRadius: {blast_radius}')
            subprocess.check_call(['chmod', 'u+x', startScript])
            subprocess.check_call(['chmod', 'u+x', endScript])
            responseStart = subprocess.run(startScript, stderr=subprocess.PIPE)
            if responseStart.returncode != 0:
                logger.error(f'Failed to run the start dns failure script.')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity(f'Failed to run the start dns failure script. {responseStart.stderr}')

            else:
                time.sleep(duration_seconds)
            responseEnd = subprocess.run(endScript, stderr=subprocess.PIPE)
            if responseEnd.returncode != 0:
                logger.error(f'Failed to run the end dns failure script. ')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity('Failed to run the start dns failure script. %s', response['error'])

            diff=datetime.datetime.now() - start_time
            logger.info('Stopped dns failure simualtion after {} seconds.'.format(diff))

    except KeyboardInterrupt:
        logger.error('User interrupted the process at {}'.format(ctime()))

    return response
