# -*- coding: utf-8 -*-

# import python libs

import os
import pandas as pd
import numpy as np
import win32com.client  # import win32com


class aimms():
    path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, path, project_name, v64bit=True, startup_mode=0, cleanup=True, ElementValuePassMode=2):
        if cleanup:
            os.system("taskkill /im AimmsCOM.exe /f")

        # AIMMS = win32com.client.Dispatch("Aimms.Project.4.2")  # or aimms64.project.4.2 # initialise pyaimms com
        # AIMMS = win32com.client.Dispatch("Aimms.Project")  # or aimms64.project.4.2 # initialise pyaimms com #todo bring it back
        # AIMMS = win32com.client.Dispatch("AimmsSelector.Selector")  # or aimms64.project.4.2 # initialise pyaimms com
        # AIMMS = win32com.client.Dispatch("aimms64.project.4.2")  # or aimms64.project.4.2 # initialise pyaimms com

        if v64bit:
            AIMMS_Driver = win32com.client.Dispatch("AimmsSelector.Selector64")
        else:
            AIMMS_Driver = win32com.client.Dispatch("AimmsSelector.Selector32")

        Aimms_project_folder = path
        Aimms_project_obj = project_name
        projectName = os.path.join(Aimms_project_folder, Aimms_project_obj)

        AIMMS = AIMMS_Driver.GetAimmsProject(projectName)

        AIMMS.DefaultElementValuePassMode = ElementValuePassMode  # pass set names
        AIMMS.StartupMode = startup_mode  ##1  # mini startup mode

        start_up_message = '''
           STARTUP_NORMAL = 0 (default)
         STARTUP_MINIMIZED = 1
         STARTUP_MAXIMIZED = 2
         STARTUP_HIDDEN = 3
           
        '''
        print(start_up_message)
        print('Project open with startup_mode {} and faultElementValuePassMode {}'.format(startup_mode, ElementValuePassMode))
        AIMMS.ProjectOpen(projectName, 0)
        print(AIMMS)
        print('AIMMS start up successfully !')
        self.aimms_com_handler = AIMMS

    # define a series of pyaimms defination, for easily get and assign value between pyaimms and python
    # usder-defined function, make receive data from pyaimms easier: call pyaimms com func and retreive data into pandas
    # datafram
    def run(self, *args):
        value_ = self.aimms_com_handler.Run(*args)
        if value_ != 0:
            print('!!! procedure {} NOT run properly !!'.format(args[0]))

    def aimms_get_indentifier(self, n, In=None):

        if isinstance(In, str):
            In = self.aimms_get_set(In)

        AimmsArray = list(self.aimms_com_handler.CreateArray(n))
        Aimms_df = pd.DataFrame(AimmsArray, index=In, columns=[n])
        return Aimms_df

    def aimms_get_indentifier_crosstab(self, n, In=None, Col=None):

        if isinstance(In, str):
            In = self.aimms_get_set(In)
        if isinstance(Col, str):
            Col = self.aimms_get_set(Col)

        AimmsArray = list(self.aimms_com_handler.CreateArray(n))
        Aimms_df = pd.DataFrame(AimmsArray, index=In, columns=Col).applymap(lambda x: x if np.isscalar(x) else x[0])  # tricky, not cleatly explained in aimms manual
        print(Aimms_df.head(3))
        return Aimms_df

    def aimms_get_set(self, n):
        AimmsArray = list(self.aimms_com_handler.CreateElementArray(n))
        # print AimmsArray[02]
        return AimmsArray

    def aimms_get_scalar(self, n):
        AimmsScalar = self.aimms_com_handler.Value(n)
        # print AimmsArray[02]
        return AimmsScalar

    def aimms_assign_set(self, n, value):
        self.aimms_com_handler.GetSet(n).AssignElementArray(value)
        print('set {} is update to {}'.format(n, value))

    def aimms_assign_value(self, n, value):  # pyaimms.value = *, can not properly interpret in python; have to use .assignarray

        if np.isscalar(value):
            AimmsValue = self.aimms_com_handler.Value(n)
            bef = AimmsValue

            self.aimms_com_handler.GetIdentifier(n).AssignArray((value,))
            AimmsValue = self.aimms_com_handler.Value(n)
            aft = AimmsValue

            print('%s is changed from %s to %s' % (n, bef, aft))

        else:
            self.aimms_com_handler.GetIdentifier(n).AssignArray(value)
            print('array(matrix) of %s is updated' % (n))

    def aimms_get_solveinfo(self, opt_instance):

        SolvingTime = self.aimms_com_handler.Value(str(opt_instance) + '.SolutionTime')  # from ms to min
        ProgStat = self.aimms_com_handler.CreateElementArray('AllSolutionStates')[
            int(self.aimms_com_handler.Value(str(opt_instance) + '.ProgramStatus')) - 2]  # tricky, not cleatly explained in aimms manual
        SolvStat = self.aimms_com_handler.CreateElementArray('AllSolutionStates')[int(self.aimms_com_handler.Value(str(opt_instance) + '.SolverStatus')) - 2]
        BestLPSolution = self.aimms_com_handler.Value(str(opt_instance) + '.Objective')

        print('OPT stop in {} min with obj value of {}'.format(SolvingTime, BestLPSolution))
        print('ProgStat is {} with SolvStat is {}'.format(ProgStat, SolvStat))

        solve_info = [SolvingTime, ProgStat, SolvStat, BestLPSolution]
        return solve_info

    def aimms_get_OPTinfo(self, opt_instance):

        NumberOfConstraints = self.aimms_com_handler.Value(str(opt_instance) + '.NumberOfConstraints')
        NumberOfVariables = self.aimms_com_handler.Value(str(opt_instance) + '.NumberOfVariables')
        print('OPT have {} Constraints and {} Variables'.format(NumberOfConstraints, NumberOfVariables))
        opt_info = [NumberOfConstraints, NumberOfVariables]
        return opt_info

    def aimms_get_suffix(self, opt_instance, suffix_str):
        suffix_str_value = self.aimms_com_handler.Value(str(opt_instance) + '.{}'.format(suffix_str))
        return suffix_str_value

    # from AIMMS_def import aimms_get_indentifier, aimms_get_indentifier_crosstab, aimms_get_set, aimms_assign_value
    # repackage a serires of python funcs, for easily clean zero and subplot
    def drop_zero_row(df):  # n is a dataframe
        valid = df[(df.T != 0).any()]
        # valid = df.loc[(df.T !=0).any()] #filter zero row
        return valid

    def drop_zero_col(df):  # n is a dataframe
        valid = df[df.columns[(df != 0).any()]]
        return valid


if __name__ == '__main__':
    pass
