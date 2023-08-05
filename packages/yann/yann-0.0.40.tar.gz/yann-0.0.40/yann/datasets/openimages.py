import yann

class files:
  class_names = ''


class OpenImages:
  """



  https://storage.googleapis.com/openimages/web/download.html
  """




  def __init__(self, root=None, classes=None, download=True):
    self.images = []


  def image_url(self, id):
    pass

  def image_path(self, id):
    pass

  def download(self):
    for id in self.images:
      url = self.image_url(id)
      yann.download(url)


class OpenImagesExtended(OpenImages):
  """
  https://storage.googleapis.com/openimages/web/extended.html
  """