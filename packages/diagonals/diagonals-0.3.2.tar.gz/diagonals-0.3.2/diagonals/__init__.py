import threading
import contextlib
import logging
import six

import numba.cuda

logger = logging.getLogger(__name__)


class Config(threading.local):
    """Run-time configuration controller."""

    def __init__(self, use_gpu=None):
        """
        A container for run-time options controls.
        To adjust the values simply update the relevant attribute from
        within your code. For example::
            diagonals.CONFIG.use_gpu = False
        If Iris code is executed with multiple threads, note the values of
        these options are thread-specific.

        """
        if use_gpu is None:
            use_gpu = numba.cuda.is_available()
        self.__dict__['use_gpu'] = use_gpu
        self.use_gpu = use_gpu

    def __repr__(self):
        return 'Config(use_gpu={0})'.format(self.use_gpu)

    def __setattr__(self, name, value):
        if name not in self.__dict__:
            msg = "'Config' object has no attribute {!r}".format(name)
            raise AttributeError(msg)
        if name == 'use_gpu':
            if value and not numba.cuda.is_available():
                logger.warning(
                    'CUDA is not available. Usage of GPU is disabled'
                )
                self.__dict__[name] = False
                return
        self.__dict__[name] = value

    @contextlib.contextmanager
    def context(self, **kwargs):
        """
        Return a context manager which allows temporary modification of
        the option values for the active thread.
        On entry to the `with` statement, all keyword arguments are
        applied to the Config object. On exit from the `with`
        statement, the previous state is restored.
        For example::
            with diagonals.CONFIG.context(cell_datetime_objects=False):
                # ... code that expects numbers and not datetimes
        """
        # Save the current context
        current_state = self.__dict__.copy()
        # Update the state
        for name, value in six.iteritems(kwargs):
            setattr(self, name, value)
        try:
            yield
        finally:
            # Return the state
            self.__dict__.clear()
            self.__dict__.update(current_state)


#: Object containing all the Iris run-time options.
CONFIG = Config()
