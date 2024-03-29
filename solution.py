from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import base64
import os

def fac(n):
    if n == 1 or n == 0:
        return 1
    return n * fac(n - 1)


class KeysSMO(Enum):
    """
    Ключи для одноканальные СМО с ожиданием
    """

    mu = "μ (Интенсивность обслуживания)"
    po = "ρ (Приведенная интенсивность потока)"
    P = "Предельные вероятности системы P"
    P_rej = "P отказа (Вероятность отказа в обслуживании)"
    q = "q (Относительная пропускная способность)"
    A = "A (Абсолютная пропускная способность)"
    r_mid = "r среднее (Среднее число заявок, находящихся в очереди)"
    w_mid = "w среднее (Среднее число заявок, находящихся под обслуживанием)"
    k_mid = "к среднее (Среднее число заявок, находящихся в системе)"
    T_sys = "T системное (Среднее время пребывания заявки в системе)"
    T_aw = "Т ожидания (Средняя продолжительность пребывания заявки в очереди)"
    A_nom = "А номинальное (Номинальную пропускную способность системы)"
    nom = "Nom (Отношение номинальной пропускной способности к фактической)"
    P_no_q = "P от.оч (Вероятность отсутствия очереди)"

def draw_multi_reject(n, k):
    image = Image.open('smo_multi_reject_template.png')
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.text(1018, 82, f'{n}', fontsize=8, color='black')
    plt.savefig('smo_multi_reject.png')
    result = ""
    with open("smo_multi_reject.png", "rb") as file:
        img = file.read()
        result = f"data:image/png;base64,{base64.b64encode(img).decode('utf-8')}"
    os.remove("smo_multi_reject.png")
    return result


def draw_multi_await(n, m):
    image = Image.open('smo_multi_await_template.png')
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.text(555, 82, f'{n}', fontsize=8, color='black')
    ax.text(757, 82, f'{n}+{m}', fontsize=8, color='black')
    plt.savefig('smo_multi_await.png')
    result = ""
    with open("smo_multi_await.png", "rb") as file:
        img = file.read()
        result = f"data:image/png;base64,{base64.b64encode(img).decode('utf-8')}"
    os.remove("smo_multi_await.png")
    return result

def draw_multi_await_inf(n, m):
    image = Image.open('smo_multi_await_inf_template.png')
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.text(532, 60, f'{n}', fontsize=8, color='black')
    ax.text(720, 70, f'{n}+{m}', fontsize=7, color='black')
    plt.savefig('smo_multi_await_inf.png')
    result = ""
    with open("smo_multi_await_inf.png", "rb") as file:
        img = file.read()
        result = f"data:image/png;base64,{base64.b64encode(img).decode('utf-8')}"
    os.remove("smo_multi_await_inf.png")
    return result
    

def reformat_result(current_map):
    """
    Преобразование для отдачи данных
    """
    result = []
    for key, value in current_map.items():
        if key != "P" and key != "P_rej":
            result.append(f"{KeysSMO[key].value}: {round(value, 3)}")
        elif key == "P_rej":
            result.append(f"{KeysSMO[key].value}: {value}")
        else:
            for p in range(len(value)):
                result.append(f"{KeysSMO.P.value} {p}: {value[p]}")
    return result


class SolutionSMO1Await:
    """
    Одноканальные СМО с ожиданием
    """

    def __init__(self, params) -> None:
        self.t = params[0]
        self.l = params[1]
        self.m = params[2]
        self.map = {
            "mu": 1 / self.t,
            "P": [],
        }
        self.result = []

    def solve(self):
        self.map["po"] = self.l / self.map["mu"]
        po = self.map["po"]

        self.map["P"].append((1 - po) / (1 - po ** (self.m + 2)))
        for i in range(1, self.m + 2):
            self.map["P"].append((po**i) * self.map["P"][0])

        self.map["P_rej"] = self.map["P"][self.m + 1]
        self.map["q"] = 1 - self.map["P_rej"]
        self.map["A"] = self.l * self.map["q"]

        # TODO: Сказать что там ошибка в расчетах!!
        self.map["r_mid"] = (
            (po**2) * (1 - (po**self.m) * (self.m + 1 - self.m * po))
        ) / ((1 - po ** (self.m + 2)) * (1 - po))

        self.map["w_mid"] = (po - po ** (self.m + 2)) / (1 - po ** (self.m + 2))
        self.map["k_mid"] = self.map["r_mid"] + self.map["w_mid"]
        self.map["T_sys"] = self.l / self.map["mu"]
        self.map["T_aw"] = self.map["r_mid"] / self.l
        self.map["T_sys"] = self.map["T_aw"] + self.t

        # Приведение к процентам
        for i in range(len(self.map["P"])):
            self.map["P"][i] = f"{round(self.map['P'][i] * 100, 3)}%"
        self.map["P_rej"] = f"{round(self.map['P_rej'] * 100, 3) }%"

        self.result = reformat_result(self.map)


# sol = SolutionSMO1Await([1.05, 0.85, 3])
# sol.solve()
# print(sol.result)


