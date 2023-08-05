from collections import defaultdict

class Callback:
  def on_train_start(self, trainer=None):
    pass

  def on_epoch_start(self, epoch=None, trainer=None):
    pass

  def on_batch_start(self, batch=None, inputs=None, targets=None, trainer=None):
    pass

  def on_batch_end(self, batch=None, inputs=None, targets=None, outputs=None, loss=None,
                   trainer=None):
    pass

  def on_epoch_end(self, epoch=None, loss=None, metrics=None, trainer=None):
    pass

  def on_validation_start(self, trainer=None):
    pass

  def on_validation_batch(self, inputs=None, targets=None, outputs=None, trainer=None):
    pass

  def on_validation_end(self, targets=None, outputs=None, loss=None,
                        trainer=None):
    pass

  def on_train_end(self, trainer=None):
    pass

  def on_batch_error(self, batch=None, error=None, trainer=None):
    pass

  def on_error(self, error=None, trainer=None):
    pass


class FunctionCallback(Callback):
  _valid_names = {
    'train_start',
    'epoch_start',
    'batch_start',
    'batch_end',
    'epoch_end',
    'validation_start',
    'validation_batch',
    'validation_end',
    'train_end',
    'error',
  }

  def __init__(self, callbacks=None):
    self.callbacks = callbacks or defaultdict(list)

  def on(self, event, callback):
    if event not in self._valid_names:
      raise ValueError(
        f'{event} is not a valid option, '
        f'must be one of {self._valid_names}')
    callbacks = self.callbacks[event]
    if callback not in callbacks:
      callbacks.append(callback)

  def on_train_start(self, *args, **kwargs):
    for f in self.callbacks['train_start']:
      f(*args, **kwargs)

  def on_epoch_start(self, *args, **kwargs):
    for f in self.callbacks['epoch_start']:
      f(*args, **kwargs)

  def on_batch_start(self, *args, **kwargs):
    for f in self.callbacks['batch_start']:
      f(*args, **kwargs)

  def on_batch_end(self, *args, **kwargs):
    for f in self.callbacks['batch_end']:
      f(*args, **kwargs)

  def on_epoch_end(self, *args, **kwargs):
    for f in self.callbacks['epoch_end']:
      f(*args, **kwargs)

  def on_validation_start(self, *args, **kwargs):
    for f in self.callbacks['validation_start']:
      f(*args, **kwargs)

  def on_validation_batch(self, *args, **kwargs):
    for f in self.callbacks['validation_batch']:
      f(*args, **kwargs)

  def on_validation_end(self, *args, **kwargs):
    for f in self.callbacks['validation_end']:
      f(*args, **kwargs)

  def on_train_end(self, *args, **kwargs):
    for f in self.callbacks['train_end']:
      f(*args, **kwargs)

  def on_error(self, *args, **kwargs):
    for f in self.callbacks['error']:
      f(*args, **kwargs)


class TempCallback(Callback):
  def __init__(self, callback, steps=None, epochs=None):
    self.callback = callback
    self.steps = steps
    self.epochs = epochs

  def unregister(self):
    raise NotImplementedError()

  def on_batch_end(self, batches, *args, **kwargs):
    if self.steps and self.steps < batches:
      self.unregister()

  def on_epoch_end(self, epoch=None, loss=None, metrics=None, trainer=None):
    if self.epochs and self.epochs < epoch:
      self.unregister()