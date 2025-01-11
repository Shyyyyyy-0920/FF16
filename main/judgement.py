import pygame
import chat

class general:#本部分的一些通用参数
    will_pace1 = 1  #will值变化量设置
    will_pace2 = 2    
    will_pace5 = 5
    will_pace10 = 10 

    
    anger_pace1 = 1  #怒气值变化量设置
    anger_pace2 = 2

    trader3_anger = 0
    sans_anger = 0
    top_anger_sans = 6#     怒气值最高值——sans
    top_anger = 4           #怒气值最高值——trader
    end = None            #是否进入好结局
    

# ————————————————————————————————————————————————不同对话对象的剧情对话————————————————————————————————————————————————————————



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
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            self.will_delta -=general.will_pace1
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
                 if you want to know it , go there and witness the sence.\n "\
                "*(Chat End)*"
            else:
                out =  ":(  \n YOU ARE A TURE DEVIL! \n"\
                + "What behind this entrance is a once prosperous village. \
                 \n BUT \n \n countless lonely souls are wandering around there because of \n YOUR FUCKING GENOCIDE \n \
                 go to there and witness WHAT YOU HAD DONE!!.\n "\
                "*(Chat End)*"
            self.fight = False
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
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            general.trader3_anger -= general.anger_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace1
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
                 \n We will praise your kind and helping heart!\n "\
                "*(Chat End)*"
            else:
                out =  "\n YOU ARE A TURE DEVIL! \n\
                        Chara! \n \
                       Now I have nothing to lose! \n\
                        I`ll fight you until the end!\n\
                        GO HELL!\n "\
                        "*(Chat End)*"
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
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            self.anger -= general.anger_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace1
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
                +"Die!Idiot!\n "\
                "*(Chat End)*"
                self.fight = True
            else:
                out =  ":|  \n Alright,I know. \n"\
                + "As a ghost, I can see your soul was divided into two parts. \
                 \n  now you let your kind side facing me \n \
                 But,the other side----- Chara. \n\
                 Now try to absorbe your soul. \n \
                 Maybe you can find a way to save your soul \
                 by working out more and more tasks to let the Chara`s soul be liberated.\n \
                 Start your adventure!We trust you! Good luck!\n "\
                "*(Chat End)*"
                self.fight = False
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
    up = None #是否战斗难度升级

    def display_choice(self, user_input):#更新选项内容
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            self.anger -= general.anger_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace1
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
                out =  ":)))))))\n\
                You think I was gonna let you off the hook? \n \
                Absolutely No!\n "\
                "*(Chat End)*"
                self.up = False
                return out , self.will_delta, self.anger, self.up

            else:
                out =  "Its a beautiful day outside. \n \
                        Birds are singing,\n \
                        flowers are blooming.\n \
                        On days like these,\n \
                        kids like you......\n \
                        SHOULD BE BURNING IN HELL.\n "\
                        "*(Chat End)*"
                self.up = True
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
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            self.anger -= general.anger_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace1
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
                        I'm DETERMITION\n " \
                        "*(Chat End)*"
                self.fight = False
            else:
                out =  "You'd be dead where you stand.GO HELL.\n "\
                        "*(Chat End)*"
                self.fight = True
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight



class boss_c:  #sans  后期阶段
    q_a = [["What?! It seems that there are two souls sharing one body" , "(redempt)You see, There is a devil inside me." , "(corrupt)I cant`t control myself! AH!!!!"],\
        ["Then there are more reason to kill you and your soul" , "(redempt)NO! This would only make Chara awake!" , "(corrupt)Killing is exactly what I was looking forward to"],\
        ["So why you are so willing to come and die? How foolish you are!", "(redempt)Because I have the DETERMINATION!" ,"(corrupt)It will be the most regrettable words you've ever said"]]
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
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            return " " , " "
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        
        if self.c1: #按下1后会发生的事情
            self.will_delta +=general.will_pace1
            self.anger -= general.anger_pace1
            self.c2 = False
            return self.hint1
        
        elif self.c2:   #按下2后会发生的事情
            self.will_delta -=general.will_pace1
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
                out =   "So there is only one solution to this. \n \
                        Prove yourself... Prove to me you are strong enough to survive."\
                        "*(Chat End)*"
                self.fight = False
            else:
                out =  "You'd be dead where you stand. \n \
                        GO HELL \n \
                        :)"\
                        "*(Chat End)*"
                self.fight = True
            if general.sans_anger > general.top_anger_sans:
                general.end = False
            return out , self.will_delta, self.anger, self.fight
        return "" ,0 , self.anger, self.fight



        
