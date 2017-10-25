"""
模式匹配结果
"""


class PatternMatchResult:
    def __init__(self):
        # 问题类型模式文件——模式匹配结果项
        self.__q_r_dict = {}

    def get_questiontypepatternfiles_loosetocompact(self):
        return self.fromcompact_toloose(False)

    def get_questiontypepatternfiles_compacttoloose(self):
        return self.fromcompact_toloose(True)

    def fromcompact_toloose(self, compact_toloose):
        temp_dict = {}
        string_list = []
        for file in self.__q_r_dict.keys():
            string_list.append(file.get_file())
            temp_dict[file.get_file()] = file
        sorted(string_list)
        if not compact_toloose:
            string_list.reverse()
        result = []
        for item in string_list:
            result.append(temp_dict[item])
        return result

    def add_pattern_match_result(self, file, items):
        """
        添加模式匹配结果
        :param file:问题类型模式文件
        :param items: 模式匹配结果项
        """
        value = self.__q_r_dict.get(file)
        if value is None:
            value = items
        else:
            value.extend(items)
        self.__q_r_dict[file] = value

    def get_pattern_match_result(self, file):
        """
        :param file: 问题类型模式文件
        :return:模式匹配结果
        """
        return self.__q_r_dict[file]

    def get_all_pattern_match_result(self):
        value = []
        for v in self.__q_r_dict.values():
            value.extend(v)
        return value
