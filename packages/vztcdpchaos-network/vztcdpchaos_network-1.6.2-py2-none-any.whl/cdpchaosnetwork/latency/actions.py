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
import subprocess

__all__ = ["simulate_egress_network_latency", "install_tc"]

def install_tc():
    try:
        logger.info('Installing tc')
        start_time = datetime.datetime.now()
        response = {}
        response['status'] = 'Success'
        responseStart = subprocess.run('yum install -y iproute-tc', stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=os.environ, shell=True)
        if responseStart.returncode != 0:
            logger.error(f'Failed to install tc.')
            response['status'] = 'Failure'
            response['error'] = str(responseStart.stderr)
            raise FailedActivity(f'Failed to install tc. {responseStart.stderr}')
        else:
            logger.info('Successfully installed tc.')


    except KeyboardInterrupt:
        logger.error('User interrupted the process at {}'.format(ctime()))

    return response

def simulate_egress_network_latency(input_base_path, input_arguments_file):
    logger.info(f'Loading input arguments from path: {input_base_path}, arguments file: {input_arguments_file}')
    logger.info(f'Loading scripts from path: {input_base_path}')
    os.chdir(input_base_path)
    config = ConfigParser()
    config.read(max(glob.glob(os.getcwd() + "/**/input.ini", recursive = True), key=os.path.getctime))
    logger.info(f'Configuration sections: {config.sections()}')

    if "network-latency" in config:
        duration_seconds = int(config["network-latency"]["duration_seconds"])
        latency = int(config["network-latency"]["latency"])
        variation = int(config["network-latency"]["variation"])
    else:
        duration_seconds = 60
        latency = 100
        variation = 10
    try:
        start_time = datetime.datetime.now()
        response = {}
        response['status'] = 'Success'
        startScript = max(glob.glob(os.getcwd() + "/**/startAddLatency.sh", recursive = True), key=os.path.getctime)
        endScript = max(glob.glob(os.getcwd() + "/**/deleteTcRules.sh", recursive = True), key=os.path.getctime)
        # if blast_radius == 2:
        #     startScript = max(glob.glob(os.getcwd() + "/**/startFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
        #     endScript = max(glob.glob(os.getcwd() + "/**/endFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
        # if blast_radius > 2:
        #     startScript = max(glob.glob(os.getcwd() + "/**/startFailDns.sh", recursive = True), key=os.path.getctime)
        #     endScript = max(glob.glob(os.getcwd() + "/**/endFailDns.sh", recursive = True), key=os.path.getctime)
        if (duration_seconds > 0):
            logger.info(f'Started network latency simulation for duration: {duration_seconds}, latency: {latency}')
            subprocess.check_call(['chmod', 'u+x', startScript])
            subprocess.check_call(['chmod', 'u+x', endScript])
            responseStart = subprocess.run([startScript, str(latency)+'ms', str(variation)+'ms'], stderr=subprocess.PIPE)
            if responseStart.returncode != 0:
                logger.error(f'Failed to run network latency simulation.')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity(f'Failed to run network latency simulation. {responseStart.stderr}')

            else:
                time.sleep(duration_seconds)
            responseEnd = subprocess.run(endScript, stderr=subprocess.PIPE)
            if responseEnd.returncode != 0:
                logger.error(f'Failed to run end network latency simulation. ')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity('Failed to run end network latency simulation. %s', response['error'])

            diff=datetime.datetime.now() - start_time
            logger.info('Stopped network latency simualtion after {} seconds.'.format(diff))

    except KeyboardInterrupt:
        logger.error('User interrupted the process at {}'.format(ctime()))

    return response
