"""



sched = Linear(0, 10)

sched[1]


s = Sequence(
  Linear(0, 10, steps=100),

)


for size in sched:
  print(size)

"""


class Schedule:
  def __init__(self, steps=None):
    self.current_step = -1
    self.steps = steps

  def __len__(self):
    return self.steps

  def __getitem__(self, step):
    raise NotImplementedError()

  def __call__(self):
    self.current_step += 1


class Sequence(Schedule):
  def __init__(self, *schedules):
    self.schedules = list(schedules)

  def __len__(self):
    return sum((len(s) for s in self.schedules))

  def __getitem__(self, step):
    start = 0
    for s in self.schedules:
      if step < start + len(s):
        return s[step - start]

      start += len(s)

    raise IndexError()


class Constant(Schedule):
  def __init__(self, value, steps=None):
    self.value = value
    self.steps = steps

  def __getitem__(self, step):
    if step > self.steps:
      raise IndexError()
    return self.value


class Linear(Schedule):
  def __init__(self, start, end, steps):
    self.start = start
    self.end = end
    self.steps = steps

  def __getitem__(self, step):
    if step > self.steps:
      raise IndexError()
    return (self.end - self.start) / (self.steps - 1) * step


# class Lambda(Schedule):
#   def __init__(self, func):
#     pass
#
# class Random(Schedule):
#   pass
#
# class Warmup(Schedule):
#   pass
#
# class Restart(Schedule):
#   pass
#
#
# class Stop(Schedule):
#   """
#
#     sched = Stop(
#       sched,
#       lambda step: train.history.loss[-1] < 0
#     )
#   """
#   pass