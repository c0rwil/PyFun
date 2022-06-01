import random
test_list=[
    ('RedTest',1),
    ('BlueTest',1),
    ('GreenTest',2),
    ('BlackTest',0),
    ('WhiteTest',1),
    ('PurpleTest',2),
    ('YellowTest',5),
    ('OrangeTest',1)]

chosen_list =[]

def monte_picker():
    weights = [x[1] for x in test_list]
    tests = [x[0] for x in test_list]
    chosen_list.append(random.choices(tests, weights, k= 100))
    print(str(chosen_list))
    
def monte_count():
    for x in chosen_list:
        red_count = blue_count = green_count = black_count = white_count = purple_count = yellow_count = orange_count = 0
        if x == "RedTest":
            red_count += 1
        elif x == "BlueTest":
            blue_count += 1
        elif x == "GreenTest":
            green_count += 1
        elif x == "BlackTest":
            black_count += 1
        elif x == "WhiteTest":
            white_count += 1
        elif x == "PurpleCount":
            purple_count += 1
        elif x == "YellowCount":
            yellow_count += 1
        elif x == "OrangeCount":
            orange_count += 1
    print("Red Count = " + str(red_count) + '\n')
    print("Blue Count = " + str(blue_count) + '\n')
    print("Green Count = " + str(green_count) + '\n')
    print("Black Count = " + str(black_count) + '\n')
    print("White Count = " + str(white_count) + '\n')
    print("Purple Count = " + str(purple_count) + '\n')
    print("Yellow Count = " + str(yellow_count) + '\n')
    print("Orange Count = " + str(orange_count) + '\n')


monte_picker()
monte_count()

