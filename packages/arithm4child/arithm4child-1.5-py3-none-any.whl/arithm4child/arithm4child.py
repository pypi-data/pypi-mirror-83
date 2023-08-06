#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import random
import pyttsx3
import argparse

engine = pyttsx3.init()
rightStr = "正确"
wrongStr = "错误"

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--number", type=int,
                    help="题数")
parser.add_argument("-m", "--max", type=int,
                    help="最大数值")
parser.add_argument("-v", "--voice", action="store_true",
                    help="发出声音")
parser.add_argument("-l", "--lang",help="设置语言")
args = parser.parse_args()

lang = 'zh'
minInt = 1
maxInt = 8
N = 5
hasVoice = False

if args.number:
    N = args.number
if args.lang:
    lang = args.lang
if args.max:
    maxInt = args.max
if args.voice:
    hasVoice = args.voice

correctTime = 0

for i in range(N):

    a = random.randint(minInt, maxInt)
    b = random.randint(minInt, maxInt)
    print('-' * 10)
    print("第{}题：".format(i+1))
    titleStr = "第{}题，{}+{}=多少？".format(i+1, a, b)
    if hasVoice:
        engine.say(titleStr)
        engine.runAndWait()

    titleStr2 = '    {}+{}=?\n'.format(a, b)
    c = None
    while True:
        try:
            cStr = input(titleStr2)
            if cStr.startswith('?'):
                rightAnsStr = "正确答案是{}".format(a+b)
                print(rightAnsStr)
                if hasVoice:
                    engine.say(rightAnsStr)
                    engine.runAndWait()
                break
            c = int(cStr)
            break
        except ValueError:
            print("请输入数字:")
            if hasVoice:
                engine.say("请输入数字")
                engine.runAndWait()

    if c:
        if c == (a+b):
            print(rightStr)
            if hasVoice:
                engine.say(rightStr)
                engine.runAndWait()
            correctTime = correctTime + 1
        else:
            print(wrongStr)
            if hasVoice:
                engine.say(wrongStr)
                engine.runAndWait()


print('-' * 10)
finalStr = "一共{}道题，做对{}道题，总分{}分。".format(N,
	 				correctTime, correctTime / N * 100)
print(finalStr)
if hasVoice:
    engine.say(finalStr)
    engine.runAndWait()