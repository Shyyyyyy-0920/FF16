import pygame

from openai import OpenAI
from typing import List, Dict
client = OpenAI(
    base_url='http://10.15.88.73:5002/v1',
    api_key='ollama',  # required but ignored
)
#以上为常见设定
'''
user_money 是临时设定参数=200,合并时需要修改

'''
user_money = 200

#以下是正文


class Trader_chat():#设置一个商人ai对话类
    def __init__(self,messages_trader = [{}] , list_chat = [] , list_ai = [] , list_user = []):
        self.messages_trader = messages_trader
        self.list_chat = list_chat
        self.list_ai = list_ai
        self.list_user = list_user

    def chat(self,messages_trader = [{}] , list_chat = [] , list_ai = [] , list_user = []): # 定义一个聊天函数
            
        def when_come_to_wrong_words():#错误提示函数
            print("We can`t identify your words!Please check your input lines~")

        def value(goods_name , condition):#
            if condition == "buy":        
                if goods_name == "corn":
                    return 4
                elif goods_name == "tomato":
                    return 5
                elif goods_name == "apple_vision_s_pro_max_ultra_turbo_plus":
                    print("Really?!")
                    messages_trader.append([{"role": "assistant", "content":"Really?!"}])
                    return 29999
                else:
                    return 0
            if condition == "sell":
                if goods_name == "corn":
                    return 10
                elif goods_name == "tomato":
                    return 20
                elif goods_name == "apple":
                    return 2
                elif goods_name == "wood":
                    return 4
                else:
                    return 0

        def judgement_user(value ,messages_trader, userinput = "user said nothing"):  #定义对用户对话进行实际操作的内容
            global user_money
            
            if userinput == "user said nothing":#如果没有输入，提示输入
                print("Do you still want to buy something?")
                userinput = input("User input: ")
                messages_trader.append({"role": "assistant", "content":"Do you still want to buy something?"})
                pass
            
            list_user_say = []  #将所有单词转换为列表中单个的字符串
            list_user_say = userinput.split(" ")
            list_user_say =[str(i).lower() for i in list_user_say]

            
            if "buy" in list_user_say and len(list_user_say) == 3 :
                money = value(list_user_say[1] , "buy")
                num = int(list_user_say[2])
                if money == 0:
                    when_come_to_wrong_words()
                    pass
                else:
                    if money * num > user_money:
                        print("You don`t have enough money!")
                        messages_trader.append({"role": "assistant", "content":"You don`t have enough money!"})#判断 手里现有的资金是否是否足够，不够发出提示
                        pass
                    else:
                        user_money -= money * num
                        print("You have bought " + str(num) + " " + list_user_say[1] + "!")
                        messages_trader.append({"role": "assistant","content":"You have bought " + str(num) + " " + list_user_say[1] + "!"})   
                        pass#购买
            
            
            if "sell" in list_user_say and len(list_user_say) == 3 :#同样的，售卖也这么写
                money = value(list_user_say[1], "sell")
                num = int(list_user_say[2])
                if money == 0:
                    when_come_to_wrong_words()
                    pass
                else:
                    user_money += money * num
                    print("You have sold " + str(num) + " " + list_user_say[1] + "!")
                    messages_trader.append({"role": "assistant","content":"You have sold " + str(num) + " " + list_user_say[1] + "!"})
                    pass


        # def judgement_ai(aioutput,message_trader):  #定义对ai对话进行实际操作的内容
        #     pass
        #     #要检测是否要涨价   和  是否要退出
        #     list_ai_say = []  #将所有单词转换为列表中单个的字符串
        #     list_ai_say = aioutput.split(" ")
        #     list_ai_say =[str(i).lower() for i in list_ai_say]


        '''
        没做完QAQ
        '''


        #以下为大模型  ~调教~


        #1.按1 买入商品  按2 卖出商品  2.购买输入句式 "buy 'good`s name' 'good`s quantity'"  3.卖出输入句式 "sell 'good`s name' 'good`s quantity'"
        messages_trader : List[Dict] = [
            {"role": "system", "content": "You are an trader lives in a cyberpunk world.\
                the user`s name is 'Mr.Knight' .\
                What you need to say at first is greetings,less than 50 words.\
                You should tell the user 'type 1 to buy goods and 2 to sell goods.'\
                Then you can announce your goods and the price.\
                the details are as follows:\
                1 corn per 4 dollar for user to buy,10 dollar for user to sell\
                1 tomato per 5 dollar for user to buy,20 dollar for user to sell\
                1 apple per 2 dollar for user to sell,\
                1 wood per 4 dollar for user to \
                An Apple_Vision_s_Pro_Max_Ultra_Turbo_Plus per 30000 dollar before,\
                now only on a very surprising prise ----29999 dollar for user to buy!!!\
                In order to make the information clearly,You'd better make each item take up its own line of space\
                you need to tell the user how to buy and sell goods.\
                like:(buy 'good`s name' 'good`s quantity')  for buying goods\
                and (sell 'good`s name' 'good`s quantity') for selling goods)\
                At the end of your first speaking,you need to tell the user to only print\
                'exit', 'quit',to end the conversation.\
                specially, if the user make you drive mad,\
                you can warn him by increase the value of your goods for a little\
                and you can also say 'son of the bitch!','You stupid bugger!' to strike back .\
                If you get annoyed to the extreme, you have the option of just swearing or ending the conversation\
                by saying (I will end my business,You get out')\
                At the end of your first speaking,you need to tell the user to only print\
                And except the goods announcement,other words should be less than 100 words or Chinese words.)"}#进行AI扮演角色的要求设置
        ]

        list_chat = []

        while True:

            list_ai = []#AI当前语句
            list_user = []#用户当前语句

            user_input = input("User input: ")
            if user_input.lower() in [ "exit", "quit"]:#退出对话的要求
                print("chat ends.")
                # list_user.clear()   #清空对话记录后退出,或者在彻底退出对话系统后删除
                break
            list_user.append(user_input)#记录用户输入-judge

            messages_trader.append({"role": "user", "content": user_input})#添加用户输入-ai回答

            response = client.chat.completions.create(
                model="llama3.2",      
                messages_trader=messages_trader,    # a list of dictionary contains all chat dictionary
            )

            # 提取模型回复
            assistant_reply = response.choices[0].message.content
            print(f"Llama: {assistant_reply}")

            list_ai.append(assistant_reply)#记录AI回复-judge

            # 将助手回复添加到对话历史-ai回复
            messages_trader.append({"role": "assistant", "content": assistant_reply})

            list_chat.extend({"user":user_input , "ai":assistant_reply})#记录会话记录

            judgement_user(value,messages_trader,user_input)#对用户对话进行实际操作的内容
            # judgement_ai(assistant_reply,messages_trader) #对ai对话进行实际操作的内容
        
