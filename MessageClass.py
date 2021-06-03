class BotMessage():
    def __init__(self, IdOfReciver, Text):
        self.__IdOfReciver = IdOfReciver
        self.__Text = Text

    def GetId(self):
        return self.__IdOfReciver

    def GetText(self):
        return self.__Text