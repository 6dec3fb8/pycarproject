#!/usr/bin/python3

# the service used to run the smart car

# imports

import time
import threading
from socketserver import (
    ThreadingTCPServer,
    StreamRequestHandler
    )

# functions

# classes

class ReconnectableThreadingTCPServer(ThreadingTCPServer):
    allow_reuse_address = True


class PycarHandler(StreamRequestHandler):
    _env = None
    def handle(self):
        print("Get connected with client(%s)."
                % (self.client_address,) )
        if self.__class__._env is None or (
                'motor_differentor' not in self.__class__._env
                # or 'else_required' not in ...
                ):
                print("EnvironmentError!")
                self.__class__._env = self.__class__._env or {}
                self.__class__._env['error'] = 'Missing required key'
                return
        self.wfile.write( 'pycar_magic_header'.encode() )
        # while loop
        while True:
            time.sleep(0.1)
            # receive command:
            msg = self.rfile.readline().strip().decode()
            print( "Received message from (%s): %s"
                    % (self.client_address, msg) )
            if msg == '':
                print("Client connection closed.")
                break
            setc = False
            wait_time = -1
            # commands:
            cmds = msg.split(' ')
            if cmds[0] == 'exit':
                print("Client called Exit.")
                self.wfile.write( 'Bye'.encode() )
                break
            elif (cmds[0] == 'set' and cmds[1] == 'speed'):
                if len(cmds) >= 4:
                    try:
                        velo, deltavelo = int(cmds[2]),int(cmds[3])
                        setc = True
                    except ValueError:
                        print("Command format error!")
                    if len(cmds) >= 5:
                        wait_time = float(cmds[4])
                else:
                    print("Command argument missing!")
                    # more may add here
            elif cmds[0] == 's':
                # short for 'set speed'
                if len(cmds) >= 3:
                    try:
                        velo, deltavelo = int(cmds[1]),int(cmds[2])
                        setc = True
                    except ValueError:
                        print("Command format error!")
                    if len(cmds) >= 4:
                        wait_time = float(cmds[3])
                else:
                    print("Command argument missing!")
            elif cmds[0] == 'h' or cmds[0] == 'halt' or cmds[0] == 'brake':
                # fast halt
                self.__class__._env['motor_differentor'].set_speed(0, 0)
                setc = False
                print("Car fast brake")
            else:
                # failback
                print("Invalid command.")

            if setc:
                self.__class__._env['motor_differentor'].set_speed(velo, deltavelo)
                if wait_time > 0:
                    print("Set speed to (%d, %d) for %f seconds." % (velo, deltavelo, wait_time) )
                    time.sleep(wait_time)
                    self.__class__._env['motor_differentor'].set_speed(0, 0)
                else:
                    print("Set speed to (%d, %d)" % (velo, deltavelo) )
    pass

# class factory

def handler_factory(env):
    class _TempraryChildHandler(PycarHandler):
        _env = env
    return _TempraryChildHandler


# test drive

def _test_1():
    from pycar import misc, motor
    misc.init()
    md = motor.MotorDifferentor(12, 16, 18, 11)
    env = {'motor_differentor': md}
    serv = ReconnectableThreadingTCPServer( ('', 2500), handler_factory(env) )
    try:
        print("Waiting to get connected...")
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Exiting.")
        serv.shutdown()

    pass


if __name__ == '__main__':
    _test_1()