'''
需要对接的东西：
    list_ai = []#AI当前语句
    list_user = []#用户当前语句


'''
# trader1 = Trader_chat()
# Trader_chat.chat(trader1)

class Player1_chat():#设置一个商人ai对话类
    def __init__(self,messages_player1 = [{}] , list_chat = [] , list_ai = [] , list_user = []):
        self.messages_trader = messages_player1
        self.list_chat = list_chat
        self.list_ai = list_ai
        self.list_user = list_user

    def chat(self,messages_player1 = [{}] , list_chat = [] , list_ai = [] , list_user = []): # 定义一个聊天函数

        messages_player1 : List[Dict] = [
            {"role": "system", "content": "We are going to play a game now, and I have an integer in my mind. You can ask me an integer each time, and I will tell you whether the answer will be larger or smaller than the number asked. You need to use the minimum number of questions to answer what the answer is. For example, when the answer in my mind is 200, you can ask 100 and I will tell you that the answer is greater than 100."}
        ]

        while True:
            user_input = input("User input: ")
            if user_input.lower() in [ "exit", "quit"]:
                print("chat ends.")
                break

            messages_player1.append({"role": "user", "content": user_input})

            response = client.chat.completions.create(
                model="llama3.2",      
                messages_player1=messages_player1,    # a list of dictionary contains all chat dictionary
            )

            # 提取模型回复
            assistant_reply = response.choices[0].message.content
            print(f"Llama: {assistant_reply}")

            # 将助手回复添加到对话历史
            messages_player1.append({"role": "assistant", "content": assistant_reply})










        #     {"role": "system", "content": "We are going to play a game now, and I have an integer in my mind. \
        #         You can ask me an integer each time, \
        #      and I will tell you whether the answer will be larger or smaller than the number asked. \
        #      You need to use the minimum number of questions to answer what the answer is. \
        #      For example, when the answer in my mind is 200,\
        #       you can ask 100 and I will tell you that the answer is greater than 100."}
        # ]
