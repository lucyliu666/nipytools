# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import os
import string


def par2ev(par_file):
    """Convert par file to ev files."""
    loc_dir = os.path.dirname(par_file)
    with open(par_file, 'r') as f:
        evs = dict()
        for line in f:
            if not line:
                pass
            line = line.split()
            if line[1] > '0' and line[1] not in evs:
                if len(line) > 4:
                    line[4] = string.join(line[4:], '_')
                    evs.update({line[1]:open(
                            os.path.join(loc_dir, line[4]+'.ev'), 'w')})
                else:
                    evs.update({line[1]:open(
                            os.path.join(loc_dir, line[1]+'.ev'), 'w')})
            if line[1] > '0':
                evs[line[1]].write('{0:8}\t{1:6}\t{2:d}\n'.
                            format(line[0], line[2], int(float(line[3]))))
        for key, value in evs.items():
            value.close()

