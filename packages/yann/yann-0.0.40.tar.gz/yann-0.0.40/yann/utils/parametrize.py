"""
TODO: way to wrap a function to parametrize it with a random function or argument generator,
 track parameters used and outputs



augment = partial(resize, width=N(0,1))

outputs, params = augment.parametrized(image)
outputs = augment(image)
outputs = augment(image, width=20)


augment = partial(resize, width=Schedule())
augment = partial(resize, width=Compute())  # compute param as a function of provided params

augment.width = 3

"""
# class Partial:
#   def __init__(self, func, **kwargs):
#     self.func = func
#     self.kwargs = kwargs
#
#   def __call__(self, *args, **kwargs):
#     return self.func(*args, **kwargs)
#
# resize = yann.partial(resize, width=N(0 ,1), U(0 ,10))