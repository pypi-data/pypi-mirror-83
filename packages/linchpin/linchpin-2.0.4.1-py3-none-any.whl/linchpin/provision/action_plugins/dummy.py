from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
import linchpin.MockUtils.MockUtils as mock_utils
from time import sleep
from mock import MagicMock
import zmq


class ActionModule(ActionBase):
    ''' Send events to Nanomsg '''

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        vm = self._task.get_variable_manager()
        if vm.extra_vars.get('no_monitor', False):
            def get_dict(context, key):
                return context.__context_dict[key]

            def set_dict(context, key, value):
                context.__context_dict[key] = value

            context = MagicMock()
            context.__context_dict = {}
            context.__getitem__ = get_dict
            context.__setitem__ = set_dict
            wait = 0
        else:
            context = zmq.Context()
            wait = 2
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5599")
        socket.RCVTIMEO = 2000

        if task_vars is None:
            task_vars = dict()
        name = "{}({})".format(self._task.args['name'],
                               self._task.args['count'])
        msg = dict(status=dict(target=name, state='Provisioning'), bar=50)
        socket.send_string(str(msg))
        socket.recv_string()

        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        linchpin_mock = task_vars['vars'].get('linchpin_mock',
                                              False)
        if linchpin_mock:
            return mock_utils.get_mock_data(module_args,
                                            "dummy")
        else:
            module_return = self._execute_module(module_name='dummy',
                                                 module_args=module_args,
                                                 task_vars=task_vars, tmp=tmp)
        del tmp  # tmp no longer has any effect
        sleep(wait)

        msg = dict(status=dict(target=name, state='Done'), bar=50)
        socket.send(str(msg).encode('utf-8'))
        socket.recv_string()
        sleep(wait)

        return module_return
