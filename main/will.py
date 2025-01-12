class player_will:#制造单例类
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(player_will, cls).__new__(cls)
            cls._instance.player_will = 0
        return cls._instance

    def get_player_will(self):
        return self.player_will

    def set_player_will(self, value):
        self.player_will = value

    def modify_player_will(self, delta):
        self.player_will += delta
#---------到此为止------------
