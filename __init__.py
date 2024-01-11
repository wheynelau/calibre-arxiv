#!/usr/bin/python
# -*- coding: utf-8 -*-
# License: GPLv3 Copyright: 2024, wheynelau
store_version = 8

__license__ = 'GPL v3'
__copyright__ = '2024, wheynelau <waynelau15045@gmail.com>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class Arxiv(StoreBase):
    name = "Arxiv"
    version = (0, 1, 0)
    type_ = _("Store")
    description = "Searches for arxiv.org papers"
    actual_plugin = 'calibre_plugins.arxiv.main:ArxivStorePlugin'
    author = "wheynelau"
    drm_free_only = True
    formats = ["PDF"]









