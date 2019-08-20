import random
from collections import deque, defaultdict
import pandas as pd


class Individual:
    """个体基类.
    主要用于被继承.
    """

    def __init__(self, name, preferences):
        """初始化.
        :param str name: 姓名
        :param list preferences: 偏好列表
        """
        # 名称
        self.name = name
        # 偏好
        self.preferences = preferences
        # 偏好序
        self.preferences_rank = self._preferences_rank()
        # 匹配结果
        self.matched = None

    def _preferences_rank(self):
        """偏好序.
        偏好序
        """
        preferences_rank = dict()
        i = 1
        for item in self.preferences:
            if isinstance(item, int):
                preferences_rank[item] = i
            elif isinstance(item, set):
                for unit in item:
                    preferences_rank[unit] = i
            else:
                print('Wrong type!')
                raise Exception
            i = i + 1

        return preferences_rank

    def __repr__(self):
        """打印信息.
        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        return fmt.format(type=self.__class__.__name__, name=self.name,
                          someone=self.matched.__repr__())
    # def __repr__(self):
    #     return repr(self.name)


class Student(Individual):

    def __init__(self, name, preferences):
        """
        :param str name: 名称
        :param list preferences: 偏好
        """
        super().__init__(name=name, preferences=preferences)
        # 追求列表
        self._proposal_list = deque(preferences)
        # 被接受者个体
        self._accepted_by = None

    def propose(self):
        """向清单中排名最靠前的被追求者提出请求.
        :return: 返回被追求者的名称
        :rtype: str
        """
        # 如果上一轮没有被女性暂时接受，并且追求列表不为零，
        # 那么返回追求列表中最靠前的个体，否则返回None
        if (self._accepted_by is None) and (len(self._proposal_list) > 0):
            return self._proposal_list.popleft()
        else:
            return None

    def __repr__(self):
        """打印信息.
        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        if self._accepted_by is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone=self._accepted_by.name)
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone='None')
    # def __repr__(self):
    #     return repr(self.name)


class School(Individual):
    """女性类.
    用于描述被追求者.
    """

    def __init__(self, name, preferences, max_accepted=1):
        """女性类.
        :param str name: 名称
        :param list preferences: 偏好
        :param int max_accepted: 最多可接受追求者的数量，默认为1
        """
        super().__init__(name=name, preferences=preferences)
        # 对自己请求的追求者列表
        self._be_prosoed_by = []
        # 接受的追求者
        self._accept = None
        # 接受追求者的数量
        self._accept_number = max_accepted

    def reset_proposal(self):
        """重置追求者列表中所有追求者的匹配对象为None.
        因为暂时被接受的追求者的匹配对象是自己，但是下一轮需要重新和其他追求者
        一起重新追求，所以需要把追求者列表中的先去成功匹配的对象位置为None.
        :return: 无返回值
        """
        for item in self._be_prosoed_by:
            item._accepted_by = None

    def filtrate(self):
        """筛选列表中所有的追求者，接受偏好排序在前的个体，拒绝其他所有追求者.
        :return: 返回被接受的追求者的名称
        """
        # 重置所有追求者的匹配对象为None
        self.reset_proposal()
        # 生成字典，键为追求者在自己偏好中的次序，值为追求者的姓名
        proposal_dict = defaultdict(list)
        for man in self._be_prosoed_by:
            if man.name in self.preferences_rank:
                proposal_dict[self.preferences_rank[man.name]].append(man.name)
            else:
                pass
                # print("Not in preference!")
                # raise Exception

        # 储存被接受的追求者的姓名
        accepted = []
        available_accepted_number = self._accept_number
        for i in sorted(proposal_dict):
            to_be_choosen = proposal_dict[i]
            if len(to_be_choosen) <= available_accepted_number:
                accepted.extend(proposal_dict[i][0:len(to_be_choosen)])
                available_accepted_number -= len(to_be_choosen)
            else:
                accepted.extend(random.sample(proposal_dict[i],
                                              available_accepted_number))
                available_accepted_number = 0

        # 返回接受者，若无，则返回None
        if len(accepted) > 0:
            return accepted
        else:
            return None

    def __repr__(self):
        """打印信息.
        主要用于打印类信息.
        """
        fmt = '{type} {name} matched {someone}'
        if self._accept is not None:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone=' '.join(str([item.name
                                                for item in self._accept])))
        else:
            return fmt.format(type=self.__class__.__name__, name=self.name,
                              someone='None')
    # def __repr__(self):
    #     return repr(self.name)


