import re
import sys

import numpy as np
import torch
from PIL import Image
import datetime


def timestr(d=None):
  return f"{(d or datetime.datetime.utcnow()).strftime('%y-%m-%dT%H:%M:%S')}"


def camel_to_snake(text):
  s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def abbreviate(text):
  return re.sub(r"([a-zA-Z])[a-z]*[^A-Za-z]*",r"\1", text).lower()


def get_arg_parser(x, description=None, epilog=None, parser=None, **kwargs):
  import argparse
  from ..params import Field
  parser = parser or argparse.ArgumentParser(description=description, epilog=epilog, **kwargs)

  abbreviations = set()

  for k, v in x.items():
    names = []
    abbreviated = abbreviate(k)
    if abbreviated not in abbreviations:
      names.append(f"-{abbreviated}")
      abbreviations.add(abbreviated)
    names.append(f"--{camel_to_snake(k)}")

    if isinstance(v, dict):
      parser.add_argument(
        *names,
        default=v.get('default'),
        type=v.get('type'),
        action=v.get('action'),
        help=v.get('help'),
        required=v.get('required'),
        choices=v.get('choices'),
        dest=v.get('dest')
      )
    elif isinstance(v, Field):
      parser.add_argument(
        *names,
        default=v.default,
        type=v.type,
        help=f"{v.help or k} (default: {v.default})",
        required=v.required,
        choices=getattr(v, 'choices', None),
      )
    else:
      parser.add_argument(*names, default=v, type=type(v))
  return parser


def truthy(items):
  return [x for x in items if x]


class Obj(dict):
  __setattr__ = dict.__setitem__
  __getattr__ = dict.__getitem__


def almost_equal(t1, t2, prec=1e-12):
  return torch.all(torch.lt(torch.abs(torch.add(t1, -t2)), prec))


def equal(t1, t2):
  return torch.all(t1 == t2)


def randimg(*shape, dtype='uint8'):
  return Image.fromarray((np.random.rand(*shape) * 255).astype(dtype))


def progress(it, num=None):
  if not num:
    try:
      num = len(it)
    except:
      num = None

  if num:
    for n, x in enumerate(it, 1):
      sys.stdout.write(f"\r{n} / {num}")
      sys.stdout.flush()
      yield x
  else:
    for n, x in enumerate(it, 1):
      sys.stdout.write(f"\r{n}")
      sys.stdout.flush()
      yield x


def repeat(val):
  while True:
    yield val


def counter(start=0, end=None, step=1):
  current = start
  while end is None or (end and (current < end)):
    yield current
    current += step


def to_numpy(x):
  if isinstance(x, np.ndarray):
    return x
  if torch.is_tensor(x):
    return x.to('cpu').detach().numpy()
  return np.array(x)


class RangeMap(dict):
  def __init__(self, items=None):
    super().__init__()

    if isinstance(items, dict):
      items = items.items()

    if items:
      for k, v in items:
        self[k] = v

  def __getitem__(self, item):
    if isinstance(item, tuple):
      return super().__getitem__(item)

    if item is not None:
      for (min, max), value in self.items():
        if min is not None and item < min:
          continue
        if max is not None and item > max:
          continue
        return value

    raise KeyError(f'Key `{item}` does not fall in any of the ranges')

  def __call__(self, item):
    return self[item]


def pretty_size(bytes):
  num = bytes
  for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    if num < 1024.0:
      return f'{num:3.1f} {unit}'
    num /= 1024.0


def print_tree(root, indent=2, depth=None, filter=None):
  from pathlib import Path
  from datetime import datetime
  root = Path(root)
  for path in sorted((root, *root.rglob('*'))):
    d = len(path.relative_to(root).parts)
    if depth and depth < d:
      continue
    if not path.is_dir() and filter and not path.match(filter):
      continue
    if path.is_dir():
      print(f'{" " * (d * indent)} /{path.name}/')
    else:
      print(
        f'{" " * (d * indent)}  - {path.name:25} '
        f'{f"({pretty_size(path.stat().st_size)})":15} '
        f'{datetime.fromtimestamp(path.stat().st_mtime)}'
      )


def fully_qualified_name(x):
  module = x.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return x.__class__.__name__
  else:
    return f'{module}.{x.__class__.__name__}'


def hash_params(module):
    from hashlib import sha1
    s = sha1()
    for p in module.parameters():
      s.update(to_numpy(p).tobytes())
    return s.hexdigest()