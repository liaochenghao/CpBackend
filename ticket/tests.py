# coding: utf-8
A = 353192
i = 1
while A > 1:
    B = A * 0.0009
    balance = A - B
    print("""第 %s 天提出现金 %s 元, 剩余金额 %s 元""" % (str(i), str(B), str(balance)))
    A = balance
    i = i + 1

