#!/usr/bin/env python3

from datetime import timedelta
from logging import getLogger
from os import path
from pygfs.task.analysis import Analysis
from soca import bkg_utils
from typing import Dict
from wxflow import (chdir,
                    FileHandler,
                    logit,
                    Task)

logger = getLogger(__name__.split('.')[-1])


class MarineLETKF(Analysis):
    """
    Class for global ocean and sea ice analysis LETKF task
    """

    @logit(logger, name="MarineLETKF")
    def __init__(self, config: Dict) -> None:
        """Constructor for ocean and sea ice LETKF task
        Parameters:
        ------------
        config: Dict
            configuration, namely evironment variables
        Returns:
        --------
        None
        """

        logger.info("init")
        super().__init__(config)

        PDY = self.runtime_config['PDY']
        cyc = self.runtime_config['cyc']
        DATA = self.runtime_config.DATA
        cdate = PDY + timedelta(hours=cyc)

        half_assim_freq = timedelta(hours=int(config['assim_freq'])/2)
        window_begin = cdate - half_assim_freq

        self.config['window_begin'] = window_begin
        self.config['BKG_LIST'] = 'bkg_list.yaml'
        self.config['bkg_dir'] = path.join(DATA, 'bkg')

    @logit(logger)
    def initialize(self):
        """Method initialize for ocean and sea ice LETKF task
        Parameters:
        ------------
        None
        Returns:
        --------
        None
        """

        logger.info("initialize")


        FileHandler({'mkdir': [self.config.bkg_dir]}).sync()
        bkg_utils.gen_bkg_list(bkg_path=self.config.COM_OCEAN_HISTORY_PREV,
                               out_path=self.config.bkg_dir,
                               window_begin=self.config.window_begin,
                               yaml_name=self.config.BKG_LIST)

    @logit(logger)
    def run(self):
        """Method run for ocean and sea ice LETKF task
        Parameters:
        ------------
        None
        Returns:
        --------
        None
        """

        logger.info("run")

        chdir(self.runtime_config.DATA)

    @logit(logger)
    def finalize(self):
        """Method finalize for ocean and sea ice LETKF task
        Parameters:
        ------------
        None
        Returns:
        --------
        None
        """

        logger.info("finalize")
