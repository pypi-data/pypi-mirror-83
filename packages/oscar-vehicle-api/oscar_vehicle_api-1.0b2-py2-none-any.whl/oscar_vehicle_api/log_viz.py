#!/usr/bin/env python

###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import os, sys, time

import json
from collections import OrderedDict as odict

from argparse import ArgumentParser

import matplotlib.pyplot as plt

import log


class VehicleLogViz():

    def __init__(self):
        self._path_to_vehicle_log_file = self.pars_arguments().file_path
        self.vehicle_log = self.load_vehicle_log_from_file()
        self.fig, self.ax = plt.subplots(1, 1, figsize=[22.0, 12.0], facecolor='#E0E0E0')#, axisbg='black')
        plt.subplots_adjust(bottom=0.05, right=0.98, top=0.96, left=0.04)
        # self.ax.set_aspect('equal')
        # self.ax.set_xlim([-12, 12])
        # self.ax.set_ylim([-12, 12])
        self.ax.grid(True, color='#E0E0E0')
        self.ax.set_xlabel('time, [s]')
        self.ax.set_ylabel('data')
        self.ax.patch.set_facecolor('#161616')

        plt.title(self._path_to_vehicle_log_file)

        self.sw_angle_plot, = self.ax.plot([], [],      color="#483D8B", lw=2, ls='-', label='sw_angle [ang]')
        self.sw_velocity_plot, = self.ax.plot([], [],   color="#DC143C", lw=2, ls='-', label='sw_velocity [ang/s]')
        self.sw_torque_plot, = self.ax.plot([], [],     color="#00FA9A", lw=2, ls='-', label='sw_torque')
        self.eps_torque_plot, = self.ax.plot([], [],    color="#1E90FF", lw=2, ls='--', label='eps_torque * 0.1')
        self.vehicle_speed_plot, = self.ax.plot([], [], color="#EB7A6F", lw=2, ls='-', label='vehicle_speed [cm/s]')
        self.mode_plot, = self.ax.plot([], [],          color="#FFA500", lw=1, ls='-', label='mode')

        self.legend = self.ax.legend()
        self.legend.get_frame().set_facecolor('#E0E0E0')


    def pars_arguments(self):
        parser = ArgumentParser(description="Script plots vehicle logs.")
        parser.add_argument('-n', '--name', dest='file_path', required=True, help='Full path to log file')
        return parser.parse_args()


    def load_vehicle_log_from_file(self):

        try:
            log_file_handler = open(self._path_to_vehicle_log_file, 'r')
        except Exception as err:
            log.error("Can't open file " + self._path_to_vehicle_log_file + ". " + str(err))

        try:
            vehicle_log_data = json.load(log_file_handler)
        except Exception as err:
            log.error("Can't load log from file " + self._path_to_vehicle_log_file + ". " + str(err))

        log_file_handler.close()
        return vehicle_log_data


    def plot_vehicle_log(self):

        t = []
        sw_angle = []
        sw_velocity = []
        sw_torque = []
        eps_torque = []
        vehicle_speed = []
        mode = []

        for element in self.vehicle_log["data"]:
            t.append(float(element['t']))
            sw_angle.append(float(element['sw_angle']))
            sw_velocity.append(float(element['sw_velocity']))
            sw_torque.append(float(element['sw_torque']))
            eps_torque.append(float(element['eps_torque']) * 0.1)
            vehicle_speed.append(float(element['vehicle_speed']) * 100)
            mode.append(float(element['mode']) * 100)

        self.sw_angle_plot.set_data(t, sw_angle)
        self.sw_velocity_plot.set_data(t, sw_velocity)
        self.sw_torque_plot.set_data(t, sw_torque)
        self.eps_torque_plot.set_data(t, eps_torque)
        self.vehicle_speed_plot.set_data(t, vehicle_speed)
        self.mode_plot.set_data(t, mode)

        self.ax.relim()      # make sure all the data fits
        self.ax.autoscale()

        plt.show()


if __name__ == "__main__":

    log_plotter = VehicleLogViz()
    log_plotter.plot_vehicle_log()
