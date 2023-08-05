from yann.train import Trainer
import yann
from yann.params import HyperParams
from torch.optim import SGD


class RecognitionParams(HyperParams):
  checkpoint: str = None
  pretrained = True

  warmup = None
  optimizer = 'SGD'
  learning_rate = 0.01
  momentum = .9
  weight_decay = 0.0001


  label_smoothing = 0.1

  loss = 'soft_target_cross_entry'

  notebook = False


  sizes = None  # 160, 160, 224, 224, 360

  mixup = False
  manifold_mixup = False
  cutmix = False
  cutout = False
  autoaugment = False
  augmix = False



class RecognitionTrainer(Trainer):
  def __init__(
      self,
      model=None,
      dataset=None,
      optimizer=None,
      loss=None,
      loader=None,
      sampler=None,
      num_workers=8,
      transform=None,
      transform_batch=None,
      lr_scheduler=None,
      lr_batch_step=False,
      callbacks=None,
      device=None,
      parameters='trainable',
      batch_size=16,
      val_dataset=None,
      val_loader=None,
      val_transform=None,
      classes=None,
      parallel=False,
      name=None,
      description=None,
      root='./experiments/train-runs/',
      metrics=None,
      collate=None,
      params=None,
      pin_memory=True,
      step=None,
      id=None

  ):

    model = model or yann.resolve.model('resnet50', pretrained=True)

    optimizer = optimizer or SGD(model.parameters(), momentum=.9)

    super(RecognitionTrainer, self).__init__(
      model=model or 'resnet50',
      optimizer=optimizer or
    )