import pygame
# 关于用户输入的话语检测功能，没做好


class Trader1:
    def judgement_user(self,person, user_input):
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
