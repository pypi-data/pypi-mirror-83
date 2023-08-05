from yann.train.supervised import Trainer



class MulticlassTrainer(Trainer):
  def __init__(
      self,
      **kwargs
  ):

    super(MulticlassTrainer, self).__init__(**kwargs)