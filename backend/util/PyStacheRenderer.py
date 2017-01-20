#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

from pystache.loader import Loader
from pystache.renderer import Renderer

class PartialsLoader(object):

	def __init__(self):
		self.loader = Loader(extension="html", search_dirs=["html/partials"])

	def get(self, template_name):
		return self.loader.load_name(template_name)

class PyStacheRenderer(Renderer):

	file_extension = "html"
	search_dirs = ["html"]
	partials = PartialsLoader()
	file_encoding = "utf-8"
	string_encoding = "utf-8"

	def __init__(self):
		super(PyStacheRenderer, self).__init__(
			file_extension=PyStacheRenderer.file_extension,
			search_dirs=PyStacheRenderer.search_dirs,
			partials=PyStacheRenderer.partials,
			file_encoding=PyStacheRenderer.file_encoding,
			string_encoding=PyStacheRenderer.string_encoding
		)

if __name__ == "__main__":
	p = PyStacheRenderer()