###################################################有关boss战结局的内容

class boss_d: #结局A——————Frisk战胜Chara
    q_a1 = [["Ao!It hurts! Now I notarize you DETERMINATION have it`s power!" , "I believe I can destory Chara by myself!" , "Get out of my mind! Chara!"],\
        ["Hold on your will!Or he`ll absorbe your soul. " , "I want to be alive!With all my friends!" , "Please , Sans!Help me!Let Chara liberate in peace!"],\
        ["I got it , The  Chara`s soul! \n \
         Papyrus ,Undyne ,I avenge you!", "(redempt)-999999999999999999" ,"......"] , \
        ["......(Sans panting) \n \
         Finally , all tragic storys come to the end!", "Bye Chara, may you rest in peace...", "......"]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2
    end = general.end ################结局的判定标准  

    def display_choice(self, user_input):#更新选项内容 
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            return " " , " "
    def choose(self, user_input ,quick_end):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        if self.c1 :
            return self.hint1
            
        elif self.c2 :   
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
                out =  "The souls who could not rest because of Chara are calmed now... \n \
                        The Underworld will have it`s bright and new future... \n \
                        Now you can leave an back to your world~~~ \n \
                        ............ \n \
                        (Ending --- Redemption)"
                self.chat_end = True
                self.chat_end = False
                return out , 0, 0, self.end
        else:
            return "" ,0 , 0, self.end



class boss_e:#结局B——————Chara战胜Frisk

    q_a = [["Akh akh... \n In the end, nothing's gonna change..." , "......" , "......"],\
        ["Now... \n \
            F...Frisk...\n \
            no, ......not you... \n \
            ... \n \
            I see it... \n \
            You`re Chara...\n \
            right?" , "It was me the whole time" , "Enough talking? Time to die"],\
        ["If you ... if you try t... \n \
            to ... destroy... \n \
            Akh  akh .... \n \
            I ... won`t...let you...... n\
            let you go...", "You can try it." ,"Burn in hell :)"],\
        ["......", "Finally, it's quiet.", "In this world, nobody could stop me now."]]
    
    order =0     #选择式对话的顺序（应该对应第几次选择式对话e  
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    will_delta = 0  #对话阶段的善恶值变化
    chat_start = False #是否开启选择式对话
    
    c1 = False #是否按了1
    c2 = False #是否按了2

    end = general.end ################结局的判定标准  

    def display_choice(self, user_input):#更新选项内容 
        if "skip" in user_input.lower() or "break" in user_input.lower():#玩家输入 yes 后开始对话
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
            return " " , " "
    def choose(self, user_input ):#判定玩家选择了哪一个选项
        self.c1 = "1" in user_input.lower()
        self.c2 = "2" in user_input.lower()
        if self.c1 :
            return self.hint1
            
        elif self.c2 :   
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
                out =  "...........    \n \
                        *(Entity Presence Cannot Be Detected)* \n \
                        ........... \n \
                        CHARA : \n \
                        Hello, I`m Chara \n \
                        Thank you for setting me free \n \
                        It was your murderousness that awakened my \n \
                        DETERMINATION \n \
                        Thanks for your help.\n \
                        .\n \
                        And\n \
                        I\n \
                        will\n \
                        come\n \
                        to\n \
                        see\n \
                        you\n \
                        soonnnnnnnnnnnnnnnnnn\n \
                        .\n \
                        ...............\n \
                        ............................................................................. \n \
                        (Ending --- Corruption)"

                return out , 0, 0, self.end
        else:
            return "" ,0 , 0, self.end











#曾经用来AI对话来买卖东西的程序的废稿
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