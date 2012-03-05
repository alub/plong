#!/usr/bin/env python3

"""
This is a wrapper for Sphinx, as Sphinx needs to be executed inside Blender,
or else it can not access the `bpy` module.
"""

if __name__ == '__main__':
    # Allow for Blender to find Sphinx
    import sys
    sys.path.insert(0, '/usr/lib/python3.2/site-packages')
    sys.path.append('/usr/local/Cellar/python3/3.2.2/lib/python3.2/site-packages/Sphinx-1.1.2-py3.2.egg')
    sys.path.append('/usr/local/Cellar/python3/3.2.2/lib/python3.2/site-packages/docutils-0.8.1-py3.2.egg')
    sys.path.append('/usr/local/Cellar/python3/3.2.2/lib/python3.2/site-packages/Jinja2-2.6-py3.2.egg')
    sys.path.append('/usr/local/Cellar/python3/3.2.2/lib/python3.2/site-packages/Pygments-1.4-py3.2.egg')
    import sphinx

    args = [__file__] + sys.argv[sys.argv.index('--') + 1:]

    sphinx.main(argv=args)
