# 导入随机和时间库
from random import *
from time import *


# 逻辑池处理函数
def monster_analyze(logic_pool: list, true_bullets: int, false_bullets: int):
    if false_bullets < true_bullets:
        logic_pool.append(True)

    elif false_bullets > true_bullets:
        logic_pool.append(False)

    elif false_bullets == true_bullets:
        logic_pool.append(choice([True, False]))


# 处理最佳成绩的函数
def max_times(array):
    try:
        biggest = int(array[0])
    except IndexError:
        return 0
    for i in array:
        if int(i) > biggest:
            biggest = int(i)
    return biggest


# 游戏基本属性
equipment = ['knife', 'beer', 'magnify', 'smoke', 'lock']
page_life = [2, 4, 6]
times = 0
score = 0
while times <= 2:
    people_life = page_life[times]
    monster_life = page_life[times]
    human_bag = []
    monster_bag = []
    gun_bullets = []
    human_hurt = 1
    monster_hurt = 1
    monster_turn = False
    human_turn = True
    monster_getLock = False
    human_getLock = False
    while monster_life > 0:
        monster_logical_pool = []
        # 基本设置
        bullets_times = randint(2, 8)  # 随机子弹数量
        if people_life <= 0:  # 判断若玩家生命小于或等于0
            print("游戏结束")
            times = 100
            break

        # 填入子弹
        if len(gun_bullets) == 0:
            human_bag.clear()  # 清空背包
            monster_bag.clear()  # 清空背包
            human_turn = True
            monster_turn = False
            print("我会把他们以不同的顺序装填")
            for i in range(1, bullets_times + 1):
                gun_bullets.append(choice([True, False]))
                print("{}".format(i), flush=False, end="")
                print("....", flush=False)
                sleep(1)

            # 分发装备
            if times >= 1:
                if len(human_bag) <= 8:
                    for i in range(people_life):
                        human_bag.append(choice(equipment))

                if len(monster_bag) <= 8:
                    for i in range(monster_life):
                        monster_bag.append(choice(equipment))

            # 处理所有子弹相同
            if bullets_times != 1:
                if gun_bullets.count(False) == bullets_times:
                    gun_bullets[randint(0, bullets_times - 1)] = True

                elif gun_bullets.count(True) == bullets_times:
                    gun_bullets[randint(0, bullets_times - 1)] = False

            print("所有类型的子弹:{}".format(gun_bullets))
            shuffle(gun_bullets)

        # 用于处理怪物逻辑判断的数据
        true_bullets_times = gun_bullets.count(True)
        false_bullets_times = gun_bullets.count(False)

        # 怪物逻辑池
        monster_analyze(monster_logical_pool, true_bullets_times, false_bullets_times)

        # tell condition
        print(
            "你的生命:{} 敌人的生命:{}\n你的物品:{} 敌方的物品:{}".format(people_life, monster_life, human_bag,
                                                                          monster_bag))

        # print("对面的逻辑池:{}".format(monster_logical_pool))

        # 人类回合
        if human_turn:
            human_choice = str(input("行动吧\n"))
            print("")
            if human_choice == "shoot_myself" or human_choice == "自己":
                if gun_bullets[0] is True:
                    people_life -= human_hurt
                    true_bullets_times -= 1
                    if monster_getLock is False:
                        human_turn = False
                        monster_turn = True

                else:
                    false_bullets_times -= 1
                    score += 20000
                gun_bullets.remove(gun_bullets[0])

            elif human_choice == "shoot_dealer" or human_choice == "对面":
                if gun_bullets[0]:
                    monster_life -= human_hurt
                    true_bullets_times -= 1
                    score += 10000
                    print("啊!这还挺痛的呢呵呵呵")
                    sleep(1)

                else:
                    false_bullets_times -= 1
                gun_bullets.remove(gun_bullets[0])

                # 回合结束,判断怪物是否被锁
                if monster_getLock is False:
                    monster_turn = True
                    human_turn = False

                # 若是,则将怪物的被锁状态设置为False.接着由于怪物的回合没有被设置为True,所以玩家获得一个回合
                else:
                    monster_getLock = False
                human_hurt = 1  # 重置玩家伤害

            # 使用刀
            elif human_choice == "knife" or human_choice == "酒" or human_choice == "刀":
                if 'knife' in human_bag:
                    if human_hurt == 1:  # 防止玩家叠伤害
                        human_hurt += 1
                        print("你的伤害增加了!")
                    else:
                        print("你的伤害已经增加了!")
                    human_bag.remove('knife')
                    score += 5000
                else:
                    print("你没有刀")

            # 治疗
            elif human_choice == "smoke" or human_choice == "桃" or human_choice == "烟":
                if 'smoke' in human_bag:
                    # 防止玩家疯狂叠甲
                    if people_life == page_life[times]:
                        print("你现在是满血")

                    else:
                        people_life += 1
                        print("你的生命值回复了!")
                    human_bag.remove('smoke')
                    score += 2000

                else:
                    print("你没有烟!")

            elif human_choice == "magnify" or human_choice == "放大镜":
                if 'magnify' in human_bag:
                    print("这颗子弹是: {}".format(gun_bullets[0]))
                    human_bag.remove(human_bag[human_bag.index('magnify')])  # 移除最上方的子弹,写得麻烦了些,效果不变
                    score += 3000

                else:
                    print("你没有放大镜")

            elif human_choice == 'beer' or human_choice == "退弹":
                if 'beer' in human_bag:
                    human_bag.remove('beer')
                    print("被退出来的子弹类型是: {}".format(gun_bullets[0]))
                    if gun_bullets[0] is True:
                        true_bullets_times -= 1
                        score += 4000
                    else:
                        false_bullets_times -= 1
                        score += 5000
                    gun_bullets.remove(gun_bullets[0])
                else:
                    print("你没有啤酒")

                # 处理推出子弹后子弹数量为零的操作
                if len(gun_bullets) == 0:
                    continue

            elif human_choice == 'lock' or human_choice == "乐不思蜀" or human_choice == "手铐":
                if 'lock' in human_bag:
                    human_bag.remove('lock')
                    print("你给对面乐不思蜀了")
                    score += 8000
                    sleep(1)
                    monster_getLock = True  # 将怪物被锁的状态设置为True
                else:
                    print("你没有手铐了")

        # 怪物的回合
        else:
            print("现在是我的回合了\n")
            sleep(1)
            print("我将会...\n")
            sleep(1)

            if 'smoke' in monster_bag and monster_life < page_life[times]:
                print("为什么不来抽一口呢?")
                sleep(1)
                monster_bag.remove('smoke')
                monster_life += 1
                continue

            # 当子弹数量大于1的时候且背包有放大镜
            elif 'magnify' in monster_bag and len(gun_bullets) > 1:
                print("让我看看这颗子弹...")
                sleep(1)
                print("非常有趣 :)\n")
                monster_bag.remove('magnify')  # 从怪物背包移除放大镜
                if gun_bullets[0] is True:  # 若子弹为真时
                    monster_logical_pool.append(True)
                    false_bullets_times = 0  # 意味着假子弹的数量为0,为下面分析处理作铺垫
                else:
                    monster_logical_pool.append(False)
                    true_bullets_times = 0  # 同上
                '''
                Q:  为什么放大镜在观测下一颗子弹的状态下,相反子弹的数量就为0?
                A:  因为在观测下一颗子弹后,怪物就必须知道下一颗子弹的状态,也就是为什么上面我添加了为逻辑池加入真假的代码,这是为了给下面使用beer和
                    monster_analyze这个函数做了铺垫:因为知道了下一颗子弹的状态,使用beer的操作就显得可有可无.接着当相反子弹的数量为0,
                    进入monster_analyze函数的false_bullets_times或者true_bullets_times就会变为0,这样就会为下面射击自己或者射击对方的操作做出了选择
                    而在射击结束后,这个循环会重复,即使是人类被锁住,真假子弹的数量也会重新统计.
                '''

            # 当怪物背包有酒且认为下一颗子弹为假时
            elif 'beer' in monster_bag and monster_logical_pool[-1] is False:
                print("喝一杯,退一弹")
                sleep(1)
                monster_bag.remove('beer')
                if gun_bullets[0] is True:  # 当子弹为真的时候
                    print("是真的呢,算你好运哈哈哈 :)\n")
                    sleep(1)
                    true_bullets_times -= 1
                    gun_bullets.remove(gun_bullets[0])

                else:  # 若子弹为假
                    print("是假的呢.哼哼哼\n")
                    false_bullets_times -= 1  # 假子弹数量减一
                    gun_bullets.remove(gun_bullets[0])  # 退出一枚子弹

            # 处理当怪物使用啤酒退子弹后子弹数量为零的情况
            if len(gun_bullets) == 0:
                continue

            # 退弹或检查下一颗子弹之后的分析操作
            monster_analyze(monster_logical_pool, true_bullets_times, false_bullets_times)

            # 当怪物背包有刀且认为下一枚子弹为真
            if 'knife' in monster_bag and monster_logical_pool[-1] is True:
                print("我会使用刀来增加我的伤害,你准备好了吗.")
                sleep(1)
                monster_hurt += 1
                monster_bag.remove('knife')

            # 当怪物背包有锁时
            if 'lock' in monster_bag and human_getLock is False:
                print("把你锁起来 =)")
                sleep(1)
                monster_bag.remove('lock')
                human_getLock = True

            # 若怪物逻辑池认为下一颗子弹为真
            if monster_logical_pool[-1] is True:
                print("我会射你\n")
                sleep(1)
                if gun_bullets[0] is True:  # 若子弹为真
                    people_life -= monster_hurt  # 扣除人类受到怪物伤害的血量
                    true_bullets_times -= 1  # 真子弹数量减一
                    gun_bullets.remove(gun_bullets[0])  # 退出一枚子弹
                    print("百步穿杨!\n")
                    sleep(1)
                    score += 200  # 人类受伤加分
                    if human_getLock is False:
                        monster_turn = False
                        human_turn = True

                    else:
                        human_getLock = False

                # 发射的子弹为假
                else:
                    print("你还真幸运 不是么?\n")
                    false_bullets_times -= 1
                    gun_bullets.remove(gun_bullets[0])
                    score += 300  # 若躲过子弹加分

            # 若逻辑池内怪物认为下一颗子弹为假
            else:
                sleep(1)
                print("我赌我的枪里没有子弹\n")
                if gun_bullets[0] is True:  # 若子弹为真
                    monster_life -= monster_hurt  # 扣除怪物的血量
                    true_bullets_times -= 1  # 真子弹数量减一
                    gun_bullets.remove(gun_bullets[0])  # 退出子弹
                    print("操!\n")
                    sleep(1)
                    if human_getLock is False:
                        monster_turn = False
                        human_turn = True

                    else:
                        human_getLock = False

                # 若子弹为假
                else:
                    print("我还挺幸运的呢\n")
                    sleep(1)
                    false_bullets_times -= 1
                    gun_bullets.remove(gun_bullets[0])

        monster_analyze(monster_logical_pool, true_bullets_times, false_bullets_times)
        monster_hurt = 1
    # 击杀对方的奖励
    else:
        score += 15000  # 奖励
        times += 1  # 新的一关

try:
    with open("history", mode="a") as f:
        f.write(str(bin(score)) + " ")

except FileExistsError:
    with open("history", mode="w") as f:
        f.write(str(bin(score)) + " ")
        f.write(str(bin(0)) + " ")

print("你最终的分数是:{:,}".format(score))

# 写入文件,对比上次分数
with open("history", mode="r") as f:
    try:
        last_temp = f.readlines()
        last = int(last_temp[len(last_temp) - 2].split()[len(last_temp) - 2], 2)
        sum_grade = f.readlines()
        print("你上次的分数{:,}".format(last))
        if last < score:
            print("比上次高了{:,}分".format(score - last))
        elif last > score:
            print("比上次低了{:,}分".format(last - score))
        else:
            print("没有变化")

        if score == max_times(sum_grade):
            print("本次为最佳成绩")
    except IndexError:
        print("本次为首次成绩")
