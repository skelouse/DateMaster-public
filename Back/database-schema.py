
db = {
    'store_num': {  # 3652
        'department': {  # Dairy
            'mark_days': 0,  # 5
            'move_days': 0,  # 3
            'ood_quantity': 0,
            'todo_quantity': 0,
            # For the app to see if product list needs to be updated
            'product_num': 4908124,  # random between 1 and 1B
            # For the app to see if todo list needs to be updated
            'todo_num': 5892340,

            # Created by a cloud function at 12am everyday
            # Taken by the app as an custom ordereddict to parse in the itemviewer
            'todo': {
                'sect_num': {  # 100202300
                    'upc': 312321,

                    'date': "xx/xx/xxxx",  # 0 for oos


                    'type': "move/mark/ood/oos/marknmove",
                    'desc': "@@@@",
                    'img': "https://doc...",
                    'price': "$0.00"
                }
            },
            # Created from the section_id list + upc_data
            'products': {
                'upc': {
                    'sect_num1': {  # 100202300
                        'date': "xx/xx/xxxx",  # 0 for oos
                        'desc': "@@@@",
                        'img': "https://doc...",
                        'marked': False,
                        'moved': False,
                        'price': "$0.00",
                        'count': 13  # get from inventory
                    },

                    'sect_num2': {  # 100202300
                        'date': "xx/xx/xxxx",
                        'desc': "@@@@",
                        'img': "https://doc...",
                        'marked': False,
                        'moved': False,
                        'price': "$0.00",
                        'count': 13  # get from inventory
                    }
                }
            }
        },
        'data': {
            'upc':{
                'times_marked': 0,
                'times_moved': 0,
                'times_oos': 0,
                'avg_date_weight': 0,
                'avg_date': 0
            }
        } 
    },


    'upc_data': {
        'upc': {
            'desc': "@@@",
            'img': "https://doc...",
            'case_count': 12,

            # If discontinued is true, when marked oos remove from products
            'discontinuted': False
        }
    },

    'inventory-sect': {
        'dairy': [300, 325],
        'meat': [326, 350]
    }
}

if __name__ == "__main__":
    print('Store:')
    for i in db.items():
        print(i, '\n')
