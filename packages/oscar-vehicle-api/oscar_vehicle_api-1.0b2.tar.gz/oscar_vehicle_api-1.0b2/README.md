### OSCAR vehicle API

Репозиторий содержит API низкоуровневой системы управления, разрабатываемой в рамках проекта [OSCAR](https://gitlab.com/starline/oscar), для беспилотных транспортных средств.


#### Установка с PyPI

```
pip install --user oscar_vehicle_api
```


#### Установка из исходников

```
git clone https://gitlab.com/starline/oscar_vehicle_api.git && cd oscar_vehicle_api
pip install --user -e .
```

#### Использование

```
import oscar_vehicle_api
vehicle = oscar_vehicle_api.LexusRX450H(“/dev/ttyACM0”)       # начало работы с автомобилем
vehicle.auto_mode()                                           # перехват управления автомобилем
vehicle.manual_mode()                                         # ручной режим управления автомобилем
vehicle.set_vehicle_throttle                                  # управление ускорением автомобиля в процентах
vehicle.set_steering_wheel_torque                             # управление усилием на руле в процентах
vehicle.led_blink()                                           # индикация на панели управления автомобиля
vehicle.emergency_stop()                                      # экстренное торможение автомобиля
vehicle.recover()                                             # отмена экстренного торможения автомобиля
vehicle.left_turn_signal()                                    # включить левый сигнал поворота
vehicle.right_turn_signal()                                   # включить правый сигнал поворота
vehicle.emergency_signals()                                   # включить аварийные огни автомобиля
vehicle.turn_off_signals()                                    # выключить индикацию автомобиля
vehicle.get_steering_wheel_angle_and_velocity()               # получить положение и скорость руля
vehicle.get_steering_wheel_and_eps_torques                    # получить усилие на руле и системе EPS
vehicle.get_vehicle_speed                                     # получить скорость автомобиля
vehicle.get_vehicle_wheels_speed                              # получить скорость колес автомобиля
```
