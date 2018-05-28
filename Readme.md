The Python-RaspberryPi SmartCar
-------------------------------

## Introduction

This `repo` is for the DPI SRT project.
The SRT requires us to:
- Build a smart car and control it with a RaspberryPi
- Use sensors(camera, Ultrasonic sonar, Infrared detector, etc)
  to detect a lighting object and get close to it, without being
  too close.
Then this `repo` is used to finish this project.

## Basic structure

This repo currently contains the following modules:
- A logging module, and its `yaml` config file
- A motor module to control the whole running
- A camera module, with an thread that will catch and process the
  image to find the light object and put the coordinate into an
  given queue

Some modules that passed the test but not belong to this `repo` :
- A simple TCP server that will receive connection from my PC
  and receive commands to control its movement.

Future development:
- A state-machine or a behavior-tree based AI to control its movement
- A server-client structure to control and monitor its state from 
  an upper-computer

## Simple usage guide

The logging module should be initialized before use.
The initialization method is like this:

```python
import mylogger
mylogger.loggerinit(path_to_config_file)
```

To get an logger by name, you can also use this module:

```python
your_logger = mylogger.getLogger(your_logger_name)
```

Another import initialization is the GPIO port.
To initialization, you should use this(default is GPIO.BOARD):

```python
from pycar import misc
misc.RPiGPIOinit([GPIO.some_naming_mode])
```

To get the contour data, you need first prepare an queue `import queue`,
and an event object `threading.Event` to send the **EXIT** message to the thread.

When getting data from the queue, **Be careful to catch the `queue.Empty` exception!**


----
TODO:

- [x] Motor
- [x] camera
- [ ] state-machine
- [ ] The server interface

Deprecated:
- [ ] bluetooth controller(with multi-threading)
