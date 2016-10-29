#!/usr/bin/env python3
"""
# Modified by mhminai to use Preview
open pdf file produced by latexmk in Preview.app
"""

import os
import subprocess
import sys
sys.path.append(os.path.join(os.environ['PANZER_SHARED'], 'python'))
import panzertools


def open_pdf(filepath):
    fullpath = os.path.abspath(filepath)
    target = panzertools.FileInfo(filepath)
    command = ['open']
    command.extend([target.filename()])
    panzertools.log('INFO', 'running "%s"' % ' '.join(command))
    try:
        p = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout_bytes, stderr_bytes = p.communicate()
        if stdout_bytes:
            stdout = stdout_bytes.decode(panzertools.ENCODING, errors='ignore')
            for line in stdout.splitlines():
                panzertools.log('INFO', line)
        if stderr_bytes:
            stderr = stderr_bytes.decode(panzertools.ENCODING, errors='ignore')
            for line in stderr.splitlines():
                panzertools.log('INFO', line)
    except OSError as error:
        panzertools.log('ERROR', error)


def main():
    """docstring for main"""
    OPTIONS = panzertools.read_options()
    filepath = OPTIONS['pandoc']['output']
    if filepath == '-':
        panzertools.log('INFO', 'not run')
        return
    target = panzertools.FileInfo(filepath)
    target.set_extension('.pdf')
    pdfpath = target.fullpath()
    if os.path.exists(pdfpath):
        open_pdf(pdfpath)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
