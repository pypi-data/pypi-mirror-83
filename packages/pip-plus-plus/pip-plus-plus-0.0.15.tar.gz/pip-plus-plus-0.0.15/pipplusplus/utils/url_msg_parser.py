class UrlMessageParser(object):
    @classmethod
    def parse(cls, data):
        pass


class UrlMessageListParser(UrlMessageParser):
    @classmethod
    def parse(cls, data):
        res = data.split("\r\n")
        minus_line_index = 0
        for i in range(len(res)):
            num_of_space = res[i].count(" ")
            if num_of_space:
                splitted = res[i].split(" " * num_of_space)
                if splitted[0] == ("-" * len(splitted[0])) and splitted[1] == ("-" * len(splitted[1])):
                    minus_line_index = i
                res[i] = [splitted[0].strip(), splitted[1].strip()]
            else:
                del res[i]
        if minus_line_index:
            del res[minus_line_index]
        return res

