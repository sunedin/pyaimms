# -*- coding: utf-8 -*-

# import python libs

import os
import pandas as pd
import win32com.client  # import win32com

class aimms():
    path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, path, project_name, v64bit=True, startup_mode=0, cleanup=True):
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

        AIMMS.DefaultElementValuePassMode = 2  # pass set names
        AIMMS.StartupMode = startup_mode  ##1  # mini startup mode

        start_up_message = '''
           STARTUP_NORMAL = 0 (default)
         STARTUP_MINIMIZED = 1
         STARTUP_MAXIMIZED = 2
         STARTUP_HIDDEN = 3
        '''
        print(start_up_message)
        AIMMS.ProjectOpen(projectName, 0)
        print(AIMMS)
        print('AIMMS start up successfully !')
        self.aimms_handler = AIMMS

    # define a series of pyaimms defination, for easily get and assign value between pyaimms and python
    # usder-defined function, make receive data from pyaimms easier: call pyaimms com func and retreive data into pandas
    # datafram
    def run(self, str_command):
        self.aimms_handler.Run(str_command)

    def aimms_get_indentifier(self, n, In=None):
        AimmsArray = list(self.aimms_handler.CreateArray(n))
        Aimms_df = pd.DataFrame(AimmsArray, index=In, columns=[n])
        return Aimms_df

    def aimms_get_indentifier_crosstab(self, n, In=None, Col=None):
        AimmsArray = list(self.aimms_handler.CreateArray(n))
        Aimms_df = pd.DataFrame(AimmsArray, index=In, columns=Col)
        print(Aimms_df.head(3))
        return Aimms_df

    def aimms_get_set(self, n):
        AimmsArray = list(self.aimms_handler.CreateElementArray(n))
        # print AimmsArray[02]
        return AimmsArray

    def aimms_assign_value(self, n, value):  # pyaimms.value = *, can not properly interpret in python; have to use .assignarray
        AimmsIdentifier = self.aimms_handler.GetIdentifier(n)
        AimmsArray = AimmsIdentifier.CreateArray()
        AimmsValue = self.aimms_handler.Value(n)
        bef = AimmsValue

        AimmsIdentifier.AssignArray((value,))
        AimmsValue = self.aimms_handler.Value(n)
        aft = AimmsValue

        print('%s is changed from %s to %s' % (n, bef, aft))

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
    AIMMS = aimms(path=r'c:\Users\wsun\OneDrive - University of Edinburgh\AIMMS G_converted - AP', project_name='OPF ANM.aimms')
    print('word')
