import math
import random
import tqdm

# ========================
# 1. 正規乱数を生成する関数
#    (平均 mean, 標準偏差 sd)
# ========================
def normal_int(mean, sd):
    # random.gauss(平均, 標準偏差) で浮動小数の正規乱数を生成し、整数に丸める
    return int(round(random.gauss(mean, sd)))

# ========================
# 2. 野菜1つ分の価格を求める関数
#    vegetable: 0=キュウリ, 1=トマト, 2=ナス
# ========================
def get_price(vegetable):
    if vegetable == 0:  # キュウリ
        w = normal_int(100, 20)
        # 規格判定
        if 51 <= w <= 80:
            return 30  # S
        elif 81 <= w <= 120:
            return 60  # M
        elif 121 <= w <= 150:
            return 60  # L
        else:
            return 0   # 規格外
    elif vegetable == 1:  # トマト
        w = normal_int(150, 15)
        if 101 <= w <= 135:
            return 50  # S
        elif 136 <= w <= 165:
            return 100 # M
        elif 166 <= w <= 200:
            return 150 # L
        else:
            return 10  # 規格外
    else:  # ナス (2)
        w = normal_int(180, 18)
        if 161 <= w <= 200:
            return 120 # M
        elif 201 <= w <= 240:
            return 180 # L
        else:
            return 0   # 規格外

# ========================
# 3. 1袋をシミュレート
#    上限 L を与え、袋に入る (C, T, E) を返す
# ========================
def simulate_one_bag(L):
    total_price = 0
    count_items = 0
    c = t = e = 0  # それぞれキュウリ、トマト、ナスの個数カウント
    
    while True:
        if count_items >= 20:
            # 20個に到達したら終了
            break
        
        # 野菜の種類を 4:3:3 の比率で選ぶ
        # 例えば random.random() を使い、0〜1の一様乱数から選ぶ方法
        r = random.random()
        if r < 0.4:
            veg_type = 0  # キュウリ
        elif r < 0.7:
            veg_type = 1  # トマト
        else:
            veg_type = 2  # ナス
        
        price = get_price(veg_type)
        # 上限を超えるかチェック
        if total_price + price > L:
            # 超えるなら入れずに終了
            break
        
        # 入れる
        total_price += price
        count_items += 1
        if veg_type == 0:
            c += 1
        elif veg_type == 1:
            t += 1
        else:
            e += 1
    
    return (c, t, e)

# ========================
# 4. 10袋まとめてシミュレートして結果を返す
# ========================
def simulate_10_bags(L):
    bags = []
    for _ in range(10):
        bags.append(simulate_one_bag(L))
    return bags

# ========================
# 5. 誤差(スコア)計算関数 (例: 二乗誤差の合計)
#    - 実際データ actual_bags と
#      シミュ結果 sim_bags は [(C1,T1,E1),..., (C10,T10,E10)] の形
# ========================
def score_bags(actual_bags, sim_bags):
    score = 0
    for (ac, at, ae), (sc, st, se) in zip(actual_bags, sim_bags):
        score += (ac - sc)**2 + (at - st)**2 + (ae - se)**2
    return score

# ========================
# メイン (例)
# ========================
def main():
    import sys
    input_data = sys.stdin.read().strip().split()
    # 実際の入力 (10行 x 3列)
    # C_i, T_i, E_i
    actual_bags = []
    for i in range(10):
        Ci = int(input_data[3*i])
        Ti = int(input_data[3*i + 1])
        Ei = int(input_data[3*i + 2])
        actual_bags.append((Ci, Ti, Ei))
    
    # 乱数シードを固定する場合（再現用）
    random.seed(0)
    
    best_L = 500
    best_score = float('inf')
    
    # 単純に 500〜5000 の範囲を総当たり (1刻み)
    # 計算コストが重い場合はステップを大きくして段階的に絞るなど工夫する
    for L in tqdm.tqdm(range(500, 5001)):
        # シミュレーション回数が少ないと誤差が大きくブレやすいので、
        # 各Lで複数回(例: 1〜3回など)シミュレートし平均スコアを使うなどしてもよい
        # 例: 各Lに対して 3回シミュレートして平均スコアをとる
        times = 3
        total_score = 0
        for _ in range(times):
          sim_bags_10 = simulate_10_bags(L)
          total_score += score_bags(actual_bags, sim_bags_10)
        sc = total_score / times
        if sc < best_score:
            best_score = sc
            best_L = L
    
    print(best_L)

if __name__ == '__main__':
    main()
