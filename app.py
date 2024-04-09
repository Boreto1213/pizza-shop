from flask import Flask, render_template, redirect, request

pizzas = [
    {"id": 1, "name": "Margarita", "small_price": 10, "medium_price": 12, "large_price": 15, "description": "Pizza margherita, as the Italians call it, is a simple pizza hailing from Naples. When done right, margherita pizza features a bubbly crust, crushed San Marzano tomato sauce, fresh mozzarella and basil, a drizzle of olive oil, and a sprinkle of salt.", "img": "../static/images/margarita.png", "ingredients": ["tomato sauce"," mozzarella", "basil", "olive oil"] },
    {"id": 2, "name": "Capricciosa", "small_price": 12, "medium_price": 14, "large_price": 16, "description":"Capricciosa Pizza is a classic Italian pizza. 'The Capricciosa', as everybody calls it, is on every pizzeria's menu, usually under the list of traditional pizzas. Its staple ingredients are tomato puree, mozzarella, cremini mushrooms, artichoke hearts, black olives, and prosciutto cotto (Italian cooked ham).", "img": "../static/images/capricosia.png", "ingredients": ["tomato sauce", "mozzarella", "mushrooms", "artichoke", "black olives", "italian ham"]},
    {"id": 3, "name": "Hawaiian", "small_price": 13, "medium_price": 15, "large_price": 17, "description":"Classic Hawaiian Pizza combines pizza sauce, cheese, cooked ham, and pineapple. This crowd-pleasing pizza recipe starts with our homemade pizza crust and is finished with a sprinkle of crispy bacon. It's salty, sweet, cheesy, and undeniably delicious!", "img": "../static/images/hawaiian.png", "ingredients": ["tomato sauce", "mozzarella", "italian ham", "pineapple"]},
    {"id": 4, "name": "Pepperoni", "small_price": 12, "medium_price": 14, "large_price": 16, "description":"Pepperoni pizza is an American pizza variety which includes one of the country's most beloved toppings. Pepperoni is a spicy salami, usually made with a mixture of beef, pork, and spices", "img": "../static/images/peperoni-pizza.png", "ingredients" : ["tomato sauce", "mozzarella", "pepperoni"]},
    {"id": 5, "name": "BBQ Chicken", "small_price": 14, "medium_price": 16, "large_price": 18, "description":"The flavors and textures in this pizza are incredible! You have the sweet tang from the BBQ sauce, the meaty chicken, the zesty red onion, fresh cilantro, smoky gouda, soft crust, crispy edges, and ultra cheesy mozzarella covering it all.", "img": "../static/images/bbq-chicken.png", "ingredients": ["tomato sauce", "mozzarella","BBQ sauce", "chicken", "red onion", "gouda cheese", "cilantro"]},
    {"id": 7, "name": "Veggie Pizza", "small_price": 11, "medium_price": 13, "large_price": 15, "description":"This vegetarian pizza recipe will delight vegetarians and carnivores alike. It's fresh and full of flavor, featuring cherry tomatoes, artichoke, bell pepper, olives, red onion and some hidden baby spinach. You'll find a base of rich tomato sauce and golden, bubbling mozzarella underneath, of course.", "img": "../static/images/veggie.png", "ingredients":["tomato sauce", "mozzarella", "cherry tomato", "artichoke", "bell pepper", "olives", "red onion", "baby spinach"]},
]

drinks = [
    {"id": 9, "name": "Iced tea", "img": "../static/images/ice-tea.png", 'price': 2},
    {"id": 10, "name": "Coffee", "img": "../static/images/coffee.png", 'price': 3},
    {"id": 11, "name": "Water", "img": "../static/images/water.png", 'price': 1},
    {"id": 12, "name": "Cola", "img": "../static/images/cola-can.png", 'price': 2},
    {"id": 13, "name": "Vodka", "img": "../static/images/vodka-2.png", 'price': 50}
]

