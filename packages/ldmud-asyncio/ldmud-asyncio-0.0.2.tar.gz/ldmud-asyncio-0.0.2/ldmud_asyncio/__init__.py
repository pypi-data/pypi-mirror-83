import asyncio, collections, heapq, select, selectors, signal, threading
import ldmud

class LDMudSelector(selectors.BaseSelector):
    """LDMud selector.

    This selector uses the LDMud backend loop to wait for a
    socket to become ready. The select function here will not wait,
    instead the select results will be passed directly to
    loop.run_select_event().
    """

    class Mapping(collections.abc.Mapping):
        """A mapping of file objects to selector keys.

        It uses the mapping of file descriptors to keys
        from the LDMudSelector to present a read-only
        mapping from file objects to selector keys.
        """

        def __init__(self, filemap):
            self._filemap = filemap

        def __len__(self):
            return len(self._filemap)

        def __getitem__(self, fileobj):
            try:
                fd = LDMudSelector._get_fd_from_fileobj(fileobj)
            except:
                fd = -1

            if fd >= 0:
                return self._filemap[fd]

            # Search the map
            for key in self._filemap.values():
                if key.fileobj is fileobj:
                    return key

        def __iter__(self):
            return iter(self._selector._fd_to_key)

    def __init__(self):
        self._filemap = {} # fd -> key

    def register(self, fileobj, events, data=None):
        key = selectors.SelectorKey(fileobj, self._get_fd_from_fileobj(fileobj), events, data)
        if key.fd in self._filemap:
            raise KeyError("File is already registered")
        self._filemap[key.fd] = key

        def callback(cbmask):
            cbevents = 0
            if cbmask & select.POLLIN:
                cbevents |= selectors.EVENT_READ
            if cbmask & select.POLLOUT:
                cbevents |= selectors.EVENT_WRITE
            asyncio.get_event_loop().run_select_event(key, cbevents & key.events)

        mask = 0
        if events & selectors.EVENT_READ:
            mask |= select.POLLIN
        if events & selectors.EVENT_WRITE:
            mask |= select.POLLOUT

        ldmud.register_socket(key.fd, callback, mask)

    def unregister(self, fileobj):
        key = self.get_key(fileobj)
        del self._filemap[key.fd]
        ldmud.unregister_socket(key.fd)
        return key

    def select(self, timeout=None):
        return []

    def close(self):
        for key in self._filemap.values():
            self.unregister(self, key.fileobj)

    def get_map(self):
        return LDMudSelector.Mapping(self._filemap)

    @staticmethod
    def _get_fd_from_fileobj(fileobj):
        """Returns the file descriptor for a file object.

        The file object needs either to be an integer (the descriptor itself)
        or have a fileno() function that returns the descriptor.
        """
        if isinstance(fileobj, int):
            return fileobj
        else:
            return int(fileobj.fileno())

