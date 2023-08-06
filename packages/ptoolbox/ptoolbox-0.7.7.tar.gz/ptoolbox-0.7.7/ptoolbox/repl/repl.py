import copy
import json
import os
import traceback
from datetime import datetime

from dateutil import tz, parser

from draftjs_exporter.html import HTML
from draftjs_exporter_markdown import BLOCK_MAP, ENGINE, ENTITY_DECORATORS, STYLE_MAP

import requests
from ucode.services.dsa.problem_service import ProblemService

from ptoolbox.helpers.misc import make_slug
from ptoolbox.models.general_models import MatchingType, Classroom, ProgrammingLanguage, ProblemStatus, TestCase, \
    JudgeMode, Problem


class ReplIt:
    def __init__(self, cookies):
        self.s = requests.session()
        self._headers = {
            'origin': 'https://repl.it',
            'referer': 'https://repl.it/login',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'cookie': cookies
        }
        self.cookies = cookies

    def get_classroom_list(self):
        url = "https://repl.it/data/teacher/classrooms"
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)
        raw = r.json()
        print(json.dumps(raw))
        print([v['id'] for v in raw])
        return raw

    def get_classroom(self, classroom_id, get_assignments=True, get_students=False, get_submissions=False,
                      get_all_problems=False):
        url = 'https://repl.it/data/classrooms/{}'.format(classroom_id)
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)
        raw = r.json()
        print(json.dumps(raw))

        classroom = Classroom()
        classroom.src_id = raw['id']
        classroom.name = raw['name']
        if raw['language_key'] == 'python3':
            classroom.language = ProgrammingLanguage.python3

        problems = []
        if get_assignments:
            url = 'https://repl.it/data/classrooms/{}/assignments'.format(classroom_id)
            r = self.s.get(url, headers=headers)
            assignments = r.json()
            for a in assignments:
                for p in ['classroom_id', 'time_deleted', 'time_updated', 'time_due', 'time_created', 'github_id']:
                    a.pop(p, None)
                # time_published = null: draft
                # time_published > now: scheduled
                # time_published <= now: published
                if not a['time_published']:
                    a['status'] = ProblemStatus.draft
                else:
                    now = datetime.now()
                    # from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    published_date = parser.parse(a['time_published'])
                    # published_date = published_date.replace(tzinfo=from_zone)
                    local = published_date.astimezone(to_zone).replace(tzinfo=None)
                    if local < now:
                        a['status'] = ProblemStatus.published
                    else:
                        a['status'] = ProblemStatus.scheduled

            classroom.assignments = sorted(assignments, key=lambda x: x['name'])
            if get_all_problems:
                # classroom
                problems = self.get_problems([asm['id'] for asm in assignments])

        if get_students:
            url = 'https://repl.it/data/classrooms/{}/students'.format(classroom_id)
            # r = self.s.get(url, headers=headers)
            # students = r.json()
            # TODO
        if get_submissions:
            url = 'https://repl.it/data/classrooms/{}/submissions'.format(classroom_id)
            # r = self.s.get(url, headers=headers)
            # students = r.json()
            # TODO

        return classroom, problems

    def get_problems(self, problem_ids):
        """
        :param problem_ids: list of problem ids
        :return:
        """
        problems = []
        for id in problem_ids:
            problems.append(self.get_problem(id))
        return problems

    def get_problem(self, problem_id):
        url = 'https://repl.it/data/assignments/{}'.format(problem_id)
        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        print(r.text)

        raw = r.json()
        problem = self.parse_problem(raw)
        problem.statement_language = "vi"
        problem.src_name = "repl"
        problem.tags = ["basic"]
        problem.difficulty = 1.0
        return problem

    def get_testcases(self, problem_id):
        url = 'https://repl.it/data/assignments/{}/tests/'.format(problem_id)
        r = self.s.get(url, headers=self._headers)
        raw = r.json()
        print(raw)

        testcases = []
        for t in raw:
            testcase = self.parse_testcase(t)
            testcases.append(testcase)

        return testcases

    def get_solution(self, problem_id):
        url = 'https://repl.it/data/teacher/model_solutions/{}'.format(problem_id)
        r = self.s.get(url, headers=self._headers)
        raw = r.json()
        if 'editor_text' in raw:
            sol = raw['editor_text']
        else:
            sol = ''
        return sol

    def parse_problem(self, raw):
        exporter = HTML({
            'block_map': BLOCK_MAP,
            'style_map': STYLE_MAP,
            'entity_decorators': ENTITY_DECORATORS,
            'engine': ENGINE,
        })

        if not raw['instructions']:
            markdown = ''
        else:
            try:
                markdown = exporter.render(json.loads(raw['instructions']))
            except Exception:
                markdown = ""
                traceback.print_exc()

        problem = Problem()
        problem.statement = markdown

        if raw['feedback_mode'] == "input_output":
            problem.judge_mode = JudgeMode.oj
        elif raw['feedback_mode'] == "manual":
            problem.judge_mode = JudgeMode.manual
        else:
            problem.judge_mode = JudgeMode.unit_test

        problem.src_id = raw['id']
        problem.name = raw['name']
        problem.template = raw['editor_template']

        # print(markdown)

        problem.testcases = self.get_testcases(problem.src_id)
        # print(problem.testcases)

        if problem.testcases:
            problem.testcases_sample = problem.testcases[:1]

        problem.solution = self.get_solution(problem.src_id)
        return problem

    def parse_testcase(self, t):
        if t['matching_type'] == 'flexible':
            mt = MatchingType.flexible
        elif t['matching_type'] == 'strict':
            mt = MatchingType.strict
        else:
            mt = MatchingType.regexp
        testcase = TestCase(t['input'], t['output'], matchingtype=mt)
        testcase.src_id = t['id']
        return testcase


