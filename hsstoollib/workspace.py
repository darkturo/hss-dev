#!/usr/bin/python

import os.path
import json

class SerializableConfig (object):
    """
    The SerializableConfig class

    Used as a base class for the configuration objects to contain the methods
    for converting from dictionaries to strings representing the objects.
    """

    @staticmethod
    def convertFromStringToDict (string):
        return json.loads (string)

    @staticmethod
    def convertFromDictToString (values):
        return json.dumps (values, indent=2)

    def serialize (self, values = None):
        if not values:
            values = self.__dict__

        return SerializableConfig.convertFromDictToString (values)

    @staticmethod
    def unserialize (string, cls, config):
        data = SerializableConfig.convertFromStringToDict (string)
        obj = cls.createObject (cls, data)
        obj.populateFromDict (data, config)
        return obj

    @staticmethod
    def createObject (cls, data):
        return cls.__new__ (cls)

    def populateFromDict (self, data, config):
        for attr, value in data.iteritems ():
            setattr (self, attr, value)


class Code (SerializableConfig):
    def __init__ (self, name, epws, arch = "x86_64"):
        self.name = name
        self.epws = epws
        self.arch = arch

    def build (self, rebuild = False):
        pass

    @staticmethod
    def createObject (cls, data):
        # Decide whether we should create a Code or BuildableCode object
        if data.has_key ("buildable") and data["buildable"]:
            return BuildableCode.__new__(BuildableCode)
        else:
            return Code.__new__ (Code)

class BuildableCode(Code):
    def __init__ (self, name, epws, base, arch = "x86_64"):
        super(BuildableCode, self).__init__ (name, epws, arch)
        self.base = base
        self.buildable = True

    def build (self, rebuild = False):
        pass

class Runtime (SerializableConfig):
    def __init__ (self, name, testsuite):
        self.name = name
        self.testsuite = testsuite

    def start (self):
        pass

    def stop (self):
        pass

class Workspace (SerializableConfig):
    def __init__ (self, name, code, runtime):
        self.name = name
        self.code = code
        self.runtime = runtime

    def serialize (self):
        return super(Workspace, self).serialize ({"name" : self.name, "code" : self.code.name, "runtime" : self.runtime.name})

    def populateFromDict (self, data, config):
        self.name = data["name"]

        self.code = config.read (Code, data["code"])
        self.runtime = config.read (Runtime, data["runtime"])

class Configuration:
    """
    The Configuration class.

    Responsible for getting, setting and reading, saving the configuration
    objects: Code, Runtime and Workspace.

    It keeps track of the relevant paths and delegates seralizing and
    unserializing to the SerializableConfig objects.
    """

    def __init__ (self, root=None):
        if root:
            self.root = root
        else:
            self.root = os.path.expanduser ("~/.hss")

        self.codes_path = os.path.join (self.root, "codes")
        self.runtimes_path = os.path.join (self.root, "runtimes")
        self.workspaces_path = os.path.join (self.root, "workspaces")

        self.verifyConfig ()

    def verifyConfig (self):
        # Verify that all the relevant paths exist
        if not os.path.isdir (self.root):
            os.makedirs (self.root)

        if not os.path.isdir (self.codes_path):
            os.makedirs (self.codes_path)

        if not os.path.isdir (self.runtimes_path):
            os.makedirs (self.runtimes_path)

        if not os.path.isdir (self.workspaces_path):
            os.makedirs (self.workspaces_path)

    def getPathFromObject (self, obj):
        if isinstance (obj, Code):
            path = self.codes_path
        elif isinstance (obj, Runtime):
            path = self.runtimes_path
        elif isinstance (obj, Workspace):
            path = self.workspaces_path
        else:
            raise ValueError ("Unrecognized object!")
        
        filename = obj.name + ".json"
        return os.path.join (path, filename)

    def getPathFromClass (self, cls, name):
        if cls == Code:
            path = self.codes_path
        elif cls == Runtime:
            path = self.runtimes_path
        elif cls == Workspace:
            path = self.workspaces_path
        else:
            raise ValueError ("Unrecognized object!")
        
        filename = name + ".json"
        return os.path.join (path, filename)

    def write (self, obj):
        with open (self.getPathFromObject (obj), "w") as f:
            f.write (obj.serialize ())

    def read (self, cls, name):
        with open (self.getPathFromClass (cls, name), "r") as f:
            return SerializableConfig.unserialize (f.read(), cls, self)

if __name__ == "__main__":

    config = Configuration ()

    #code = BuildableCode ("Code1", "/local/tmp", "/local/scratch/src")
    #runtime = Runtime ("Runtime1", "ts_hss_cxderegister")
    #workspace = Workspace ("TR", code, runtime)
    #config.write (code)
    #config.write (runtime)
    #config.write (workspace)

    code = config.read (Code, "Code1")
    print code.__dict__
    runtime = config.read (Runtime, "Runtime1")
    print runtime.__dict__
    workspace = config.read (Workspace, "TR")
    print workspace.code.epws
    print workspace.runtime.testsuite
