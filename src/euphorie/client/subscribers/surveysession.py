# coding=utf-8
def modified(obj, evt):
    ''' Invoke the touch method of this object that should update the columns:

    - modified
    - last_modifier
    '''
    obj.touch()
