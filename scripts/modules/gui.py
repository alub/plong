"""
GUI functions for the Python scripts to show progress.
"""

import subprocess
import sys


def _toggle_console():
    """
    Toggles the display of the Windows console, if applicable
    """

    if sys.platform.startswith("win"):
        bpy.ops.wm.console_toggle()


class ProgressBar:
    """
    This class allows a running script to show a progress bar during its execution.
    """

    def __init__(self, title, description, indeterminate=False):
        self.description = description

        try:
            params = ["zenity", "--progress", "--auto-close", "--no-cancel",
                "--title=%s" % title, "--text=%s" % description]
            if indeterminate:
                params.append('--pulsate')

            self.proc = subprocess.Popen(params, stdin=subprocess.PIPE)
        except OSError:
            self.proc = None

        if self.proc and indeterminate:
            try:
                self.proc.stdin.write(("0\n").encode('ascii'))
            except IOError:
                pass
        elif not self.proc:
            _toggle_console()
            print("%s: 0%%" % self.description, end='')
            sys.stdout.flush()

    def progress(self, percentage):
        """
        Reports progress to the user. percentage must be an integer
        between 0 and 100.
        """

        if self.proc:
            try:
                self.proc.stdin.write(("%d\n" % percentage).encode('ascii'))
            except IOError:
                pass
        else:
            print("\r%s: 0%%" % self.description, end='')
            sys.stdout.flush()

    def close(self):
        """
        Closes the progress dialog, if any
        """

        if self.proc:
            self.proc.terminate()
        else:
            print("")
            _toggle_console()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class ProgressText:
    """
    This class allows a running script to output text during its execution.
    """

    def __init__(self, title):
        try:
            self.proc = subprocess.Popen(["zenity", "--text-info", "--width=600",
                "--height=400", "--title=%s" % title], stdin=subprocess.PIPE)
        except OSError:
            self.proc = None

        if not self.proc:
            print("%s:" % title)

    def output(self, text):
        """
        Reports progress to the user.
        """

        if self.proc:
            try:
                self.proc.stdin.write(text.encode('utf-8'))
            except IOError:
                pass
        else:
            sys.stdout.write(text)
            sys.stdout.flush()

    def close(self):
        """
        Closes the progress dialog, if any
        """

        if self.proc:
            self.proc.terminate()
        else:
            print("Done.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
