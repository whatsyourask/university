import numpy as np
import matplotlib.pyplot as plt

# Классификатор
def classifier(heights, t):
    class_out = []
    for height in heights.flat:
        if height > t:
            class_out.append(1)
        if height < t:
            class_out.append(0)
    return np.array(class_out)

# Рассчёт TruePositive TrueNegative FalsePositive FalseNegative
def tp_tn_fp_fn(basket_class, basketball_flags,
        foot_class, football_flags):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for ind in range(len(basket_class)):
        tp += 1 if (basketball_flags[ind] == 1 and
                basket_class[ind] == 1) else 0
        tn += 1 if (football_flags[ind] == 0 and
                foot_class[ind] == 0) else 0
        fp += 1 if (football_flags[ind] == 0 and
                foot_class[ind] == 1) else 0
        fn += 1 if (basketball_flags[ind] == 1 and
                basket_class[ind] == 0) else 0
    return tp, tn, fp, fn

# Рассчёт accuracy
def accuracy(tp, tn, count):
    return (tp + tn) / count

# Рассчёт precision
def precision(tp, fp):
    return 1 if (tp == 0 and fp == 0) else tp / (tp + fp)

# Рассчёт recall
def recall(tp, fn):
    return tp / (tp + fn)

# Рассчёт F1_score
def f1_score(pr, rec):
    return 2 * (pr * rec) / (pr + rec)

# Рассчёт ошибка 1 рода
def alpha(fp, tn):
    return fp / (tn + fp)

# Рассчёт ошибки 2 рода
def beta(fn, tp):
    return fn / (tp + fn)

# Вычисление всех метрик для порога t
# Если cycle не задан, то вывести информацию о метриках
def calculate_all_metrics(t, basketball, basketball_flags,
        football, football_flags, count, cycle=0): 
    basket_class = classifier(basketball, t)
    foot_class = classifier(football, t)
    tp, tn, fp, fn = tp_tn_fp_fn(basket_class, basketball_flags,
            foot_class, football_flags)
    ac = accuracy(tp, tn, count)
    pr = precision(tp, fp)
    rec = recall(tp, fn)
    f1 = f1_score(pr, rec)
    alp = alpha(fp, tn)
    bet = beta(fn, tp)
    if cycle == 0:
        print(f"tp = {tp}\ntn = {tn}\nfp = {fp}\nfn = {fn}")
        print(f"accuracy = {ac}\nprecision = {pr}\nrecall = {rec}\n"
            f"f1_score = {f1}\nalpha = {alp}\nbeta = {bet}")
    return rec, alp, ac
    
# Рисование линии и вычисление метрик при максимальной accuracy
def draw_roc(thresholds, basketball, basketball_flags,
        football, football_flags, count):
    recs, alps = [], []
    max_ac = 0
    max_threshold = 0
    for threshold in thresholds:
        rec, alp, ac = calculate_all_metrics(threshold, basketball,
                basketball_flags, football,
                football_flags, count, 1)
        recs.append(rec)
        alps.append(alp)
        if ac > max_ac:
            max_ac = ac
            max_threshold = threshold
    print(f"max accuracy = {max_ac} max threshold = {max_threshold}")
    calculate_all_metrics(max_threshold, basketball, basketball_flags,
            football, football_flags, count)
    # Привести к numpy.ndarray
    recs = np.array(recs)
    alps = np.array(alps)
    fig, ax = plt.subplots()
    ax.plot(alps, recs)
    plt.show()
    return recs, alps
   
# Рассчёт площади под кривой
def calculate_auc(recs, alps):
    auc = 0
    for ind in range(len(recs)-1):
        auc += abs(alps[ind] - alps[ind+1])*(recs[ind] + recs[ind + 1]) / 2
    print(f"AUC = {auc}")


def complete_task():
    count = 1000
    # Задать сигму и мю для баскетболистов
    # и сгенерировать данные в количестве count
    basket_sigma = 7
    basket_mu = 193
    basketball = basket_sigma * np.random.randn(1, count) + basket_mu
    # Массив меток с единицами(С1)
    basketball_flags = np.ones(count)
    # Аналогично, баскетболистам задать
    # и сгененировать данные
    foot_sigma = 6
    foot_mu = 180
    football = foot_sigma * np.random.randn(1, count) + foot_mu
    # Массив меток с нулями(С0)
    football_flags = np.zeros(count)
    # Задать порог для одного случая
    t = 187
    # Вычислить все метрики для этого случая
    calculate_all_metrics(t, basketball, basketball_flags,
            football, football_flags, count)
    # Сгенерировать вектор порогов
    thresholds = np.linspace(1, 300, 300)
    # Нарисовать кривую и вернуть recalls & alphas для вычисления площади под кривой
    recs, alps = draw_roc(thresholds, basketball, basketball_flags,
            football, football_flags, count)
    # Вычислить площадь под кривой
    calculate_auc(recs, alps)


complete_task()
