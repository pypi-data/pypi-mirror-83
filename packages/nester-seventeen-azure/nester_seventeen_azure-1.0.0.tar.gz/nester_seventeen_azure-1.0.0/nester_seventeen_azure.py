"""这是nester.py模块,它的作用是打印列表，其中可能包含也可能不包含嵌套列表"""
def print_lol(the_list):
    """the_list是一个位置参数，可以是任何Python列表"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
            
