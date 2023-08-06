# coding=utf-8
import json
import logging

__author__ = 'ThucNC'

import os

from ptoolbox.dsa.dsa_problem import DsaProblem
from ptoolbox.ucode.ucode import UCode

_logger = logging.getLogger(__name__)


def add_chapters_to_course(chapters, ucode, course_id, base_ucoin=100):
    base_path = "/home/thuc/projects/ucode/weekly-algorithm-problems/"
    for i, chapter in enumerate(chapters):
        is_free = i < 1
        print(f"chapter {i}:", chapter)
        chapter_name = "Training %02d" % i
        if i < 1:
            chapter_name = "[Học thử miễn phí] " + chapter_name
        chapter_id = ucode.create_chapter(course_id=course_id,
                                          chapter_name=chapter_name,
                                          status="published", is_free=is_free)
        lesson_id = ucode.create_lesson_item(course_id=course_id, chapter_id=chapter_id,
                                             lesson_name=chapter_name + " - Đề bài",
                                             type="quiz", status="published", is_free=is_free)
        for i, prob in enumerate(chapter['problem']):
            path = os.path.join(base_path, prob['path'] )
            print(path)
            trans = []
            langs = prob.get("lang")
            if langs and "vi" in langs:
                trans = ['vi']
            problem = DsaProblem.load(path, translations=trans, load_testcase=True)
            problem.tags = None
            print(type(problem))
            ucode.create_problem(lesson_id=lesson_id, problem=problem, lang='en',
                                 status="published", question_type='code', xp=i*50+base_ucoin)
        for i, video in enumerate(chapter['video']):
            lesson_id = ucode.create_lesson_item(course_id=course_id, chapter_id=chapter_id,
                                                 lesson_name="[Chữa bài] " + video['name'] ,
                                                 type="video", status="published",
                                                 video_url=video['url'], is_free=is_free)
        # break


def math_coding_mc1(ucode, course_id):
    with open("/home/thuc/projects/ucode/weekly-algorithm-problems/courses/mc1_course_list.json") as syllabus_file:
        syllabus = json.load(syllabus_file)
        print(syllabus)
        add_chapters_to_course(syllabus, ucode, course_id)


def math_coding_mc2(ucode, course_id, base_ucoin=200):
    with open("/home/thuc/projects/ucode/weekly-algorithm-problems/courses/mc2_course_list.json") as syllabus_file:
        syllabus = json.load(syllabus_file)
        print(syllabus)
        add_chapters_to_course(syllabus, ucode, course_id, base_ucoin=base_ucoin)


if __name__ == "__main__":
    ucode = UCode("https://dev-api.ucode.vn/api", "b1f3bba4df8c50713ee39d9f75647739")
    # course_id = 12

    # math_coding_mc1(ucode, 12)
    math_coding_mc2(ucode, 13)