def read_all_classrooms():
    # user ThucNguyen1
    cookies = """_ga=GA1.2.1677725907.1574165625; ajs_anonymous_id=%22ffa18d4a-381b-4ef8-91c8-8b8512a84015%22; ajs_user_id=816683; ajs_anonymous_id=%22ffa18d4a-381b-4ef8-91c8-8b8512a84015%22; __stripe_mid=a7cc7f25-5676-4976-bfea-485c81fbb897cd1019; connect.sid=s%3A6U4N1bC3IoIImUzjVLQG75cnetABj5WC.ZIoDQ59W9VCy8DmznuF7nEgqYij%2B5keSPs%2F36OEjNeE; _gid=GA1.2.1495296026.1603513773; __cfduid=d9083e66152402ae6a57210e7b81bb6df1603513777; ajs_user_id=816683; _gat=1"""
    repl = ReplIt(cookies)
    # classroom, problems = repl.get_classroom(classroom_id=223285, get_assignments=True, get_all_problems=True)
    # repl.get_classroom_list()
    classroom_ids = [
        56776, 56777, 56778, 56779, 58619, 58669, 69942, 69959, 69962, 75548, 75549, 75550, 76159, 76160, 76798,
        # 76831, 78111, 78159, 78425, 78856, 79067, 79466, 79738, 80200, 80237, 80885, 80901, 80906, 80907, 80954,
        # 81723, 82556, 82591, 82633, 82638, 83229, 83939, 83940, 83942, 84007, 84474, 84524, 84839, 85275, 85300,
        # 85301, 85374, 85432, 87237, 87249, 87265, 90146, 93504, 93695, 95169, 97703, 97806, 99769, 99797, 100485,
        # 102813, 103932, 104222, 104248, 105430, 106618, 109172, 110078, 110082, 110430, 110441, 111047, 111127,
        # 111128, 112685, 114140, 115575, 115675, 115691, 120047, 120441, 120442, 120445, 120446, 120447, 120448,
        # 120449, 120450, 120451, 120452, 121299, 122108, 122119, 122120, 122557, 122648, 124930, 125959, 126009,
        # 126754, 126755, 127025, 128007, 128047, 128777, 129425, 129428, 129528, 129529, 131016, 131789, 131825,
        # 132927, 132961, 133159, 133160, 133161, 133162, 133163, 133164, 133165, 133166, 133167, 133168, 133908,
        # 133997, 134579, 135390, 136363, 136701, 137697, 137709, 137762, 137788, 138323, 138617, 139148, 139508,
        # 139551, 140651, 140726, 141150, 141644, 142548, 143142, 143159, 143868, 144520, 149236, 149470, 151448,
        # 153043, 154487, 154496, 154916, 155789, 156082, 156829, 156934, 156942, 158254, 158629, 159222, 160409,
        # 160410, 160417, 162661, 163361, 163981, 163993, 166274, 167259, 169524, 185273, 195746, 195747, 196544,
        # 198409, 199129, 199132, 200673, 202363, 202372, 205760, 205775, 207919, 209625, 210305, 210313, 210327,
        # 210341, 213097, 213212, 218542, 220578, 220729, 222655, 222673, 223263, 223285, 210324, 211581, 210443, 211149, 212842
    ]

    for classroom_id in classroom_ids:
        classroom, problems = repl.get_classroom(classroom_id=classroom_id, get_assignments=True, get_all_problems=True)
        print(classroom)

        classroom_folder = os.path.join("../../problems/_repl/ThucNguyen1", make_slug(classroom.name))
        if not os.path.exists(classroom_folder):
            os.mkdir(classroom_folder)
        for problem in sorted(problems, key=lambda p: p.name):
            ProblemService.save(problem, classroom_folder, overwrite=True)
            print(problem.name)


if __name__ == "__main__":
    read_all_classrooms()
    # print(classroom)
    # for assignment in classroom.assignments:
    #     print(assignment)

    # problem = repl.get_problem(5064610)
    # DsaProblem.save(problem, "../../problems/p1")


    # problem = repl.get_problem(2079412)
    # problem = repl.get_problem(2079413)
    # problem = repl.get_problem(2079416)
    # problem = repl.get_problem(2079417)

    # i = 1
    # for t in problem.testcases:
    #     print('#{}: '.format(i), t)
    #     i += 1

    # classroom = repl.get_classroom("85432")
    # print(classroom)
    # pprint.pprint(classroom.assignments)

    # test_create_problem()