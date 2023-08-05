from yann.train.supervised import Trainer



class MultilabelTrainer(Trainer):
  def __init__(
      self,
      **kwargs
  ):

    super(MultilabelTrainer, self).__init__(**kwargs)