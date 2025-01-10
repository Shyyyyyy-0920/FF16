import pygame
import chat

class player:
    kind_point = 5#测试用的善恶值

class trader1:#第一关的trader
    answer1 = ["I don`t know", "Why?I`ve never been here!" , "No , I`m so sorry"]
    answer2 = ["Frisk", "Yeah, I know this hell place!" , " You are telling me.YOU R A FLEEING LOSER!"]
    order =0     #选择式对话的顺序（应该对应第几次选择式对话
    can = False  #是否开启选择式对话
    hint1 = ""   #选择1
    hint2 = ""   #选择2
    chat_end = False   #选择式对话是否结束
    kind_point = 0
    
    def display_choice(self, user_input):#更新选项内容
        if "yes" in user_input.lower():#玩家输入 yes 后开始对话
            self.can = True
        if self.can:
            if len(self.answer1) >= self.order + 1:
                self.hint1 = self.answer1[self.order]
                self.hint2 = self.answer2[self.order]
                self.order += 1
                return self.hint1, self.hint2
            else:                             #结束绘画后，基本数据重置
                self.order = 0
                self.can = False
                self.answer1 = ""
                self.answer2 = ""
                self.chat_end = True
                return "" , ""
        else:
            return "" , ""
        
    def choose(self, user_input):#判定玩家选择了哪一个选项
        if "1" in user_input.lower():
            self.kind_point +=1
            return self.hint1
        
        elif "2" in user_input.lower():
            self.kind_point -=1
            return self.hint2
        else:
            return ""

    def judge_user(self, user_input):#与chat 函数建立联系，返回选项内容与玩家选择对应的内容
        c = self.choose(self,user_input)
        a, b = self.display_choice(self,user_input)       
        return a, b, c

    def judge_assistant(self, ai_input):#对ai扮演的聊天对象的回复
        if self.chat_end:
            if player.kind_point > 2:
                out =  "(* ^ w ^) \n"
            else:
                out =  "凸(╬￣^￣) \n You are really a devil! \n"
            self.chat_end = False
            return out + "What behind this entrance is a once prosperous village. \
            However, countless lonely souls are wandering around there because of the massacre. \
            You can go and have a look."
        return ""




class trader3:
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""


class monster_a:#打怪之前的敌人
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""

class monster_b:#打败之后的敌人
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""

class boss_a:
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""

class boss_b:
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""

class boss_c:
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""


class boss_d:
    def judge_user(self, user_input):
        return ""
    
    def judge_assistant(self, ai_input):
        return ""



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