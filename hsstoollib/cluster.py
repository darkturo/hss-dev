#!/usr/bin/python

import pexpect
import time
import re
import ConfigParser

import logging
logger = logging.getLogger("hsstoollib.cluster")

class Error (Exception):
    def __init__ (self):
        self.kind = "Generic error"

    def __str__ (self):
        if hasattr (self, "msg") and self.msg:
            return "%s: %s" % (self.kind, self.msg)
        else:
            return self.kind

# The Cluster class
##############################################################################

class Cluster:
    def __init__ (self, name, platform_vip, loader_ip, ext_vmif, int_vmif):
        self.name = name
        self.platform_vip = platform_vip
        self.loader_ip = loader_ip
        self.ext_vmif = ext_vmif
        self.int_vmif = int_vmif

        self.connected = False

    def connect (self):
        if not self.connected:
            self.tutil = TUtil (self.loader_ip)
            self.telorb = TelORB (self.loader_ip)
            self.connected = True

    @property
    def clusterName (self):
        self.connect ()
        return self.telorb.clustername

    @property
    def backups (self):
        self.connect ()
        return Backups (self.tutil.backups, self.tutil)

    @property
    def processors (self):
        self.connect ()
        processors = {}
        for name in self.telorb.listProcessors ():
            processors[name] = Processor (name, self.tutil, self.telorb)

        return processors

# The TUtil class
##############################################################################

class TUtilError (Error):
    def __init__ (self, hostname, msg = None):
        self.kind = "TUtil error (host=%s)" % hostname
        self.msg = msg

class TUtil:
    def __init__ (self, hostname):
        self.hostname = hostname
        command = "telnet %s %u" % (hostname, 8110)
        self.tutil = pexpect.spawn (command)
        self.tutil.timeout = 2
        self.waitForPrompt ()

    def waitForPrompt (self):
        try:
            self.tutil.expect ("> ")
            return self.tutil.before
        except pexpect.EOF:
            self._raiseTUtilError ("telnet connection ended unexpectedly after:\n%s " % self.tutil.before)
        except pexpect.TIMEOUT:
            self._raiseTUtilError ("Did not receive prompt after:\n%s " % self.tutil.before)

    def _raiseTUtilError (self, msg):
        raise TUtilError (self.hostname, msg)


    # Backup functionality
    ##########################################################################

    @property
    def backups (self):
        logger.debug ("Obtaining list of backups")
        self.tutil.sendline ("CLI/Backups/list")
        self.tutil.expect ("--- Backups ---")
        self.tutil.expect ("-----------------")

        backups = {}
        for line in self.tutil.before.split ():
            if line.startswith ("(A)"):
                name = line.replace ("(A)", "")
                backups[name] = Backup (name, self, True)
            else:
                backups[line] = Backup (line, self)

        logger.debug ("Obtained backups: %s" % backups.keys())

        self.waitForPrompt ()
        return backups

    @property
    def activeBackup (self):
        logger.debug ("Obtaining active backup")
        for backup in self.backups.itervalues ():
            if backup.active:
                logger.debug ("Active backup is: %s" % backup)
                return backup
        return None

    def createBackup (self, name, wait = True):
        logger.info ("Asking to create backup: %s" % name)
        self.tutil.sendline ("CLI/Backups/create %s" % name)

        self.tutil.expect ("Backup has been ordered")
        logger.info ("Backup %s has been ordered" % name)

        self.waitForPrompt ()

        if wait:
            self.waitForBackupToActivate (name)

    def activateBackup (self, name, wait = True):
        logger.info ("Asking to activate backup: %s" % name)
        self.tutil.sendline ("CLI/Backups/activate %s" % name)

        self.tutil.expect ("Backup has been activated")
        logger.info ("Activation of backup %s has been ordered")

        self.waitForPrompt ()

        if wait:
            self.waitForBackupToActivate (name)

    def removeBackup (self, name):
        if self.activeBackup.name == name:
            self._raiseTUtilError ("Cannot remove active backup %s" % name)

        logger.info ("Asking to remove backup: %s" % name)
        self.tutil.sendline ("CLI/Backups/remove %s" % name)

        self.tutil.expect ("Removing of backup has been ordered")
        logger.info ("Removal of backup %s has been ordered")

        self.waitForPrompt ()

    def waitForBackupToActivate (self, name, timer = 1.0):
        logger.info ("Wating for backup %s to become active" % name)
        while True:
            active = self.activeBackup.name
            if not active or active.name != name:
                time.sleep (timer)
            else:
                break
        logger.info ("Backup %s is now active" % name)

    # Processor functionality
    ##########################################################################

    def getProcesses (self, tp):
        logger.debug ("Obtainging proccesses for processor %s" % tp)
        self.tutil.sendline ("/processors/%s/qtil/bin/ps" % tp)

        raw = self.waitForPrompt ()

        processes = {}
        for line in raw.splitlines():
            fields = line.split ()
            if not fields[0].isdigit ():
                continue
            pid = int(fields[0])
            name = fields[-1]

            processes[pid] = Process (name, pid, self.tutil)

        return processes

    def getProcessorLoads (self, tp):
        logger.debug ("Obtainging loads for processor %s" % tp)
        self.tutil.sendline ("/processors/%s/qtil/bin/cpuload" % tp)

        raw = self.waitForPrompt ()
        if "command not found" in raw:
            return None

        loads = {}
        for line in raw.splitlines ():
            load = re.search ("(.*):\s+(\S+)%", line)
            if load:
                loads[load.group(1)] = float(load.group(2))
        return loads