class SolutionSMO1Reject:
    """
    Одноканальные СМО с отказами
    """

    def __init__(self, params) -> None:
        self.t = params[0]
        self.l = params[1]
        self.k = params[2]
        self.map = dict()
        self.result = []

    def simulate_process(self, k):
        post = 0
        otk = 0
        obsl = 0
        k1 = 0
        t_okon = 0
        rn_post = random.randint(1, 60)

        for _ in range(1, k + 1):
            k1 = random.randint(1, rn_post)

            if k1 == 1 and t_okon == 0:
                post += 1
                t_okon = np.random.poisson(108)
                obsl += 1

            if k1 == 1 and t_okon > 0:
                post += 1
                t_okon -= 1
                otk += 1

            if k1 > 1 and t_okon > 0:
                t_okon -= 1

        self.result.append(f"Поступило: {post}")
        self.result.append(f"Обслужено: {obsl}")
        self.result.append(f"Отказано: {otk}")
        self.result.append(f"В среднем: {round(obsl / (k / 60), 3)}")

    def solve(self):
        self.map["mu"] = 1 / self.t
        self.map["q"] = P_0 = self.map["mu"] / (self.map["mu"] + self.l)
        self.map["A"] = self.l * self.map["q"]
        self.map["P_rej"] = P_1 = 1 - P_0
        self.map["P_rej"] = round(self.map["P_rej"], 3)
        self.map["A_nom"] = 1 / self.t
        self.map["nom"] = self.map["A_nom"] / self.map["A"]
        self.result = reformat_result(self.map)
        self.simulate_process(self.k)


# sol = SolutionSMO1Reject([1.8, 1, 3])
# sol.solve()
# print(sol.result)


class SolutionSMOMultiReject:
    """
    Многоканальная СМО с отказами
    """

    def __init__(self, params) -> None:
        self.t = params[0]
        self.l = params[1]
        self.n = params[2]
        self.map = {"P": []}
        self.result = []
        self.img = ""

    def solve(self):
        self.map["mu"] = 1 / self.t
        self.map["po"] = self.l / self.map["mu"]
        self.map["P"].append(
            1 / sum([(self.map["po"] ** k) / fac(k) for k in range(self.n + 1)])
        )
        for i in range(1, self.n + 1):
            self.map["P"].append((self.map["po"] ** i) * self.map["P"][0] / fac(i))
        self.map["P_rej"] = self.map["P"][-1]
        P_rej = self.map["P_rej"]
        P_0 = self.map["P"][0]

        for i in range(len(self.map["P"])):
            self.map["P"][i] = f"{round(self.map['P'][i] * 100, 3)}%"
        self.map["P_rej"] = f"{round(self.map['P_rej'] * 100, 3) }%"

        self.map["q"] = 1 - P_rej
        self.map["A"] = self.l * self.map["q"]
        self.map["k_mid"] = self.map["po"] * (1 - P_rej)
        self.result = reformat_result(self.map)
        n = 1
        while P_rej > 0.01:
            P_0 = 1 / sum([(self.map["po"] ** k) / fac(k) for k in range(n + 1)])
            P_rej = self.map["po"] ** n / fac(n) * P_0
            self.result.append(
                f"n: {n}; P0: {round(P_0 * 100, 3)}%; P отказа: {round(P_rej * 100, 3)}%"
            )
            n += 1
        self.img = draw_multi_reject(self.n, self.map["k_mid"])

# sol = SolutionSMOMultiReject([1.8, 1, 3])
# sol.solve()
# print(sol.result)


class SolutionSMOMultiAwait:
    """
    Многоканальные СМО с ожиданием
    """

    def __init__(self, params) -> None:
        self.t = params[0]
        self.l = params[1]
        self.n = params[2]
        self.m = params[3]
        self.is_inf = params[4]
        self.map = {"P": [], "P_rej": 0, "q": 1, "A": self.l}
        self.result = []
        self.img = ""

    def solve(self):
        self.map["mu"] = 1 / self.t
        self.map["po"] = self.l / self.map["mu"]
        if self.is_inf:
            self.m = 500  # инфинити епт
            self.map["P"].append(round(
                1
                / (
                    sum([self.map["po"] ** i / fac(i) for i in range(self.n + 1)]) + 
                    (self.map["po"] ** (self.n + 1)) / (fac(self.n) * (self.n - self.map["po"]))
                ), 3)
            )
        else:
            self.m = int(self.m)
            self.map["P"].append(
                round(1
                / (
                    sum([self.map["po"] ** k / fac(k) for k in range(self.n + 1)]) + 
                    self.map["po"] ** self.n / fac(self.n) +
                    sum([self.map["po"] ** s / self.n ** s for s in range(1, self.m + 1)])
                ), 3)
            )
        for i in range(1, self.n + 2):
            p_i = self.map["po"] ** i * self.map["P"][0] / fac(i)
            self.map["P"].append(round(p_i, 3))
        self.map["P_no_q"] = sum(self.map["P"]) - self.map["P"][-1]
        x = self.map["po"] / self.n
        self.map["r_mid"] = (
            (
                self.map["po"] ** self.n
                * self.map["P"][0]
                / (self.n * fac(self.n))
            )
            * (1 - (self.m + 1) * x**self.m + self.m * x ** (self.m + 1))
            / (1 - x) ** 2
        )

        self.map["k_mid"] = (
            self.map["po"]
            * (
                1
                - self.map["P"][0]
                * self.map["po"] ** (self.n + self.m)
                / self.n**self.m
                / fac(self.n)
            )
            + self.map["r_mid"]
        )
        self.map["T_aw"] = self.map["r_mid"] / self.l
        self.map["T_sys"] = self.map["T_aw"] + self.t
        self.result = reformat_result(self.map)
        if self.is_inf:
            self.img = draw_multi_await_inf(self.n, self.m)
        else:
            self.img = draw_multi_await(self.n, self.m)



# sol = SolutionSMOMultiAwait([0.5, 2.5, 3, 500, True])
# sol.solve()
# print(*sol.result, sep="\n")
# p = 1.25
# print(1 / (1 + p + p**2 / 2 + p**3 / 6 + p**4 / (6 * 1.75)))

