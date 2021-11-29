# -*- coding: utf-8 -*-

# import python libs

import glob
import os
import pandas as pd
from pyaimms.funcs import aimms

pd.set_option('expand_frame_repr', False)
pd.set_option('precision', 3)

if __name__ == '__main__':
    Aimms_project_folder = os.path.dirname(os.path.realpath(__file__))
    AIMMS = aimms(path=Aimms_project_folder, project_name='RunAIMMS.aimms')
    print(AIMMS)
    print('AIMMS start up')

    depots = ["d-1", "d-2", "d-7"]
    AIMMS.aimms_assign_set("Depots", depots)

    customers = ["c-1", "c-2", "c-3", "c-4", "c-5", "c-6", "c-7", "c-7", "c-8", "c-9", "c-10"]
    AIMMS.aimms_assign_set("Customers", customers)

    supply = [10.0, 15.0, 20.0]
    demand = [3.0, 6.0, 3.0, 3.5, 5.5, 5.0, 6.0, 1.5, 7.0, 4.5]
    unitTransportCost = [[1.0, 0.7, 0.3, 0.8, 1.2, 0.3, 1.1, 0.9, 1.0, 0.5],
                         [0.7, 0.9, 1.3, 0.9, 0.9, 1.3, 1.2, 0.5, 0.7, 1.5],
                         [1.2, 0.5, 0.9, 1.8, 1.1, 0.7, 0.5, 1.4, 0.5, 1.4]]

    AIMMS.aimms_assign_value("Supply", supply)
    AIMMS.aimms_assign_value("Demand", demand)
    AIMMS.aimms_assign_value("UnitTransportCost", unitTransportCost)

    AIMMS.aimms_get_indentifier("Supply")
    AIMMS.aimms_get_indentifier("Demand")
    AIMMS.aimms_get_indentifier_crosstab("UnitTransportCost", Col="Customers", In='Depots')

    AIMMS.run("MainExecution")
    AIMMS.aimms_get_solveinfo('TransportModel')
    AIMMS.aimms_get_OPTinfo('TransportModel')

    AIMMS.aimms_get_suffix('TransportModel', 'GenTime')
    AIMMS.aimms_get_suffix('TransportModel', 'Iterations')

    status = AIMMS.aimms_get_scalar("TransportModelStatus")
    cost = AIMMS.aimms_get_scalar("TotalCost")