class LDMudEventLoop(asyncio.SelectorEventLoop):
    """LDMud event loop.

    Event loop representing the LDMud backend loop.
    """

    def __init__(self):
        super().__init__(selector = LDMudSelector())
        self._thread_id = threading.get_ident()
        self._clock_resolution = 1
        self._sigchld_handler_handle = None
        asyncio._set_running_loop(self)

        ldmud.register_hook(ldmud.ON_HEARTBEAT, self._heart_beat)
        ldmud.register_hook(ldmud.ON_CHILD_PROCESS_TERMINATED, self._signal_handler)

    def _heart_beat(self):
        """Called from LDMud upon each heart beat.

        Check all pending timers and execute any expired timers.
        """
        self.run_ready()

        # If half of the timers are cancelled, clean the queue.
        if 2 * self._timer_cancelled_count > len(self._scheduled):
            active_timers = []
            for timer in self._scheduled:
                if timer._cancelled:
                    timer._scheduled = False
                else:
                    active_timers.append(timer)
            heapq.heapify(active_timers)
            self._scheduled = active_timers
            self._timer_cancelled_count = 0

        # Now execute any expired timers.
        now = self.time()
        while self._scheduled:
            if self._scheduled[0]._cancelled:
                timer = heapq.heappop(self._scheduled)
                timer._scheduled = False
                self._timer_cancelled_count -= 1
                continue

            if self._scheduled[0]._when > now:
                break

            timer = heapq.heappop(self._scheduled)
            timer._scheduled = False
            timer._run()
            self.run_ready()

    def run_forever(self):
        raise RuntimeError("The LDMud backend loop runs automatically.")

    def run_until_complete(self, future):
        raise RuntimeError("The LDMud backend loop runs automatically.")

    def stop(self):
        raise RuntimeError("To stop the LDMud backend loop you need to call the efun shutdown().")

    def close(self):
        pass

    def _signal_handler(self):
        """LDMud received a SIGCHLD.

        If there is a registered handler, call it.
        """
        if self._sigchld_handler_handle is None:
            return
        if self._sigchld_handler_handle._cancelled:
            self._sigchld_handler_handle = None
            return

        self._add_callback(self._sigchld_handler_handle)
        self.run_ready()

    def add_signal_handler(self, sig, callback, *args):
        if sig != signal.SIGCHLD:
            raise RuntimeError("Only signal handlers for SIDCHLD are supported.")
        self._sigchld_handler_handle = asyncio.Handle(callback, args, self, None)

    def remove_signal_handler(self, sig):
        if sig != signal.SIGCHLD:
            raise RuntimeError("Only signal handlers for SIDCHLD are supported.")
        self._sigchld_handler_handle = None

    def run_ready(self):
        """Run all tasks in the _ready list."""
        while len(self._ready):
            handle = self._ready.popleft()
            if handle._cancelled:
                continue
            if self._debug:
                try:
                    self._current_handle = handle
                    t0 = self.time()
                    handle._run()
                    dt = self.time() - t0
                    if dt >= self.slow_callback_duration:
                        logger.warning('Executing %s took %.3f seconds',
                                       _format_handle(handle), dt)
                finally:
                    self._current_handle = None
            else:
                handle._run()

    def run_select_event(self, key, event):
        """Run the task associated with the given selector key."""
        self._process_events(((key, event,),))
        self.run_ready()

class LDMudDefaultEventLoopPolicy(asyncio.AbstractEventLoopPolicy):
    """Event loop policy for LDMud.

    We have  only one thread, there we have only one loop
    which is the LDMud backend loop. There is currently no
    support for watching child processes.
    """

    _loop_factory = LDMudEventLoop

    def __init__(self):
        self._loop = None
        self._watcher = None
        self._set_called = False

    def get_event_loop(self):
        if self._loop is None and not self._set_called:
            self.set_event_loop(self.new_event_loop())

        return self._loop

    def set_event_loop(self, loop):
        assert loop is None or isinstance(loop, asyncio.AbstractEventLoop)

        self._set_called = True
        self._loop = loop
        if self._watcher:
            self._watcher.attach_loop(loop)

    def new_event_loop(self):
        return self._loop_factory()

    def get_child_watcher(self):
        if self._watcher is None:
            self._watcher = asyncio.SafeChildWatcher()
            if self._loop:
                self._watcher.attach_loop(self._loop)

        return self._watcher

    def set_child_watcher(self, watcher):
        assert watcher is None or isinstance(watcher, AbstractChildWatcher)

        if self._watcher is not None:
            self._watcher.close()

        self._watcher = watcher

def run(func):
    """Execute the given asynchronous function."""
    asyncio.ensure_future(func)
    asyncio.get_event_loop().run_ready()

asyncio.SelectorEventLoop = LDMudEventLoop
asyncio.DefaultEventLoopPolicy = LDMudDefaultEventLoopPolicy
asyncio.run = run

# We don't export anything, just monkey patch asyncio.
__all__ = []
