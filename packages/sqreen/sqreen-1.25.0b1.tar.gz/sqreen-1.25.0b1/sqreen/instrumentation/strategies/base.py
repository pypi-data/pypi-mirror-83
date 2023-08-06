# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
""" Base strategy
"""
import logging
from bisect import bisect
from collections import defaultdict

LOGGER = logging.getLogger(__name__)


class BaseStrategy(object):
    """ The base strategy holds callbacks for a hook point

    Subclasses need to define way to hook and deinstrument.
    BaseStrategy accepts a channel, usually passed from Instrumentation
    directly.
    """

    def __init__(
        self, observation_queue, queue, import_hook, before_hook_point=None
    ):
        self.observation_queue = observation_queue
        self.queue = queue
        self.unique_callbacks = set()
        # Data structure for {[hook_module, hook_name]: {pre: [], post: [], fail: []}}
        self.callbacks = defaultdict(lambda: defaultdict(list))
        self.import_hook = import_hook

        self.hooked = False

        self._before_hook_point = before_hook_point

    def add_callback(self, callback):
        """ Add a callback on a specific endpoint defined by the couple
        (hook_module, hook_name) embedded in callback
        """
        key = (callback.hook_module, callback.hook_name)

        methods = callback.lifecycle_methods

        # Normal order insertion
        if "pre" in methods:
            callbacks = self.callbacks[key]["pre"]
            idx = bisect([c.priority for c in callbacks], callback.priority)
            callbacks.insert(idx, callback)

        # Reverse order insertion
        for method in ("post", "failing"):
            if method in methods:
                rev_callbacks = list(reversed(self.callbacks[key][method]))
                idx = bisect([c.priority for c in rev_callbacks], callback.priority)
                rev_callbacks.insert(idx, callback)
                rev_callbacks.reverse()
                self.callbacks[key][method] = rev_callbacks

        self.unique_callbacks.add(callback)

    def hook(self):
        pass

    def get_pre_callbacks(self, key):
        """ Returns callbacks with a pre lifecycle method for the key
        (hook_module, hook_name)
        """
        return self.callbacks[key]["pre"]

    def get_post_callbacks(self, key):
        """ Returns callbacks with a post lifecycle method for the key
        (hook_module, hook_name)
        """
        return self.callbacks[key]["post"]

    def get_failing_callbacks(self, key):
        """ Returns callbacks with a failing lifecycle method for the key
        (hook_module, hook_name)
        """
        return self.callbacks[key]["failing"]

    def _total_callbacks(self):
        """ Count the total number of callbacks
        """
        return len(self.unique_callbacks)

    def deinstrument(self, callback):
        """ Deactivate the callback for this endpoint.
        If it was the latests callback for this endpoint, restore the original
        hooked function.
        """
        key = (callback.hook_module, callback.hook_name)

        callbacks = self.callbacks[key]
        methods = callback.lifecycle_methods

        LOGGER.debug("Deinstrumenting %s", callback)

        for method in ("pre", "post", "failing",):
            if method in methods:
                try:
                    callbacks[method].remove(callback)
                except ValueError:
                    # Callback has not been added in this strategy
                    msg = "Callback %s %s trying to be deinstrumented but not instrumented"
                    LOGGER.warning(msg, method, callback)

        try:
            self.unique_callbacks.remove(callback)
        except KeyError:
            pass

        LOGGER.debug(
            "Number of remaining callback for %s: %s",
            self,
            self._total_callbacks(),
        )

        # If no more callbacks are set deinstrument
        if self._total_callbacks() == 0:
            self._restore()

    def deinstrument_all(self):
        """ Deinstrument all callbacks
        """
        for callback in list(self.unique_callbacks):
            self.deinstrument(callback)

        self.unique_callbacks = set()

    def _restore(self):
        """ Restore the original method, subclasses need to overload this method
        """
        self.hooked = False

    def before_hook_point(self):
        """ Run code just before running a hook_point
        """
        if self._before_hook_point is not None:
            self._before_hook_point()