desserts = [
    {"id": 14, "name": "Muffin", "img": "../static/images/muffin.png", 'price': 2},
    {"id": 15, "name": "Cheesecake", "img": "../static/images/cheesecake.png", 'price': 6},
    {"id": 16, "name": "Chocolate cake", "img": "../static/images/chocolate-cake.png", 'price': 5},
    {"id": 17, "name": "Milkshake", "img": "../static/images/milkshake.png", 'price': 3},
    {"id": 18, "name": "Ice Cream", "img": "../static/images/ice-cream.png", 'price': 3},
]


def get_item_by_id(id):
    all_itmes = pizzas + drinks + desserts

    item = [item for item in all_itmes if item['id'] == int(id)]

    if item:
        return item[0]
    else:
        return {}

def get_order_by_order_number(order_number, all_orders):
    order = [order for order in all_orders if order['order_number'] == int(order_number)]

    if order:
        return order[0]
    else:
        return {}


current_order = {
    'cart': [],
    'type': ''
} 
all_orders = []
order_number = 0
most_popular_product = pizzas[0]
newest_product = pizzas[2]
selected_items = pizzas
cart_items = []

selected_order = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/second-page')
def seocnd_page():
    return render_template('second-page.html', most_popular = most_popular_product, newest = newest_product)

@app.route('/menu')
def menu():
    return render_template('menu.html', items = selected_items)

@app.route('/cart')
def cart():
    total_price = sum(map(lambda item: item['price'], cart_items))
    return render_template('cart.html', cart_items = cart_items, total_price = total_price)

@app.route('/details/<id>')
def details(id):
    return render_template('details.html', item = get_item_by_id(id))

@app.route('/edit-ingredients')
def edit_ingredients():
    return render_template('edit-ingredients.html')

@app.route('/receipt')
def receipt():
    return render_template('receipt.html', order_number = order_number)

@app.route('/select-items/<type>')
def selecet_items(type):
    global selected_items
    global pizzas
    global drinks
    global desserts

    if type == 'pizzas':
        selected_items = pizzas
    elif type == 'drinks':
        selected_items = drinks
    else:
        selected_items = desserts

    return redirect('/menu')

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.form
    size = data.get('size')
    id = data['id']
    item = get_item_by_id(id)

    if size:
        item['price'] = item[size]
        item['size'] = size[0].upper()

    global cart_items
    cart_items.append(item)

    return redirect('/menu')

@app.route('/remove-from-cart/<id>')
def remove_from_cart(id):
    global cart_items
    for i in range(len(cart_items)):
        if cart_items[i]['id'] == int(id):
            cart_items.pop(i)
            break

    return redirect('/cart')

@app.route('/select-order-type/<type>')
def select_order_type(type):
    global current_order
    current_order['type'] = type.replace('-', '')

    return redirect('/second-page')


@app.route('/finish-order')
def finish_order():
    global current_order, all_orders, cart_items, order_number
    total_price = sum(map(lambda item: item['price'], cart_items))
    order_number += 1
    current_order['order_number'] = order_number
    current_order['cart'] = cart_items
    current_order['status'] = 'Waiting'
    current_order['total_price'] = f'{total_price:.2f}'
    all_orders.append(current_order)
    current_order = {}
    cart_items = []

    return redirect('/receipt')


@app.route('/cashier')
def cashier():
    return render_template('cashier.html', all_orders = all_orders, selected_order = selected_order)

@app.route('/cashier-select-order/<order_number>')
def cashier_select_order(order_number):
    global selected_order
    order = get_order_by_order_number(order_number, all_orders)
    selected_order = order

    return redirect('/cashier')

@app.route('/cancel-order/<id>')
def cancel_order(id):
    global all_orders, selected_order
    all_orders = list(filter(lambda order: order['order_number'] != int(id), all_orders))
    if selected_order not in all_orders:
        selected_order = None

    return redirect('/cashier')

@app.route('/cook')
def cook():
    return render_template('cook.html', all_orders = all_orders)

@app.route('/oven-started')
def oven_started():
    for i in range(len(all_orders)):
        if i == 4:
            break

        all_orders[i]['status'] = 'Prepairing'

    return redirect('/cook')

@app.route('/oven-finished')
def oven_finished():
    for order in all_orders:
        if order['status'] == 'Prepairing':
            order['status'] = 'Done'

    return redirect('/cook')