class StableMatcher:
    """匹配主类.
    进行匹配的主类.
    """

    def __init__(self, men=None, women=None):
        """初始化.
        param list men: 男性（追求者）列表
        param list women: 女性(被追求者)列表
        """
        self._men = men
        self._women = women

        self._men_mapping = {man.name: man for man in self._men}
        self._women_mapping = {woman.name: woman for woman in self._women}

    def match(self, echo=False):
        """进行匹配.
        进行匹配的主要函数
        """
        # 是否继续匹配的标志
        match_flag = True
        # 匹配的轮次
        round = 1

        while (match_flag):
            # 匹配中止标志
            match_flag = False

            for man in self._men:
                # 追求者请求，返回被追求者的姓名
                proposed_female_name = man.propose()
                if proposed_female_name is not None:
                    match_flag = True
                    # 添加某追求者到被追求者本轮要筛选的追求者列表中
                    self._women_mapping[proposed_female_name]._be_prosoed_by.append(man)

            if not match_flag:
                break

            for woman in self._women:
                # 如果本轮有追求者
                if len(woman._be_prosoed_by) > 0:
                    # 根据被追求者的偏好列表筛选追求者，保留偏好序前列的追求者，拒绝其他人
                    accepted = woman.filtrate()
                    # 更新被追求者暂时接受的个体到被追求者的接受者列表
                    if accepted is not None:
                        woman._accept = [self._men_mapping[acc]
                                         for acc in accepted]
                    else:
                        woman._accept = None
                    # 把本轮匹配成功的追求者放入向该被追求者的请求列表中，以便下一轮重新进行匹配
                    if woman._accept is not None:
                        woman._be_prosoed_by = woman._accept
                    else:
                        woman._be_prosoed_by = []
                    # 更新匹配成功的追求者的暂时成功匹配对象为该被追求者
                    if woman._accept is not None:
                        for temp_accepted in woman._accept:
                            temp_accepted._accepted_by = woman

            if echo:
                print('-' * 10, 'round{}'.format(round), '-' * 10)
                for man in self._men:
                    print(man)

                for woman in self._women:
                    print(woman)

            round += 1

        print('\n' + '-' * 50, 'The number of rounds={}'.format(round-1), '-' * 50 + '\n')


    @property
    def result(self):
        pursuers_result = defaultdict(list)
        for item in self._men:
            if item._accepted_by is None:
                pursuers_result[item.name].append(item._accepted_by)
            else:
                if isinstance(item._accepted_by, School):
                    pursuers_result[item.name].append(item._accepted_by.name)

        pursueds_result = defaultdict(list)
        for item in self._women:
            if item._accept is None:
                pursueds_result[item.name].append(item._accept)
            else:
                if isinstance(item._accept, Student):
                    pursueds_result[item.name].append(item._accept.name)
                else:
                    pursueds_result[item.name].extend([unit.name for unit in item._accept])

        return dict(pursueds_result.items())


    def __repr__(self):
        """打印匹配信息.
        :return: 无返回值
        """
        lines = '-'*50
        return_string = ''.join([lines, 'Final Reslut', lines])

        for man in self._men:
            if man.__repr__().endswith('None'):
                continue
            return_string = '\n'.join([return_string, man.__repr__()])

        return_string = ''.join([return_string, '\n\n', 'In another way...',
                                 '\n'])

        for woman in self._women:
            return_string = '\n'.join([return_string, woman.__repr__()])

        return_string = ''.join([return_string, '\n', lines,
                                 '-'*len('Final Reslut'), lines])

        return return_string


if __name__ == '__main__':

    data1 = pd.read_csv('F:/Python_Code/Comp702/data/full_preferencelist/20/Schools-Preference19.csv')
    school1 = data1.set_index('Unnamed: 0').T.to_dict('list')

    data2 = pd.read_csv('F:/Python_Code/Comp702/data/full_preferencelist/20/Students-Preference19.csv')
    student1 = data2.set_index('Unnamed: 0').T.to_dict('list')

    students = []
    for k, v in student1.items():
        students.append(Student(k, v))

    schools = []
    for k, v in school1.items():
        schools.append(School(k, v, 20))      # sc/st

    matcher = StableMatcher(men=students, women=schools)
    matcher.match(echo=False)
    # print(matcher)
    # print(matcher.result)

    # fw = open("F:/Python_Code/Comp702/output_matching/full_preferencelist/5/DAmatching.txt", 'w+')
    # fw.write(str(matcher.result))  # 把字典转化为str
    # fw.close()



