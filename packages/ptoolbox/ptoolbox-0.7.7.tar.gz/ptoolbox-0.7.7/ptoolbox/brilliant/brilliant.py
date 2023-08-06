import copy
import html

import requests
import tomd
from bs4 import BeautifulSoup

from ptoolbox.helpers.clog import CLog
from ptoolbox.models.general_models import Problem, TestCase, ProblemType
from ptoolbox.models.question import Question, QuestionType, QuestionOption
from ptoolbox.ucode.ucode import UCode


def to_markdown(html_text):
    if not html_text:
        return ""

    html_text = html_text.replace("$$$", "$")
    soup = BeautifulSoup(html_text, 'html.parser')

    # img tag must be inside <p> tag
    imgs = soup.select("img")
    if imgs:
        for img in imgs:
            if "alt" in img:
                img.string = img['alt']
            del img['style']
            del img['alt']
            new_tag = soup.new_tag('p')
            img.wrap(new_tag)

    bold = soup.select('.tex-font-style-bf')
    for tag in bold:
        tag.name = 'strong'
        tag.attrs = {}
    tt = soup.select('.tex-font-style-tt')
    for tag in tt:
        tag.name = 'code'
        tag.attrs = {}
    tt = soup.select('.tex-font-style-it')
    for tag in tt:
        tag.name = 'i'
        tag.attrs = {}

    # convert subscript and superscript to latext
    #  *...*<sub class="lower-index">*...*
    #  *...*<sub class="upper-index">*...*
    subscripts = soup.select('sub')
    for subscript in subscripts:
        print(str(subscript))
    supper_scripts = soup.select('sup')
    for supper_script in supper_scripts:
        print(str(supper_script))

    res = tomd.convert(html.unescape(soup.decode())).strip()


    return res


class Brilliant:
    def __init__(self):
        self.s = requests.session()
        self._headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'origin': "https://brilliant.org/",
            'referer': "https://brilliant.org/community/home/weekly-problems/",
        }
        self.csrf = ''

    def get_quiz_list(self):
        url = f'https://brilliant.org/community/home/weekly-problems/'

        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        raw = r.text
        # print(raw)

        soup = BeautifulSoup(raw, 'html.parser')
        # self.csrf = soup.select('span.csrf-token')[0]['data-csrf']
        # print('CSRF:', self.csrf)
        res = {}
        weeks = soup.select('div.stat-potw-week')
        for week in weeks:
            title = week.select('h3')[0].decode_contents()
            print(title)
            res[title] = []
            levels = week.select("div > a")
            for level in levels:
                url = "https://brilliant.org" + level['href']
                print("\t" + url)
                res[title].append(url)

        return  res

    def get_quiz(self, url):
        headers = copy.deepcopy(self._headers)
        # for i in range(1, 6):
        r = self.s.get(f"{url}?p={1}", headers=headers)

        raw = r.text
        # print(raw)
        res = []
        soup = BeautifulSoup(raw, 'html.parser')

        questions = soup.select("div.solv-content div.question-text")
        options = soup.select("div.solv-form > form")
        print(len(questions))
        print(len(options))
        for i in range(len(questions)):
            question = questions[i]
            option = options[i]
            # input_field = option.select("div.fields input")
            choices = option.select("label.choice")
            ques = Question()
            ques.source = url
            ques.statement = str(question)
            if choices:
                print("\nChoice")
                ques.type = QuestionType.SINGLE_CHOICE
                question_options = []
                for opt in choices:
                    span = opt.findAll("span", attrs={'class': None})[0]
                    choice_text = span.decode_contents().strip()
                    print(choice_text)
                    question_options.append(QuestionOption(text=choice_text, text_type="html"))
                ques.options = question_options
            else:
                print("\nshortanswer")
                ques.type = QuestionType.SHORT_ANSWER

            res.append(ques)

        return res


if __name__ == '__main__':
    br = Brilliant()
    res = br.get_quiz_list()
    print(res)

    probs = br.get_quiz("https://brilliant.org/weekly-problems/2018-12-10/basic")
    print(probs)

    # ucode = UCode("https://dev-api.ucode.vn/api", "b1f3bba4df8c50713ee39d9f75647739")
    # course_id = 102
    # for i, level in enumerate(['Basic', 'Intermediate', 'Advanced']):
    #     chapter_id = ucode.create_chapter(course_id=course_id, chapter_name=level, status="published")
    #     for title, urls in res.items():
    #         probs = br.get_quiz(urls[i])
    #         lesson_name = title
    #         for prob in probs:
    #             print(prob.statement)
    #             print(prob.type.name)
    #             if prob.type == QuestionType.SINGLE_CHOICE:
    #                 print(prob.options)
    #
    #         lesson_id = ucode.create_lesson_item(course_id=course_id, chapter_id=chapter_id,
    #                                              lesson_name=lesson_name, type="quiz", status="published")
    #         CLog.info(f"Lesson #{lesson_id} created!")
    #
    #         for question in probs:
    #             ucode.create_problem(lesson_id=lesson_id, problem=question, lang='en',
    #                                  statement_format='html', score=20, xp=50)
