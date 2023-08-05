
from mypy_extensions import TypedDict
from typing import List, Optional

"""
/process/
/info/
/feedback/
/inputs/id/

POST /predict/

{
  inputs: [
    {
      id: 'asfsdfasf',
      base64: 'data:/asfsda
    }
  ]
  params: {
    word_threshold: .5,
    rotate: true,
    width: 400,
    vocab: [] 
  }
  
  meta: {
    client_id: 124123,
    session_id: 3414,
    
  }
}



{
  request_id: 'afdfa',
  results: [
    {
      id: 'asfsda',
      index: 0,
      text_lines: []
      boxes: [],
      transcript: []
    }
  ],
  params: {
    size: 800,
    correct: true
  },
  meta: {
    start_time: 141242,
    end_time: 31312,
  }
}
"""

UUID = str

class Meta(TypedDict):
  pass

class Input(TypedDict):
  id: Optional[UUID]
  meta: Optional[Meta]

class Base64Image(Input):
  base64: str


class Result(TypedDict):
  id: UUID
  index: int

class Error(TypedDict):
  id: UUID


class Request(TypedDict):
  request_id: Optional[UUID]
  inputs: List[Input]
  params: dict
  meta: Meta


class Response(TypedDict):
  model_id: UUID
  request_id: UUID

  results: Optional[List[Result]]
  errors: Optional[List[Error]]

  params: dict

  meta: Meta

class Feedback:
  type: str


def endpoint(f):
  def foo():
    return f()
  return f

class Server:
  input = []
  output = []

  def __init__(self, model, preprocess):
    self.model = model

  async def preprocess(self):
    pass

  async def process(self):
    pass

  async def postprocess(self):
    pass

  def __call__(self):
    pass

  async def socket(self):
    pass

class ClassificationServer(Server):
  pass

class OCRServer(Server):
  @endpoint
  async def detect(self):
    pass

import yann


yann.serve = lambda **kwargs: kwargs
yann.serve(
  checkpoint='gs://model/asfadf',
  model='resnet50',
  preprocess='imagenet',
  classes='imagenet',
  port=8080,
  workers=4,
  device=yann.default.device
)