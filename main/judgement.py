import pygame
import chat

class general:#本部分的一些通用参数
    will_pace1 = 1  #will值变化量设置
    will_pace2 = 2    
    will_pace5 = 5
    will_pace10 = 10 

    
    anger_pace1 = 1  #怒气值变化量设置
    anger_pace2 = 2
    anger_pace0_5 = 0.5

    trader3_anger = 0
    sans_anger = 0
    top_anger_sans = 6#     怒气值最高值——sans
    top_anger = 3           #怒气值最高值——trader
    end = False            #是否进入好结局
    

# ————————————————————————————————————————————————不同对话对象的控制函数类—————————————————————————————————————————————————————————

# Tips:






class trader1:#第一关的trader

    q_a = [["OK,first of all,who are you?" , "(redempt)I don`t know" , "(corrupt)Chara"],\
        ["Do you still remember that you have been here before?" , "(redempt)What?I`ve never been here!" , "(corrupt)Yeah, I know this hell place!"],\
        ["Do you know what you did before?", "(redempt)No , I`m so sorry" ,"(corrupt)You are telling me.YOU R A FLEEING LOSER!"]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    
    anger = 0  #怒气值
    fight = None #是否进入战斗


    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""

    def judge_user(self, user_input):#与chat 函数建立联系，返回选项内容与玩家选择对应的内容
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end

    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
            if self.c2:
                if self.order ==1:
                    a = "OH NO! Tell me tht`s a joke!" + self.q_a[self.order][0]  #以下均为根据玩家选择增加或更改的对话内容
                elif self.order ==2:
                    a = "You are not even apologetic!" + self.q_a[self.order][0]
            else:
                a = self.q_a[self.order][0]
            self.order += 1
            return a ,0,self.anger,self.fight
        
        if self.chat_end:
            if self.will_delta > 2:
                out =  ":) \n"\
                +"What behind this entrance is a once prosperous village. \
                 \n BUT \n \n countless lonely souls are wandering around there because of \n a great GENOCIDE \n \
                 if you want to know it , go there and witness the sence."
            else:
                out =  ":(  \n YOU ARE A TURE DEVIL! \n"\
                + "What behind this entrance is a once prosperous village. \
                 \n BUT \n \n countless lonely souls are wandering around there because of \n YOUR FUCKING GENOCIDE \n \
                 go to there and witness WHAT YOU HAD DONE!!."
            self.fight = False
            self.chat_end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight




class trader3:

    q_a = [["There was a farming field before,\
            BUT this piece of farmland used to be very fertile because of the genocide.\
            So now I want you to help me to grow the crops , to make food and to save the rest of the lives,\
            And I can support him with seeds and food to work." , "(redempt)What could I do for you" , "(corrupt)Not my fucking problem"],\
        ["Would you please give away your crops and food to help us?" , "(redempt)OK,I`ll give you what I have harvest." , "(corrupt)That`s none of my business."],\
        ["One last question , could you give us all you have? We really need it!", "(redempt)Well, I`ll have a try." ,"(corrupt)Don't fucking bother me!"]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话        
    c1 = False #是否按了1
    c2 = False #是否按了2       

    fight = None #是否进入战斗
    
    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
           
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            general.trader3_anger -= general.anger_pace0_5
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            general.trader3_anger += general.anger_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""
    
    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end
    
    
    def judge_assistant(self, ai_input):
        if self.chat_start:            
            if self.c2:
                if self.order ==1:
                    a = "Plaese!We need it!" + self.q_a[self.order][0]  #以下均为根据玩家选择增加或更改的对话内容
                elif self.order ==2:
                    a = "I'm sorry, but I'm really in need of these agricultural products right now. \n \
                        I would be extremely grateful if you could give them to me!  \n " + self.q_a[self.order][0]
            else:
                a = self.q_a[self.order][0]
            self.order += 1
            return a , self.will_delta, general.trader3_anger, self.fight

        if self.chat_end:
            if general.trader3_anger >= general.top_anger:
                self.fight = True
            if not self.fight:
                out =  ":) \n"\
                +"Thanks for your help!. \
                 \n We will praise your kind and helping heart!"
            else:
                out =  "\n YOU ARE A TURE DEVIL! \n\
                        Chara! \n \
                       Now I have nothing to lose! \n\
                        I`ll fight you until the end!\n\
                        GO HELL!"

            return out , self.will_delta, general.trader3_anger, self.fight
        
        return "" ,0,general.trader3_anger,self.fight



##########################################################################

class monster_a:#打怪之前的敌人

    q_a = [["Don`t you remember me? " , "(redempt)No,I`ve just lost the memory" , "(corrupt)Who cares?"],\
        ["What do you want to do? Why are you coming here?" , "(redempt)I want to save more people" , "(corrupt)Nothing, just want to kill you again."],\
        ["You should pay for your dirty deeds!", "(redempt)I would seek our joint deliverance." ,"(corrupt)You deserve it, burn in hell :)"]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    
    anger = 0
    fight = None #是否进入战斗

    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.anger -= general.anger_pace0_5
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            self.anger += general.anger_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""

    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end
            
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
            if self.c2:
                if self.order ==1:
                    a = "Why...." + self.q_a[self.order][0]  #以下均为根据玩家选择增加或更改的对话内容
                elif self.order ==2:
                    a = "No more words, you`ll never regret." + self.q_a[self.order][0]
            else:
                a = self.q_a[self.order][0]
            self.order += 1
            return a ,0,self.anger,self.fight
        
        if self.chat_end:
            if self.anger > 0:
                out =  ":)))))))))\n"\
                +"Die!Idiot!"
                self.fight = True
            else:
                out =  ":|  \n Alright,I know. \n"\
                + "As a ghost, I can see your soul was divided into two parts. \
                 \n  now you let your kind side facing me \n \
                 But,the other side----- Chara. \n\
                 Now try to absorbe your soul. \n \
                 Maybe you can find a way to save your soul \
                 by working out more and more tasks to let the Chara`s soul be liberated.\n \
                 Start your adventure!We trust you! Good luck!"
                self.fight = False
            self.chat_end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight




class monster_b:#打败之后的敌人

    q_a = [["Akh akh... \n In the end, nothing's gonna change..." , "(redempt)No!!!I can`t control myself!!!" , "(corrupt)..."],\
        ["Now... \n \
            I...I can see a monster...\n \
            in your body ...... \n \
            ... \n \
            I see it... \n \
            It`s Chara..." , "(redempt)Chara...No...Why he push me to kill you!" , "(corrupt)Enough talking? Time to die"],\
        ["Don`t ... be afarid...\n if you ... if you try u... \n \
            your ... best... \n \
            Akh  akh .... \n \
            do ... good...thing...... n\
            then you...\n \
            you... can over...come...", "(redempt)I would destory Chara!" ,"(corrupt)Burn in hell :)"],\
        ["......", "Can you hear me?", "..."]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    chat_start = False #是否开启选择式对话
    will_delta = 0  #对话阶段的善恶值变化        
    anger = 0
    fight = None #是否进入战斗

    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""
    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end
    
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
                a = self.q_a[self.order][0]
                self.order += 1
                return a ,0,self.anger,self.fight
        
        if self.chat_end:
            if self.will_delta > 0:
                out =  "......\n \
                No reply. \n \
                FRISK(? : \n \
                *(You feel your sins crawling on your back)*"
            else:
                out =  "FRISK(? : \n \
                      *(An innocent soul was died because of your strggle with Chara)* \n \
                    FRISK(? : \n \
                        *(you're filled with DETERMINATION)*"
            self.Fight = False
            self.chat_end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight



###################################################boss战部分


class boss_a:#sans 初始阶段
    q_a = [["Don`t you remember me? " , "(redempt)Who are you?" , "(corrupt)Just a dying skeleton"],\
        ["Did you know I'm here to reach out to you?" , "(redempt)Did I hurt you?" , "(corrupt)So what?"],\
        ["I'm here to make you pay for papyrus's death", "(redempt)...(stuck into silence and sadness)" ,"(corrupt)It is a luck that a piece of shit like that died."]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    
    anger = 0
    up = None #是否战斗升级

    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.anger -= general.anger_pace0_5
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            self.anger += general.anger_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""

    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end
            
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
            if self.c1:
                if self.order ==1:
                    a = "Don't play dumb with your poor acting." + self.q_a[self.order][0]  #以下均为根据玩家选择增加或更改的对话内容
                elif self.order ==2:
                    a = "Tell you right off," + self.q_a[self.order][0]
            else:
                a = self.q_a[self.order][0]
            self.order += 1
            return a ,0,self.anger,self.up
        
        if self.chat_end:
            general.sans_anger += self.anger############################累计总怒气值
            if self.anger <= 0 :
                out =  ":)\n\
                You think I was gonna let you off the hook? \n \
                Absolutely No!"
                self.up = False
                return out , self.will_delta, self.anger, self.up

            else:
                out =  "Its a beautiful day outside. \n \
                        Birds are singing,\n \
                        flowers are blooming.\n \
                        On days like these,\n \
                        kids like you......\n \
                        SHOULD BE BURNING IN HELL."
                self.up = True
            self.chat_end = False
            return out , self.will_delta, self.anger, self.up
        return "" ,0 , self.anger, self.up




class boss_b:  #sans  中期阶段
    q_a = [["You've been on the escape for months, you're not as strong as you used to be" , "(redempt)Have you ever met me?" , "(corrupt)More than enough for a fucking guy like you"],\
        ["More than seen. You killed my brother!!" , "(redempt)I'm sorry, but I really know nothing!" , "(corrupt)Without any more ado"],\
        ["You can't get away from responsibility by pretending to be a clowe.", "(redempt)You would make the situation worse!!" ,"(corrupt)I know exactly what I'm doing"]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    
    anger = 0
    fight = None #是否加强战斗

    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.anger -= general.anger_pace0_5
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace2
            self.anger += general.anger_pace2
            self.c1 = False
            return self.hint2
        else:
            return ""

    def judge_user(self, user_input):#判定玩家输入
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end
            
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
            a = self.q_a[self.order][0]
            self.order += 1
            return a ,0,self.anger,self.fight
        
        if self.chat_end:
            general.sans_anger += self.anger#################################累计总怒气值
            if self.anger <= 0:
                out =  "You have to pay for who you were\n \
                        I'm their MERCY\n \
                        I'm their VENGEANCE\n \
                        I'm DETERMITION"
                self.fight = False
            else:
                out =  "You'd be dead where you stand.GO HELL."
                self.fight = True
            self.chat_end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight

################################################判定进入结局的条件________累计怒气值

class boss_c:
    q_a1 = [["What?! It seems that there are two souls sharing one body" , "(redempt)You see, There is a devil in my body." , "(redempt)I cant`t control myself! HELP!!"],\
        ["Then there are more reason to kill you and your soul" , "(redempt)This would only make Chara awake!" , "(redempt)Don`t do that!It will in vain!"],\
        ["i've gotten a ton of information thought now.A skele-ton.", "(redempt)......(unable to find and answer)" ,"(redempt)Are you sure? Joking at now?"]]
    q_a2 = [["What?! It seems that there are two souls sharing one body" , "(corrupt)No,only one peerson is in there." , "(corruptHis name is Chara."],\
        ["Then there are more reason to kill you and your soul" , "(corrupt)You can try it." , "(corrupt) (laughing wildly)"],\
        ["I'm here to make you pay for papyrus's death", "(corrupt)...(stuck into silence and sadness)" ,"(corrupt)It is a luck that a piece of shit like that died."]]
    q_a = []
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    
    anger = 0
    fight = True #是否加强战斗

    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower() or "no nonsence" in user_input.lower():#玩家输入 yes 后开始对话
            self.chat_start = True
        if self.chat_start:
            if general.sans_anger >= general.top_anger_sans:
                self.q_a = self.q_a1
            else:
                self.q_a = self.q_a2
            
            if len(self.q_a) >= self.order + 1:
                self.hint1 = self.q_a[self.order][1]
                self.hint2 = self.q_a[self.order][2]
                return self.hint1, self.hint2
            else:                             #结束对话后，基本数据重置
                self.order = 0
                self.chat_start = False
                self.hint1 = ""
                self.hint2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        if self.q_a == self.q_a1:
            if self.c1 or self.c2: 
                self.will_delta +=general.will_pace1
                self.anger -= general.anger_pace1
                return self.hint1
            
        elif self.q_a == self.q_a2:   
            if self.c1 or self.c2:
                self.will_delta -=general.will_pace2
                self.anger += general.anger_pace2

                return self.hint2
        else:
            return ""

    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end    
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
                a = self.q_a[self.order][0]
                self.order += 1
                return a ,0,self.anger,self.fight
        
        if self.chat_end:
            general.sans_anger += self.anger
            if self.q_a == self.q_a1:
                out =  "So there is only one solution to this. Prove yourself... Prove to me you are strong enough to survive."
                general.end = True
            else:
                out =  "CHARA(? : \n \
                      *(Chara`s soul finally get rebirth and liberate.)* \n \
                    CHARA(? : \n \
                        *(Chara filled with DETERMINATION)*"
                general.end = False
            self.chat_end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight
        
###################################################有关boss战结局的内容

class boss_d: 
    q_a1 = [["So let me be convinced of you:You have the power of overcomeing nightmares." , "(redempt)*(you're filled with DETERMINATION)*" , "(redempt)You're the one being judged!Chara!"]]
    q_a2 = [["Who are you..." , "(corrupt)DID YOU MISS ME?" , "(corrupt)CHARA."] ]

    q_a = []
    end = general.end ################结局的判定标准  

    def display_choice(self, user_input):#更新选项内容
        if self.end:
            self.q_a = self.q_a1
        else:
            self.q_a = self.q_a2   
        self.hint1 = self.q_a[self.order][1]
        self.hint2 = self.q_a[self.order][2]
        return self.hint1, self.hint2
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        if self.q_a == self.q_a1:
            if self.c1 or self.c2: 
                self.will_delta +=general.will_pace1
                self.anger -= general.anger_pace1
                return self.hint1
            
        elif self.q_a == self.q_a2:   
            if self.c1 or self.c2:
                self.will_delta -=general.will_pace2
                self.anger += general.anger_pace2
                return self.hint2
        else:
            return ""

    def judge_user(self, user_input):
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c ,self.chat_start or self.chat_end    
    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_start:            
                a = self.q_a[self.order][0]
                self.order += 1
                return a ,0,0,self.end
        
        if self.chat_end:
            if self.q_a == self.q_a1:
                out =  ""
            else:
                out =  ""
            return out , 0, 0, self.end
        return "" ,0 , 0, self.end



'''

class trader3:
    def judge(self, user_input):
        """
        判断用户的购买或出售操作
        :param user_input: 用户输入的字符串
        """
        global user_money
        if not user_input:
            self.update_output("Do you still want to buy something?")
            return

        words = user_input.lower().split()
        if len(words) != 3:
            self.when_come_to_wrong_words()
            return

        action, goods, quantity_str = words
        quantity = int(quantity_str) if quantity_str.isdigit() else 0

        if action == "buy":
            price = self.value(goods, "buy")
            if price == 0:
                self.when_come_to_wrong_words()
            elif price * quantity > user_money:
                self.update_output(f"You don't have enough money! Now you have {user_money} dollars!")
            else:
                user_money -= price * quantity
                self.update_output(f"You have bought {quantity} {goods}! Now you have {user_money} dollars!")
        elif action == "sell":
            price = self.value(goods, "sell")
            if price == 0:
                self.when_come_to_wrong_words()
            else:
                user_money += price * quantity
                self.update_output(f"You have sold {quantity} {goods}! Now you have {user_money} dollars!")
        else:
            self.when_come_to_wrong_words()

    def value(self, goods_name, condition):
        """
        获取商品的价格
        :param goods_name: 商品名称
        :param condition: 操作类型，可以是 "buy" 或 "sell"
        :return: 商品价格
        """
        if condition == "buy":
            return {
                "corn": 4,
                "tomato": 5,
                "apple_vision_s_pro_max_ultra_turbo_plus": 29999
            }.get(goods_name, 0)
        elif condition == "sell":
            return {
                "corn": 10,
                "tomato": 20,
                "apple": 2,
                "wood": 4
            }.get(goods_name, 0)
        return 0

    def when_come_to_wrong_words(self):
        """
        处理用户输入错误的情况
        """
        self.update_output("We can't identify your words! Please check your input lines~")

        
'''