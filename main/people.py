#这里写所有角色最基本的类，这个类需要有这几个参数1.这个角色的样子（会放在文件夹里，可以直接读取）2.这个角色的HP3.这个角色的SP。4.这个角色相遇时说的话
#一些特殊角色，比如主角与敌人，需要有特殊的类，可以用类继承普通人的类再扩充，主角有自己技能，有自己的装备，有自己的动图，敌人有动图和自己的技能
class common_npc:
    def __init__(self,picture:int,HP:int,SP:int,role_text:str):
        self.picture=picture
        self.HP=HP
        self.SP=SP
        self.role_text=role_text 
    def say(self):
        print(self.role_text)
npc1=common_npc(1,1,1,'你好')
print(npc1.role_text)