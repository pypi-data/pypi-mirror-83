from __future__ import absolute_import
from ansible.plugins.callback import CallbackBase
from .utils import ansible_version_recognizer as avr


class PlaybookCallback(CallbackBase):

    """Playbook callback"""


    def __init__(self, display=None, options=None):

        # note the following if else ladder should be restructured after
        # linchpin ansible minimum requirements changed until then
        # code should be remained unchanged to maintain backward
        # compatibility to ansible 2.3.1 version
        if avr.ansibleverisgreaterthan(2.4):
            self._load_name = None
            super(PlaybookCallback, self).__init__(display=display,
                                                   options=options)
        elif avr.ansibleverisgreaterthan(2.3):
            super(PlaybookCallback, self).__init__(display=display,
                                                   options=options)
        else:
            # since ansible 2.3.1 version does not support options in
            # inside PlaybbookCallback the options are omitted
            super(PlaybookCallback, self).__init__(display=display)

        self._options = options
        self._display.verbosity = options.verbosity

        # store all results
        self.results = {'failed': [], 'ok': []}


    def v2_runner_on_ok(self, result):

        """Save ok result"""

        self.results['ok'].append(result)

    def v2_runner_on_failed(self, result, **kwargs):

        """Save failed result"""

        ignore_errors = kwargs.get('ignore_errors')

        if not ignore_errors:
            self.results['failed'].append(result)
