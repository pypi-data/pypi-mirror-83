Queue-like items: iterable queues and channels.

*Latest release 20201025*:
Drop obsolete call to MultiOpenMixin.__init__.

## Class `Channel`

A zero-storage data passage.
Unlike a Queue(1), put() blocks waiting for the matching get().

### Method `Channel.__call__(self, *a)`

Call the Channel.
With no arguments, do a .get().
With an argument, do a .put().

### Method `Channel.close(self)`

Close the Channel, preventing further puts.

### Method `Channel.get(self, *a, **kw)`

Wrapper function to check that this instance is not closed.

### Method `Channel.put(self, *a, **kw)`

Wrapper function to check that this instance is not closed.

## Function `IterablePriorityQueue(capacity=0, name=None)`

Factory to create an iterable PriorityQueue.

## Function `IterableQueue(capacity=0, name=None)`

Factory to create an iterable Queue.

## `NullQ = <NullQueue:NullQ blocking=False>`

A queue-like object that discards its inputs.
Calls to .get() raise Queue_Empty.

## Class `NullQueue(cs.resources.MultiOpenMixin)`

A queue-like object that discards its inputs.
Calls to .get() raise Queue_Empty.

### Method `NullQueue.__init__(self, blocking=False, name=None)`

Initialise the NullQueue.

Parameters:
* `blocking`: if true, calls to .get() block until .shutdown().
  Default: False.
* `name`: a name for this NullQueue.

### Method `NullQueue.get(self)`

Get the next value. Always raises Queue_Empty.
If .blocking, delay until .shutdown().

### Method `NullQueue.put(self, item)`

Put a value onto the Queue; it is discarded.

### Method `NullQueue.shutdown(self)`

Shut down the queue.

### Method `NullQueue.startup(self)`

Start the queue.

## Class `PushQueue(cs.resources.MultiOpenMixin)`

A puttable object which looks like an iterable Queue.

Calling .put(item) calls `func_push` supplied at initialisation
to trigger a function on data arrival, whose processing is mediated
queued via a Later for delivery to the output queue.

### Method `PushQueue.__init__(self, name, functor, outQ)`

Initialise the PushQueue with the Later `L`, the callable `functor`
and the output queue `outQ`.

Parameters:
* `functor` is a one-to-many function which accepts a single
  item of input and returns an iterable of outputs; it may be a
  generator. These outputs are passed to outQ.put individually as
  received.
* `outQ` is a MultiOpenMixin which accepts via its .put() method.

### Method `PushQueue.put(self, *a, **kw)`

Wrapper function to check that this instance is not closed.

### Method `PushQueue.shutdown(self)`

shutdown() is called by MultiOpenMixin._close() to close
the outQ for real.

### Method `PushQueue.startup(self)`

Start up.

## Class `TimerQueue`

Class to run a lot of "in the future" jobs without using a bazillion
Timer threads.

### Method `TimerQueue.add(self, when, func)`

Queue a new job to be called at 'when'.
'func' is the job function, typically made with functools.partial.

### Method `TimerQueue.close(self, cancel=False)`

Close the TimerQueue. This forbids further job submissions.
If `cancel` is supplied and true, cancel all pending jobs.
Note: it is still necessary to call TimerQueue.join() to
wait for all pending jobs.

### Method `TimerQueue.join(self)`

Wait for the main loop thread to finish.

# Release Log



*Release 20201025*:
Drop obsolete call to MultiOpenMixin.__init__.

*Release 20200718*:
_QueueIterator: set finalise_later via new MultiOpenMixin property, required by recent MultiOpenMixin change.

*Release 20200521*:
IterableQueue,IterablePriorityQueue: simplify wrappers, bypasses weird bug from overengineering these.

*Release 20191007*:
* PushQueue: improve __str__.
* Clean lint, drop cs.obj dependency.

*Release 20190812*:
_QueueIterator: do MultiOpenMixin.__init__ so that __str__ is functional.

*Release 20181022*:
Bugfix Channel, drasticly simplify PushQueue, other minor changes.

*Release 20160828*:
* Use "install_requires" instead of "requires" in DISTINFO.
* TimerQueue.add: support optional *a and **kw arguments for func.
* Many bugfixes and internal changes.

*Release 20150115*:
More PyPI metadata fixups.

*Release 20150111*:
Initial PyPI release.