# The TelORB class
##############################################################################

class TelORBError (Error):
    def __init__ (self, hostname, msg = None):
        self.kind = "TelORB error (host=%s)" % hostname
        self.msg = msg

class TelORB:
    def __init__ (self, hostname):
        self.hostname = hostname
        command = "telnet %s %u" % (hostname, 8000)
        self.telorb = pexpect.spawn (command)
        self.telorb.timeout = 2
        self.waitForPrompt ()

    def waitForPrompt (self):
        try:
            self.telorb.expect ("\$ /.*>")
            return self.telorb.before
        except pexpect.EOF:
            self._raiseTelORBError ("telnet connection ended unexpectedly after:\n%s " % self.telorb.before)
        except pexpect.TIMEOUT:
            self._raiseTelORBError ("Did not receive prompt after:\n%s " % self.telorb.before)

    def _raiseTelORBError (self, msg):
        raise TelORBError (self.hostname, msg)

    @property
    def clustername (self):
        name = None
        self.telorb.sendline ("CLI/getinfo")
        raw = self.waitForPrompt ()
        for line in raw.splitlines ():
            if line.startswith ("System name: "):
                fields = line.split(":")
                name = fields[1].strip ()
                logger.debug ("Obtained clustername: %s" % name)
        return name

    def listProcessors (self):
        self.telorb.sendline ("CLI/Processors/listprocessors")
        self.telorb.expect ("\n")

        raw = self.waitForPrompt ()
        processors = []
        for processor in raw.splitlines ():
            if processor:
                processors.append (processor)

        return processors

# The Backups class
##############################################################################

class Backups (dict):
    def __init__ (self, backups, tutil):
        self.tutil = tutil
        self.backups = backups
        self.update (backups)

    @property
    def active (self):
        return self.tutil.activeBackup

    def create (self, name):
        self.tutil.createBackup (name)

# The Backup class
##############################################################################

class Backup:
    def __init__ (self, name, tutil, active = False):
        self.name = name
        self.tutil = tutil
        self.active = active

    def activate (self):
        if not self.active:
            self.tutil.activateBackup (self.name)

    def remove (self):
        self.tutil.removeBackup (self.name)

    def __str__ (self):
        return self.name

    def __repr__ (self):
        if self.active:
            return "(A)%s" % self.name
        else:
            return self.name

# The Processor class
##############################################################################

class Processor:
    def __init__ (self, name, tutil, telorb):
        self.name = name
        self.tutil = tutil
        self.telorb = telorb

    @property
    def processes (self):
        return Processes (self.tutil.getProcesses (self.name))

    @property
    def load (self):
        return self.tutil.getProcessorLoads (self.name)

# The Processes class
#  A wrapper around dict, to allow accessing processes by name and by PID
##############################################################################

class Processes (dict):
    def __init__ (self, processes):
        self.processes = processes
        self.update (processes)

    def __getitem__ (self, item):
        if isinstance (item, basestring):
            if item.isdigit ():
                return self.processes[int(item)]
            else:
                matches = []
                for process in self.processes.itervalues ():
                    if item == process.name:
                        matches.append (process)
                return matches
        elif isinstance (item, int):
            return self.processes[item]
        else:
            raise ValueError ("Unsupported type as key, only int, string (name or numeric) is supported")

# The Clusters class
#  A wrapper around dict, to allow accessing processes by name and by PID
##############################################################################

class Clusters (dict):
    def __init__ (self):
        self.clusters = {}
        self.update ({})

        self.readConfig ()

    def readConfig (self):
        config = ConfigParser.ConfigParser()
        config.read("/tmp/mml/ml_running.conf")
        for cluster in config.sections ():
            name = config.get (cluster, "name")
            platform_vip = config.get (cluster, "platform_vip")
            loader_ip = config.get (cluster, "loader_ip")
            int_vmif = config.get (cluster, "int_vmif")
            ext_vmif = config.get (cluster, "ext_vmif")
            self.clusters[name] = Cluster (name, platform_vip, loader_ip, ext_vmif, int_vmif)

        self.update (self.clusters)

# The Process class
##############################################################################

class Process:
    def __init__ (self, name, pid, tutil):
        self.name = name
        self.pid = pid
        self.tutil = tutil

    def __str__ (self):
        return self.name

    def __repr__ (self):
        return "%u:%s" % (self.pid, self.name)
