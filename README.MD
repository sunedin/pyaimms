This package provide a python **short-cut** to the most usefully AIMMS com functions.

Full list of com-funcion can be acccess through AIMMS.aimms_com_handler. 

The Aimms COM object defines four COM interfaces:
- Aimms.Project,
- Aimms.Identifier,
- Aimms.Setl
- Aimms.Procedure

Full document can be access at [aimms_com_document](doc/AIMMS_com.pdf)

*todo*: set.AddElement, set.RanameElement can be added into the shortcuts

Note:
============
1. run(*arg) can handle procedure with argument
>for example, run('MainExecution', [])

2. run(*arg) can ONLY access the procedures defined by user in the project BUT not the aimms predefined builtin procedures

> for example: run('SaveCaseFiile', 'results.data') will fail unless the builtin procedure 'SaveCaseFiile'is wrapped in a user-defined procedures in the project


