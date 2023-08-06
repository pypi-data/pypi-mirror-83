import copy
import html
import json
import pickle
import time

import requests
from hyper.contrib import HTTP20Adapter
import tomd
from bs4 import BeautifulSoup

from ptoolbox.helpers.clog import CLog
from ptoolbox.helpers.misc import base64_encode
from ptoolbox.models.general_models import Problem, TestCase


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


class VJudge:
    def __init__(self):
        self.s = requests.session()
        self._headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'origin': "https://vjudge.net",
        }
        self.csrf = ''

    def login(self, username, password):
        headers = copy.deepcopy(self._headers)
        payload = {
            "username": username,
            "password": password
        }

        headers = copy.deepcopy(self._headers)
        r = self.s.post("https://vjudge.net/user/login", data=payload, headers=headers)
        print("login status code:", r.status_code)
        print("req headers:", headers)
        print(r.text)

    def get_problem(self, problem_url):
        headers = copy.deepcopy(self._headers)
        r = self.s.get(problem_url, headers=headers)
        print("get problem status code:", r.status_code)
        print(r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        meta = soup.findAll("textarea", attrs={'name': "dataJson"})[0]
        meta_json = json.loads(meta.decode_contents())
        print(json.dumps(meta_json))
        problem_title_tag = soup.select("div#prob-title")[0]
        problem_title = problem_title_tag.select("h2")[0].decode_contents()
        origin_url_tag = problem_title_tag.findAll("span", attrs={'class': "origin"})[0].select("a")[0]
        problem_tag = soup.select("iframe#frame-description")[0]
        problem_desc_url = "https://vjudge.net" + problem_tag['src']
        print(origin_url_tag['href'])
        print(problem_title)
        print(problem_desc_url)

        sumbit_button = soup.select("button#btn-submit")[0]
        data_oj = sumbit_button['data-oj']
        data_problem_num = sumbit_button['data-prob-num']
        print(data_oj, data_problem_num)
        return data_oj, data_problem_num

    def sumbit(self, oj, problem_num, source_code, language):
        languages = {
            "2": "Microsoft Visual C++ 2010",
            "3": "Delphi 7",
            "4": "Free Pascal 3.0.2",
            "6": "PHP 7.2.13",
            "7": "Python 2.7.15",
            "8": "Ruby 2.7.1",
            "9": "C# Mono 6.8",
            "12": "Haskell GHC 8.10.1",
            "13": "Perl 5.20.1",
            "19": "OCaml 4.02.1",
            "20": "Scala 2.12.8",
            "28": "D DMD32 v2.091.0",
            "31": "Python 3.7.2",
            "32": "Go 1.15.2",
            "34": "JavaScript V8 4.8.0",
            "36": "Java 1.8.0_241",
            "40": "PyPy 2.7 (7.2.0)",
            "41": "PyPy 3.6 (7.2.0)",
            "42": "GNU G++11 5.1.0",
            "43": "GNU GCC C11 5.1.0",
            "48": "Kotlin 1.4.0",
            "49": "Rust 1.42.0",
            "50": "GNU G++14 6.4.0",
            "51": "PascalABC.NET 3.4.2",
            "52": "Clang++17 Diagnostics",
            "54": "GNU G++17 7.3.0",
            "55": "Node.js 12.6.3",
            "59": "Microsoft Visual C++ 2017",
            "60": "Java 11.0.6",
            "61": "GNU G++17 9.2.0 (64 bit, msys 2)",
            "65": "C# 8, .NET Core 3.1"
        }

        payload = {
            "language": language,
            "share": 0,
            "source": base64_encode(source_code),
            "captcha": "",
            "oj": oj,
            "probNum": problem_num
        }

        headers = copy.deepcopy(self._headers)
        r = self.s.post("https://vjudge.net/problem/submit", data=payload, headers=headers)
        print("submit status code:", r.status_code)
        print("req headers:", headers)
        print(r.text)
        res = json.loads(r.text)
        if not res.get("runId"):
            return None, res
        return res["runId"], res

    def get_run_id_result(self, run_id, retry=15, interval=1.0):
        """
        response["status"]: pending, Submitted, ...
        response["processing"]: true, false
        sample respons:
        {
            "code": "# add this for enough number of characters, if not enough, add even more\nprint(\"YES\")",
            "statusType": 1,
            "author": "thucnguyen85",
            "length": 85,
            "runtime": 93,
            "language": "Python 3.7.2",
            "statusCanonical": "WA",
            "authorId": 208169,
            "languageCanonical": "PYTHON",
            "submitTime": 1602383084000,
            "isOpen": 1,
            "processing": false,
            "runId": 27704024,
            "oj": "CodeForces",
            "remoteRunId": "95166951",
            "probNum": "785A",
            "status": "Wrong answer on test 1"
        }
        :param run_id:
        :return:
        """
        url = f"https://vjudge.net/solution/data/{run_id}"
        headers = copy.deepcopy(self._headers)
        res = None
        for i in range(retry):
            r = self.s.post(url, headers=headers)
            # print(r.text)
            res = json.loads(r.text)
            print(json.dumps(res))
            processing = res['processing']
            if not processing:
                break
            time.sleep(interval)
        return res


if __name__ == '__main__':
    vj = VJudge()
    vj.login("thucnguyen85", "15041985")
    # problem_url = "https://vjudge.net/problem/CodeForces-344A"
    problem_url = "https://vjudge.net/problem/CodeForces-785A"
    data_oj, data_probcode = vj.get_problem(problem_url)
    source_code="""# add this for enough number of characters, if not enough, add even more 12
print("YES")"""
    run_id, res = vj.sumbit(oj=data_oj, problem_num=data_probcode, language=31, source_code=source_code)
    if run_id:
        print(run_id)
        res = vj.get_run_id_result(run_id)
        print("final result:", res)
    else:
        print("ERROR:", res)