# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

"""Implementation of a common dataset object (session information)."""

class Session:
    """Class Session provides basic datatype and functions for storing and
    modifying session information.

    An instance of object Session could be assigned by the instruction

        sample1 = Session(subject_ID, session_ID)
    
    Many other attributers could be assigned by specific functions.

    Example:
    --------

    >>> from session import Session
    >>> sess1 = Session('S0001', 'S0001')
    >>> sess1.dicom_ID = '20110331_LiuJ_R1_Sxxxx_ZhangSan'

    Edited by Lijie Huang, 2011-10-31
    Last modified by LJ Huang, 2011-11-09

    """

    def __init__(self, subject_ID, session_ID):
        """Initalize an instance of SessInfo, set the subject_ID and the 
        session_ID.

        """
        self.subj_ID = subject_ID
        self.sess_ID = session_ID    
        self.dicom_ID = ''
        self.run_info = {}

    def setruninfo(self, exp_name, run_index, par_file_name):
        """Set every run's information based on the experiment type.
        
        Usage:
            sess1.setruninfo(exp_name, run_index, par_file_name)

        Example:
        --------

        >>> sess1.setruninfo('loc', '9', 'par1')

        """
        if exp_name in self.run_info:
            self.run_info[exp_name][run_index] = par_file_name
        else:
            self.run_info[exp_name] = {}
            self.run_info[exp_name][run_index] = par_file_name

    def delruninfo(self, exp_name, run_index):
        """Delete certain run according to the experiment name and the run 
        index.

        Usage:
            sess1.delruninfo(exp_name, run_index)

        Example:
        --------

        >>> sess1.delRunInfo('loc', '9')

        """
        if exp_name in self.run_info:
            if run_index in self.run_info[exp_name]:
                self.run_info[exp_name].pop(run_index)
            else:
                print 'run ' + run_index + ' does not be recorded.\n'
        else:
            print 'Experiment name you specified does not exist.\n'

    def getruninfo(self, exp_name, run_index=[]):
        """Get specific run's information including run index and 
        corresponding par file name, which storing in two distinct list.

        Usage:
            [run_index_list, par_file_list] = sess1.getruninfo(exp_name,
                                                               run_index)

        Example:
        --------

        >>> sess1 = SessInfo('S0001', 'S0001')
          ......
          ......
        >>> [runIndexList, parFileList] = sess1.getruninfo('loc', ['9', '10'])

        Notes:If enter getruninfo('loc'), the function will return all runs'
        information belonging to the experiment 'loc'.
            
        """
        if exp_name in self.run_info:
            run_index_list = []
            par_file_list = []
            if len(run_index) == 0:
                run_index = self.run_info[exp_name].keys()
            for item in run_index:
                if item in self.run_info[exp_name]:
                    run_index_list.append(item)
                    par_file_list.append(self.run_info[exp_name][item])
                else:
                    print 'run ' + item + ' does not in ' + \
                          exp_name + ' list.\n'
            return run_index_list, par_file_list
        else:
            print 'Experiment name you specified does not exist.\n'
