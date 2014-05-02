# -*-

_CWN_PATH = '../data/cwn_dirty.sqlite'
class CwnInterFace(SQLiteInterface):
    def __init__(self):
        super(CwnInterFace,self).__init__(_CWN_PATH)
            
    def get_lemma(self,lemma): 
        return self.select('cwn_lemma'
                           ,where=' lemma_type="%s" ORDER BY lemma_sno ASC'%(lemma))
    def get_sense(self,lemma_id):
        pass
