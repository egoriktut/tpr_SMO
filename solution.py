from enum import Enum
import random
import numpy as np


class KeysSMO(Enum):
    """
    Ключи для одноканальные СМО с ожиданием
    """

    mu = "Интенсивность обслуживания"
    po = "Приведенная интенсивность потока"
    P = "Предельные вероятности системы"
    P_rej = "Вероятность отказа в обслуживании"
    q = "Относительная пропускная способность"
    A = "Абсолютная пропускная способность"
    r_mid = "Среднее число заявок, находящихся в очереди"
    w_mid = "Среднее число заявок, находящихся под обслуживанием"
    k_mid = "Среднее число заявок, находящихся в системе"
    T_sys = "Среднее время пребывания заявки в системе"
    T_aw = "Средняя продолжительность пребывания заявки в очереди"
    A_nom = "Номинальную пропускную способность системы"
    nom = "Отношение номинальной пропускной способности к фактической"


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
        self.result.append(f"В среднем: {obsl / (k / 60)}")

    def solve(self):
        self.map["mu"] = 1 / self.t
        self.map["q"] = P_0 = self.map["mu"] / (self.map["mu"] + self.l)
        self.map["A"] = self.l * self.map["q"]
        self.map["P_rej"] = P_1 = 1 - P_0
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

    def fac(self, n):
        if n == 1 or n == 0:
            return 1
        return n * self.fac(n - 1)

    def solve(self):
        self.map["mu"] = 1 / self.t
        self.map["po"] = self.l / self.map["mu"]
        self.map["P"].append(
            1 / sum([(self.map["po"] ** k) / self.fac(k) for k in range(self.n + 1)])
        )
        for i in range(1, self.n + 1):
            self.map["P"].append(
                (self.map["po"] ** i) * self.map["P"][0] / self.fac(i)
            )
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
            P_0 = 1 / sum([(self.map["po"] ** k) / self.fac(k) for k in range(n + 1)])
            P_rej = self.map["po"] ** n / self.fac(n) * P_0
            self.result.append(f"n: {n}; P0: {round(P_0 * 100, 3)}%; P отказа: {round(P_rej * 100, 3)}%")
            n += 1

# sol = SolutionSMOMultiReject([1.8, 1, 3])
# sol.solve()
# print(sol.result)
