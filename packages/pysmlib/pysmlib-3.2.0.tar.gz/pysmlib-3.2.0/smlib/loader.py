#! /usr/bin/python
'''
A loader to simplify the creation of a daemon of various fsm running
on different threads and sharing resources.

@date: February 2018
@authors: Davide Marcato
@email: davide.marcato@lnl.infn.it
'''

import signal
from . import fsmFileLogger, fsmLogger, mappedIOs, fsmIOs, fsmTimers, fsmWatchdog, fsmBase


# class to load multiple fsm
class loader(object):
    def __init__(self):
        self._timerManager = fsmTimers()
        self._verbosity = 2
        self._logger = fsmLogger(self._verbosity)
        self._ioManager = fsmIOs()
        self._ioMap = None
        self._fsmsList = []
        self._levelStrings = {"error": 0, "warning": 1, "info": 2, "debug": 3}

    def setVerbosity(self, level):
        if isinstance(level, int):
            n = max(0, min(level, 3))  # log level must be in range [0,3]
        elif isinstance(level, str) and level.lower().strip() in self._levelStrings.keys():
            n = self._levelStrings[level.lower().strip()]
        else:
            raise KeyError("Verbosity level \"%s\" not recognized!" % str(level))

        self._verbosity = n
        self._logger.changeLevel(n)

    def logToFile(self, path, prefix):
        self._logger = fsmFileLogger(self._verbosity, path, prefix)

    def setIoMap(self, iomap):
        self._ioMap = iomap
        self._ioManager = mappedIOs(self._ioMap)

    def load(self, fsmClass, name, *args, **kwargs):
        kwargs["tmgr"] = self._timerManager
        kwargs["ios"] = self._ioManager
        kwargs["logger"] = self._logger
        if not issubclass(fsmClass, fsmBase):
            raise TypeError("%s is not a subclass of fsmBase" % repr(fsmClass))
        fsm = fsmClass(name, *args, **kwargs)  # instance class
        self._fsmsList.append(fsm)
        return fsm

    def killAll(self, signum, frame): # pylint: disable=unused-argument
        #print("Signal: %d -> Going to kill all fsms" % signum)
        for fsm in self._fsmsList:
            if fsm.is_alive():
                fsm.kill()
        print("Killed all the fsms")
        if self._timerManager.is_alive():  # if no fsm is loaded it won't be alive
            self._timerManager.kill()
        print("Killed the timer manager")

    def printUnconnectedIOs(self, signum, frame): # pylint: disable=unused-argument
        ios = self._ioManager.getAll()
        s = 0
        print("DISCONNECTED INPUTS:")
        for i in ios:
            if not i.connected():
                print(i.ioname())
                s += 1
        print("Total disconnected inputs: %d out of %d!" % (s, len(ios)))
        signal.pause()

    def start(self, blocking=True):
        # start another fsm to report if all the others are alive to epics db
        wd = fsmWatchdog("REPORT", self._fsmsList, tmgr=self._timerManager, ios=self._ioManager, logger=self._logger)
        self._fsmsList.append(wd)

        for thread in self._fsmsList:
            thread.start()
        print("%d fsms started!" % (len(self._fsmsList)-1))  # do not count fsmWatchdog (not issued by user)

        if blocking:
            # wait for events
            signal.signal(signal.SIGINT, self.killAll)
            signal.signal(signal.SIGUSR1, self.printUnconnectedIOs)
            signal.pause()
