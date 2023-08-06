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

__all__ = ["simulate_egress_network_packet_loss"]


def simulate_egress_network_packet_loss(input_base_path, input_arguments_file):
    logger.info(f'Loading input arguments from path: {input_base_path}, arguments file: {input_arguments_file}')
    logger.info(f'Loading scripts from path: {input_base_path}')
    os.chdir(input_base_path)
    config = ConfigParser()
    config.read(max(glob.glob(os.getcwd() + "/**/input.ini", recursive = True), key=os.path.getctime))
    logger.debug(f'Configuration sections: {config.sections()}')

    if "packet-loss" in config:
        duration_seconds = int(config["packet-loss"]["duration_seconds"])
        percent = int(config["packet-loss"]["percent"])

    else:
        duration_seconds = 60
        percent = 0.1

    try:
        start_time = datetime.datetime.now()
        response = {}
        response['status'] = 'Success'
        startScript = max(glob.glob(os.getcwd() + "/**/startPacketLoss.sh", {str(percent)+'%'}, recursive = True), key=os.path.getctime)
        endScript = max(glob.glob(os.getcwd() + "/**/deleteTcRules.sh", recursive = True), key=os.path.getctime)
        # if blast_radius == 2:
        #     startScript = max(glob.glob(os.getcwd() + "/**/startFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
        #     endScript = max(glob.glob(os.getcwd() + "/**/endFailDnsTwoServers.sh", recursive = True), key=os.path.getctime)
        # if blast_radius > 2:
        #     startScript = max(glob.glob(os.getcwd() + "/**/startFailDns.sh", recursive = True), key=os.path.getctime)
        #     endScript = max(glob.glob(os.getcwd() + "/**/endFailDns.sh", recursive = True), key=os.path.getctime)
        if (duration_seconds > 0):
            logger.info(f'Started network packet loss simulation for duration: {duration_seconds}, percent: {percent}')
            subprocess.check_call(['chmod', 'u+x', startScript])
            subprocess.check_call(['chmod', 'u+x', endScript])
            responseStart = subprocess.run(startScript, stderr=subprocess.PIPE)
            if responseStart.returncode != 0:
                logger.error(f'Failed to run network packet loss simulation.')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity(f'Failed to run network packet loss simulation. {responseStart.stderr}')

            else:
                time.sleep(duration_seconds)
            responseEnd = subprocess.run(endScript, stderr=subprocess.PIPE)
            if responseEnd.returncode != 0:
                logger.error(f'Failed to run end network packet loss simulation. ')
                response['status'] = 'Failure'
                response['error'] = str(responseStart.stderr)
                raise FailedActivity('Failed to run end network packet loss simulation. %s', response['error'])

            diff=datetime.datetime.now() - start_time
            logger.info('Stopped network packet loss simualtion after {} seconds.'.format(diff))

    except KeyboardInterrupt:
        logger.error('User interrupted the process at {}'.format(ctime()))

    return response
