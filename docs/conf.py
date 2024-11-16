import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# 导入版本号
from quantduck import __version__

project = 'Quantduck'
copyright = '2024'
author = 'Quantduck Team'

# 添加版本信息
version = __version__
release = __version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# 在现有配置后添加
html_theme_options = {
    'display_version': True,
    'style_external_links': True,
    'navigation_depth': 4,
}

# 支持 markdown 文件
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# 添加自定义域名支持（如果有的话）
# html_baseurl = 'https://your-domain.com' 