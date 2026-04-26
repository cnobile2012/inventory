#
# utils/loghandler.py
#

import sys
import os
import cPickle
import time
import codecs
import logging
import logging.handlers


class NewTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, persistFile, filename, when='h', interval=1,
                 backupCount=0, encoding=None):
        self.persistFile = persistFile
        logging.handlers.TimedRotatingFileHandler.__init__(
            self, filename, when=when, interval=interval,
            backupCount=backupCount)

        data = self.getPersistentData()
        currentTime = int(time.time())
        # Calculated last roll time.
        lastRoll = self.rolloverAt - self.interval

        if isinstance(data, dict):
            rolloverAt = data.get('rolloverAt', 0)
            lastRoll = data.get('lastRoll', 0)

            if lastRoll < (currentTime - self.interval):
                self.rolloverAt = rolloverAt
            else:
                self.setPersistentData(self.rolloverAt, lastRoll=lastRoll)
        else:
            self.setPersistentData(self.rolloverAt, lastRoll=lastRoll)

        msg = (f"Current persistent log file, rolloverAt: {self.rolloverAt}, "
               f"lastRoll: {lastRoll}")
        print(msg, file=sys.stderr)

    def getPersistentData(self):
        fobj = None
        result = None

        if os.path.isfile(self.persistFile):
            # Get the persisted rollover time from a file.
            try:
                fobj = open(self.persistFile, "r")
                p = cPickle.Unpickler(fobj)
                result = p.load()
                fobj.close()
            except Exception as e:
                if fobj:
                    fobj.close()

                raise e

            if isinstance(result, dict):
                msg = ("getPersistentData(): rolloverAt: "
                       f"{result.get('rolloverAt')}, lastRoll: "
                       f"{result.get('lastRoll')}")
                print(msg, file=sys.stderr)

        return result

    def setPersistentData(self, rolloverAt, lastRoll=0):
        fobj = None
        data = {'rolloverAt': rolloverAt, 'lastRoll': lastRoll}

        # Persist the rollover time to disk.
        try:
            fobj = open(self.persistFile, "w")
            p = cPickle.Pickler(fobj)
            p.dump(data)
            fobj.close()
        except Exception as e:
            if fobj:
                fobj.close()

            raise e

        msg = (f"setPersistentData(): rolloverAt: {rolloverAt}, "
               f"lastRoll: {lastRoll}")
        print(msg, file=sys.stderr)

    def shouldRollover(self, record):
        """
        Determine if rollover should occur. First check that the
        persisted object should override the memory object.

        The argument 'record' is not used, as we are just comparing times,
        but it is needed so the method signatures are the same
        """
        result = False
        currentTime = int(time.time())

        # Check the memory value self.rolloverAt so getPersistentData()
        # is not called for every log event.
        if currentTime >= self.rolloverAt:
            data = self.getPersistentData()

            if isinstance(data, dict):
                rolloverAt = data.get('rolloverAt', 0)
                lastRoll = data.get('lastRoll', 0)

                # Check if the last roll time plus the interval is greater
                # than the current time. This means we don't need to roll yet.
                if (lastRoll + self.interval) > currentTime:
                    # No need to roll, but we need to drop the handle to the
                    # old file and get the handle to the new file.
                    self.stream.close()

                    if self.encoding:
                        self.stream = codecs.open(self.baseFilename, 'w',
                                                  self.encoding)
                    else:
                        self.stream = open(self.baseFilename, 'w')

                    self.rolloverAt = rolloverAt
                else:
                    # We have missed the roll time, so roll now.
                    msg = (f"Should roll, lastRoll({lastRoll}) + "
                           f"self.interval({self.interval}) "
                           f"<= currentTime({currentTime})")
                    print(msg, file=sys.stderr)
                    result = True
            else:
                # Bad data in the persist file or some jerk blew the file
                # away, so we just believe the memory value in self.rolloverAt.
                msg = ("Should roll, wrong data type in or missing "
                       "persist file.")
                print(msg, file=sys.stderr)
                result = True

        return result

    def doRollover(self):
        lastRoll = self.rolloverAt
        logging.handlers.TimedRotatingFileHandler.doRollover(self)
        self.setPersistentData(self.rolloverAt, lastRoll=lastRoll)
