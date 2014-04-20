# -*- coding: utf-8 -*-
def to_unicode(sem_str_raw):
    if isinstance( sem_str_raw, str):
        sem_str = sem_str_raw.decode('utf-8') 
    elif isinstance( sem_str_raw, unicode):
        sem_str = sem_str_raw
    else:
        assert 0
    return sem_str
def to_utf8_str(sem_str_raw):
    if isinstance( sem_str_raw, str):
        sem_str = sem_str_raw
    elif isinstance( sem_str_raw, unicode):
        sem_str = sem_str_raw.encode('utf-8') 
    else:
        assert 0
    return sem_str
