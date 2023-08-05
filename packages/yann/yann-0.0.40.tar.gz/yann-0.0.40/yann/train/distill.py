from .supervised import Trainer


class DistilledTrainer(Trainer):
  def __init__(self, student, teacher, **kwargs):
    super(DistilledTrainer, self).__init__(model=student, **kwargs)
    self.teacher = teacher

  @property
  def student(self):
    return self.model
