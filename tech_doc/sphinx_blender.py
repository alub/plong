#!/usr/bin/env python3

"""
This is a wrapper for Sphinx, as Sphinx needs to be executed inside Blender,
or else it can not access the `bpy` module.
"""

if __name__ == '__main__':
    # Allow for Blender to find Sphinx
    import sys
    sys.path.insert(0, '/usr/lib/python3.2/site-packages')
    import sphinx

    args = [__file__] + sys.argv[sys.argv.index('--') + 1:]

    sphinx.main(argv=args)
