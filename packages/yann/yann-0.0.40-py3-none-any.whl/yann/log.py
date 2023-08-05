from logging import Logger as PythonLogger


class Logger(PythonLogger):
  def __init__(self, **context):
    super(Logger, self).__init__()

    self.context = context

  def log(self, level: int, msg: Any, *args: Any, exc_info: _ExcInfoType = ...,
                stack_info: bool = ..., extra: Optional[Dict[str, Any]] = ...,
                **kwargs: Any) -> None:
    pass

  def __call__(self, *args, **kwargs):
    pass


#
# log = Logger()
#
#
# import torch
# log.debug(tensor=torch.rand(3,3))
# log.info(image=image)
# log.info()
#
#
# log.warning()