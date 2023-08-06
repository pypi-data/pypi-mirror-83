#!/usr/bin/env python

from __future__ import absolute_import
import os
import logging

from linchpin.version import __version__
from linchpin.exceptions import LinchpinError

# FIXME: remove this later when not using python2.6
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

try:
    import configparser as ConfigParser
except ImportError:
    import configparser as ConfigParser


class LinchpinContext(object):

    """
    LinchpinContext object, which will be used to manage the cli,
    and load the configuration file.
    """


    def __init__(self):
        """
        Initializes basic variables
        """

        self.version = __version__
        self.verbosity = 1
        self.no_monitor = False

        self.lib_path = '{0}'.format(os.path.dirname(
                                     os.path.realpath(__file__)))

        self.cfgs = {}
        self._load_constants()
        self.env_vars = ()
        self.use_shell = False


    def _load_constants(self):
        """
        Create self.cfgs with defaults from the linchpin constants file.
        """

        constants_file = '{0}/linchpin.constants'.format(self.lib_path)
        constants_file = os.path.realpath(os.path.expanduser(constants_file))
        self._parse_config(constants_file)


    def load_config(self, workspace=None, config_path=None, search_path=None):
        """

        Update self.cfgs from the linchpin configuration file (linchpin.conf).

        The following paths are used to find the config file.
        The search path defaults to the first-found order::

          * /etc/linchpin.conf
          * /linchpin/library/path/linchpin.conf
          * <workspace>/linchpin.conf

        An alternate search_path can be passed.

        :param search_path: A list of paths to search a linchpin config
        (default: None)
        """

        if workspace:
            self.workspace = os.path.realpath(workspace)

        if workspace in dir(self):
            self.workspace = os.path.realpath(os.path.curdir)

        expanded_path = None

        if config_path:
            CONFIG_PATH = [config_path]
        else:
            CONFIG_PATH = [
                '/etc/linchpin.conf',
                '~/.config/linchpin/linchpin.conf',
            ]
            if workspace in dir(self):
                CONFIG_PATH.append('{0}/linchpin.conf'.format(self.workspace))

        existing_paths = []
        for path in CONFIG_PATH:
            expanded_path = (
                "{0}".format(os.path.realpath(os.path.expanduser(path))))

            # implement first found
            if os.path.exists(expanded_path):
                # logging before the config file is setup doesn't work
                # if messages are needed before this, use print.
                existing_paths.append(expanded_path)

        for path in existing_paths:
            self._parse_config(path)

        pass


    def _parse_config(self, path):
        """
        Parse configs into the self.cfgs dict from provided path.

        :param path: A path to a config to parse
        """

        try:
            config = ConfigParser.ConfigParser()
            f = open(path)
            config.read_file(f)
            f.close()

            for section in config.sections():
                if not self.cfgs.get(section):
                    self.cfgs[section] = {}

                for k in config.options(section):
                    if section == 'evars':
                        try:
                            self.cfgs[section][k] = (
                                config.getboolean(section, k)
                            )
                        except ValueError:
                            self.cfgs[section][k] = config.get(section, k)
                    else:
                        try:
                            self.cfgs[section][k] = config.get(section, k)
                        except ConfigParser.InterpolationMissingOptionError:
                            value = config.get(section, k, raw=True)
                            self.cfgs[section][k] = value.replace('%%', '%')

        except ConfigParser.InterpolationSyntaxError as e:
            raise LinchpinError('Unable to parse configuration file properly:'
                                ' {0}'.format(e))


    def load_global_evars(self):

        """
        Instantiate the evars variable, then load the variables from the
        'evars' section in linchpin.conf. This will then be passed to
        invoke_linchpin, which passes them to the Ansible playbook as needed.

        """

        self.evars = self.cfgs.get('evars', {})
        env_vars = self.cfgs.get('env_vars', {})
        env_vars_list = list(self.env_vars)
        for k in env_vars:
            env_vars_list.append((k, env_vars[k]))
        self.env_vars = tuple(env_vars_list)



    def get_cfg(self, section=None, key=None, default=None):
        """
        Get cfgs value(s) by section and/or key, or the whole cfgs object

        :param section: section from ini-style config file

        :param key: key to get from config file, within section

        :param default: default value to return if nothing is found.
        Does not apply if section is not provided.
        """

        if section:
            s = self.cfgs.get(section, default)
            if key and s:
                return self.cfgs[section].get(key, default)
            return s
        return self.cfgs


    def set_cfg(self, section, key, value):
        """
        Set a value in cfgs. Does not persist into a file,
        only during the current execution.

        :param section: section within ini-style config file
        :param key: key to use
        :param value: value to set into section within config file
        """

        if not self.cfgs.get(section):
            self.cfgs.update({section: {}})

        self.cfgs[section][key] = value


    def get_evar(self, key=None, default=None):
        """
        Get the current evars (extra_vars)

        :param key: key to use

        :param default: default value to return if nothing is found
        (default: None)
        """

        if key:
            return self.evars.get(key, default)

        return self.evars


    def set_evar(self, key, value):
        """
        Set a value into evars (extra_vars). Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """

        self.set_cfg('evars', key, value)


    def get_env_vars(self, key=None, default=None):
        """
        Get the current env_vars

        :param key: key to use

        :param default: default value to return if nothing is found
        (default: None)
        """

        if key:
            for kv in self.env_vars:
                if key == kv[0]:
                    return kv[1]
            return default
        return self.env_vars


    def set_env_vars(self, key, value):
        """
        Set a value into env_vars. Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """
        env_vars_tuple = self.env_vars
        env_vars_tuple = [x for x in env_vars_tuple]
        set_env = False
        for kv in self.env_vars:
            if key == kv[0]:
                env_vars_tuple.remove(kv)
                env_vars_tuple.append((key, value))
                set_env = True
        if not set_env:
            env_vars_tuple.append((key, value))
        self.env_vars = tuple(env_vars_tuple)


    def setup_logging(self):

        """
        Setup logging to the console only

        .. attention:: Please implement this function in a subclass

        """

        self.console = logging.getLogger('lp_console')
        if not self.console.handlers:
            self.console.setLevel(logging.INFO)

            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            formatter = \
                logging.Formatter('%(levelname)s %(asctime)s %(message)s')
            ch.setFormatter(formatter)

            self.console.addHandler(ch)


    def log(self, msg, **kwargs):
        """
        Logs a message to a logfile

        :param msg: message to output to log

        :param level: keyword argument defining the log level

        """

        lvl = kwargs.get('level')

        if lvl is None:
            lvl = logging.INFO

        self.console.log(logging.INFO, msg)


    def log_info(self, msg):
        """Logs an INFO message"""

        self.log(msg, level=logging.INFO)


    def log_debug(self, msg):
        """Logs a DEBUG message"""

        self.log(msg, level=logging.DEBUG)


    def log_state(self, msg):
        """
        Logs nothing, just calls pass

        .. attention:: state messages need to be implemented in a subclass
        """

        pass
