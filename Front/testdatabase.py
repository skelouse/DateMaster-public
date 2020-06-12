from db.database import DataBase


def new_date(date, upc):
    return ({"date": date,
    "desc": "Kraft Natural Cheese, Shredded Whole Milk Mozzarella, 8oz Bag",
    "ftype": "new_date",
    "img": "https://docs.google.com/uc?id=",
    "price": "$0.00",
    "upc": upc})

def mark(date, upc):
    return ({"date": date,
    "desc": "Sargento Cheese Shredded, Traditional Cut, Extra Sharp Cheddar, 7.0 oz",
    "ftype": "mark",
    "img": "https://docs.google.com/uc?id=",
    "price": "$0.00",
    "upc": upc})

def movenmark(date, upc):
    return ({"date": date,
    "desc": "Lucerne Cheese Finely Shredded, Mexican Style, 4 Cheese Blend, 32.0 oz",
    "ftype": "movenmark",
    "img": "https://docs.google.com/uc?id=",
    "price": "$0.00",
    "upc": upc})

def move(date, upc):
    return ({"date": date,
    "desc": "Lucerne Cheese Finely Shredded, Mexican Style, 4 Cheese Blend, 32.0 oz",
    "ftype": "move",
    "img": "https://docs.google.com/uc?id=",
    "price": "$0.00",
    "upc": upc})


def oos(date, upc):
    return ({"date": date,
    "desc": "Sargento Cheese Shredded, Traditional Cut, Extra Sharp Cheddar, 7.0 oz",
    "ftype": "oos",
    "img": "https://docs.google.com/uc?id=",
    "price": "$0.00",
    "upc": upc})




id_token = ""
if __name__ == '__main__':
    
    class Blank():
        local_id = ""
        user_num = "5404136933"
        selected_dep = "Dairy"
    obj = Blank()

    db = DataBase(obj)

    date = "10/21/2019"
    upc = "2100007129"
    sect = "050101010"

    a = mark(date, upc)

    b = (sect, a)

    c = db.post_item(b)

    print(c.result)