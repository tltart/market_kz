import time



def get_data_from_page():
    false_parse = 0
    while false_parse < 10:
        try:
            print(false_parse)
            time.sleep(2)
            raise Exception

        except Exception as e:
            if false_parse == 5:
                print("Finish...")
                return -1
            print(f'Не распарсил страницу, повторяю... попытка: {false_parse}')
            false_parse += 1
            continue


get_data_from_page()