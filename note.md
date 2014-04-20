
幫助 他們

```
>>> e1=lgp.parse(r'\Z\u.Z(\v\e.幫助(u,v,e))' )
>>> e2=lgp.parse(r'\P.P(他們)' ) 
>>> e3=lgp.parse("%s(%s)"%(e1.__str__(),e2.__str__()))
>>> print e3
(\Z u.Z(\v e.幫助(u,v,e)))(\P.P(他們))
>>> print e3.simplify()
\u e.幫助(u,他們,e)
```

```
e1=lgp.parse(r'\Z\u.Z(\v\e.幫助(u,v,e))' )
e2=lgp.parse(r'\P.P(陳小姐)' ) 
e3=lgp.parse(r'\P.P(我)' ) 
e4=lgp.parse("%s(%s)"%(e1.__str__(),e2.__str__()))
e5=lgp.parse("%s(%s)"%(e3.__str__(),e4.__str__()))
print e5.simplify()
```

