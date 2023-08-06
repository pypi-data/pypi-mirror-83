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

import inspect
import sys
import log
import threading
import time
from math import cos, sin, tan, copysign

def available_controllers():

    controllers = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            controllers.update({name: obj})

    return controllers


def create_controller_by_name(controller, vehicle, params = None):
    if controller:
        controllers = available_controllers()
        if controller in controllers:
            return controllers[controller](vehicle, params)
        else:
            log.print_warn("There is no " + str(controller) + " controller!")

    return None


class BaseController(object):

    def __init__(self, vehicle, params = None):
        self._params = {}

        self._vehicle = vehicle

        self._state_lock = threading.Lock()

        self._target_vehicle_speed        = None
        self._target_vehicle_acceleration = None
        self._target_vehicle_jerk         = None

        self._target_steering_wheel_angle    = None
        self._target_steering_wheel_velocity = None

        self._output_vehicle_throttle = None
        self._output_steering_torque  = None


    def update_params(self, params):
        self._params.update(params)


    def get_params(self):
        return self._params


    def reset():
        pass


    def set_target_speed(self, speed = None, acceleration = None, jerk = None):
        self._target_vehicle_speed        = speed
        self._target_vehicle_acceleration = acceleration
        self._target_vehicle_jerk         = jerk


    def set_target_steering(self, steering_wheel_angle = None, steering_wheel_velocity = None):
        self._target_steering_wheel_angle    = steering_wheel_angle
        self._target_steering_wheel_velocity = steering_wheel_velocity


    def calc_output():
        return self._output_vehicle_throttle, self._output_steering_wheel_torque


class PID_with_I_saturation(BaseController):

    MAX_DELAY_IN_CONTROL_LOOP = 0.05

    def __init__(self,  *args, **kwargs):
        super(BaseController, self).__init__(*args, **kwargs)

        self._last_steering_wheel_angle_error = 0.0
        self._last_control_time = 0.0

        self._integrator = 0.0

        self._params = {"steering_wheel_P": 0.1,
                        "steering_wheel_I": 0.1,
                        "steering_wheel_I_saturation": 80,
                        "steering_wheel_D": 0.01,
                        "vehicle_speed_P":  0.5}

    def reset():
        self._last_steering_wheel_angle_error = 0.0
        self._last_control_time = 0.0
        self._integrator = 0.0


    def calc_output():

        cur_time = time.time()
        dtime = cur_time - self._last_control_time

        # acceleration and throttle are the same for this controller
        if self._target_vehicle_acceleration < 0:
            self._output_vehicle_throttle = max(self._target_vehicle_acceleration, -100)
        else:
            self._output_vehicle_throttle = min(self._target_vehicle_acceleration,  100)

        if (dtime > self.MAX_DELAY_IN_CONTROL_LOOP):
            return self._output_vehicle_throttle, 0

        # steering wheel control part
        cur_vehicle_speed = self._vehicle.get_vehicle_speed()
        cur_steering_wheel_angle, cur_steering_wheel_velocity = self._vehicle.get_steering_wheel_angle_and_velocity()

        steering_wheel_angle_error = self._target_steering_wheel_angle - cur_steering_wheel_angle

        p_term = steering_wheel_angle_error * self._params['steering_wheel_P']

        integrator = self._integrator + steering_wheel_angle_error * dtime * self._params['steering_wheel_I']
        if abs(integrator) <  self._params['steering_wheel_I_saturation']:
            self._integrator = integrator

        dsteering_wheel_angle_error = self._last_steering_wheel_angle_error - steering_wheel_angle_error
        d_term = (dsteering_wheel_angle_error / dtime) * self._params['steering_wheel_D']

        self._output_steering_wheel_torque = p_term + self._integrator + d_term

        self._last_steering_wheel_angle_error = steering_wheel_angle_error
        self._last_control_time = cur_time

        return self._output_vehicle_throttle, self._output_steering_wheel_torque
