# -*- coding: utf-8 -*-
"""ТВиМС 4 практическая работа.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1C_hy0sFsuhcekx2Gu3mAD1uQQDQYv4K1

# Заревич Михаил 513-2

Вариант 169

## Анализ выборки
"""

import pandas as pd
import scipy.stats
import statsmodels.graphics.gofplots
import matplotlib.pyplot as plt

# Уровни значимости Significance level
alphas = [0.005, 0.01, 0.05]

# Соответствующие им доверительные вероятноси Confidence level
gammas = [0.995, 0.99, 0.95]

# по умолчанию первая строчка csv файла записывается в заголовок колонки
# чтобы этого не было надо написать header = None
df = pd.read_csv("/content/v169.csv", header = None)

df = df.dropna() # убирает пропуски
df = df.sort_values(by = [0]).reset_index() # Сортировка значений
df = df.rename(columns={0: "Значения"})
df

# Значения разбросаны в диапазоне от -4.052622 до 4.055710.
# Диапазон можно разделить на 10 интервалов и посмотреть, сколько значений будет в каждом из них.
bins = pd.cut(df["Значения"], 10)
bins

df["Интервалы"] = bins
df

# Группировка значений по интервалам.
temp = df.groupby('Интервалы')

# Группированный статистический ряд абсолютных частот.
Series = temp.agg({'Интервалы': 'count'})

print(Series)

# Группированный статистический ряд абсолютных частот.
Series = Series.rename(columns={"Интервалы": "Количество значений, попавших в интервал"})
temp = df['Интервалы'].unique()
Series["Интервалы"] = temp

Series

import seaborn as sns

x1 = Series["Интервалы"]
y = Series["Количество значений, попавших в интервал"]
sns.barplot(x=x1, y=y)
plt.title("Группированный статистический ряд абсолютных частот.")
plt.show()

df['Значения'].plot(kind='hist', bins=20, title='Значения')
plt.gca().spines[['top', 'right',]].set_visible(False)

statsmodels.graphics.gofplots.qqplot(df["Значения"], scipy.stats.norm, line = "45")
plt.title("График квантиль-квантиль.")
plt.show()

print("Выборочное математическое ожидание: ", df["Значения"].mean())
print("Выборочная дисперсия: ", df["Значения"].var())
print("Выборочное ско: ", df["Значения"].std())
print("Выборочный коэффициент ассиметрии: ", df["Значения"].skew())
print("Выборочный эксцесс: ", df["Значения"].kurtosis())

"""**Вывод.**

На основани вида графика и значений выборочных параметров можно выдвинуть гипотезу - случайная величина имеет стандартное нормальное распределение.

## Проверка гипотезы по гитерию Шапиро-Уилка

Не знаю, как тут указать параметры, чтобы проверялось именно стандартное распределение, а не произвольное.
"""

scipy.stats.shapiro(df["Значения"])

"""**Вывод.**

Гипотеза принимается при всех заданных уровнях значимости.

## Проверка гипотезы по критерию Колмогорова-Смирнова
"""

KSTest = scipy.stats.kstest(df["Значения"] , "norm", args = (0, 1))
print("Наблюдаемое значение критерия: ", KSTest[0])
print("P-значение: ", KSTest[1])

"""Проверка через наблюдаемое значение критерия."""

print("Критические значения: ")
for i in gammas:
    print(scipy.stats.kstwo.ppf(i, len(df)))

"""**Вывод.**

Гипотезу можно принять при любом уровне значимости, так как наблюдаемое значение критерия меньше критического значения для всех уровней значимости.

P-значение больше всех уровней значимости, следовательно гипотезу можно принять при любом из них.

## Проверка гипотезы по критерию хи-квадрат

Зададим вероятности попадания в интервалы.
"""

# Normal distribution
# Нормальное распределение
NormDist = scipy.stats.norm()
ExpectedFrequencies = []

print("Вероятности: ")

for i in temp:
    # вероятность попадания в интервал.
    Pi = NormDist.cdf(i.right)- NormDist.cdf(i.left)
    print(Pi)
    ExpectedFrequencies.append(Pi*len(df))
print()
print("Частоты: ")
for i in ExpectedFrequencies:
    print(i)

print(scipy.stats.chisquare(Series["Количество значений, попавших в интервал"], ExpectedFrequencies, sum_check = False))

a = scipy.stats.chi2(len(df)-1)
for i in alphas:
    #print(scipy.stats.chi2.ppf(i, len(df)))
    print(a.ppf(i))

"""**Вывод.**

Гипотеза принимается при всех уровнях значимости.
"""