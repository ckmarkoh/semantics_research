#-*- coding:utf-8 -*-

#S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:台大))|Head:VC31:發表|theme:NP(Head:Nad:演說))#

#S(agent:NP(Head:Nba:柯文哲)|time:Ndabd:昨天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:大學))|Head:VC31:發表|theme:NP(Head:Nad:演說))#


#S(time:NP(property:Nbc:柯|Head:Nad:文哲)|Head:V_12:是|range:NP(Head:Nab:醫生))#,(COMMACATEGORY)
#S(time:NP(property:Nbc:柯|Head:Nad:文哲)|time:Dc:不|Head:V_12:是|range:NP(Head:Nab:醫生))#,(COMMACATEGORY)

#S(time:NP(property:Nbc:柯|Head:Nad:文哲)|time:Dc:不|Head:V_12:是|range:NP(Head:Nab:醫護人員))#,(COMMACATEGORY)
#S(agent:NP(property:Nb:柯文哲|Head:Nab:醫師)|time:Ndabd:昨天|location:PP(Head:P21:在|DUMMY:NP(Head:Nca:台大))|Head:VC31:發表|theme:NP(Head:Nad:演講))
#柯文哲昨天在台大
#NP(property:NP(property:Nb:柯文哲|Head:Ndabd:昨天)|Head:PP(Head:P21:在|DUMMY:NP(DUMMY1:Nca:台大)))
#柯文哲昨天在演講
#NP(Head:NP(property:Nbc:柯|property:Nad:文哲|Head:Ndabd:昨天)|apposition:PP(Head:P21:在|DUMMY:NP(Head:Nad:演講)))
#柯文哲昨天去台大演講
#S(theme:NP(Head:Nb:柯文哲)|time:Ndabd:昨天|Head:VC1:去|goal:NP(property:Nca:台大|Head:Nad:演講))
#S(agent:Nba(DUMMY1:Nb:柯文哲|Head:Caa:和|DUMMY2:Nb:連勝文)|time:Dd:將|Head:VC2:參選|goal:NP(Head:Nab:台北市長))
#S(agent:NP(Head:Nba:小明)|location:PP(Head:P21:在|DUMMY:NP(Head:Ncb:家))|Head:VC2:打|goal:NP(Head:Nab:電腦))
