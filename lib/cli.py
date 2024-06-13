import click
from datetime import datetime
from models import Session, Item, Customer, Order

session = Session()

def display_menu():
    click.echo("Menu:")
    click.echo("1. Add Item")
    click.echo("2. Add Customer")
    click.echo("3. Place Order")
    click.echo("4. Delete Order")
    click.echo("5. Delete Item")
    click.echo("6. Update Item")
    click.echo("7. Update Customer")
    click.echo("8. Show Items")
    click.echo("9. Show Customers")
    click.echo("10. Show Orders")
    click.echo("11. Search Item")
    click.echo("0. Exit")

@click.command()
def main_menu():
    while True:
        display_menu()
        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("Enter item name")
            quantity = click.prompt("Enter item quantity", type=int)
            price = click.prompt("Enter item price", type=float)
            add_item(name, quantity, price)
        elif choice == 2:
            name = click.prompt("Enter customer name")
            email = click.prompt("Enter customer email")
            phone = click.prompt("Enter customer phone")
            add_customer(name, email, phone)
        elif choice == 3:
            customer_id = click.prompt("Enter customer ID", type=int)
            item_id = click.prompt("Enter item ID", type=int)
            quantity = click.prompt("Enter quantity", type=int)
            place_order(customer_id, item_id, quantity)
        elif choice == 4:
            order_id = click.prompt("Enter order ID", type=int)
            delete_order(order_id)
        elif choice == 5:
            item_id = click.prompt("Enter item ID", type=int)
            delete_item(item_id)
        elif choice == 6:
            item_id = click.prompt("Enter item ID", type=int)
            name = click.prompt("Enter new item name", default=None, show_default=False)
            quantity = click.prompt("Enter new item quantity", type=int, default=None, show_default=False)
            price = click.prompt("Enter new item price", type=float, default=None, show_default=False)
            update_item(item_id, name, quantity, price)
        elif choice == 7:
            customer_id = click.prompt("Enter customer ID", type=int)
            name = click.prompt("Enter new customer name", default=None, show_default=False)
            email = click.prompt("Enter new customer email", default=None, show_default=False)
            phone = click.prompt("Enter new customer phone", default=None, show_default=False)
            update_customer(customer_id, name, email, phone)
        elif choice == 8:
            show_items()
        elif choice == 9:
            show_customers()
        elif choice == 10:
            show_orders()
        elif choice == 11:
            name = click.prompt("Enter item name to search")
            search_item(name)
        elif choice == 0:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Please try again.")

@click.command()
@click.argument('name')
@click.argument('quantity', type=int)
@click.argument('price', type=float)
def add_item(name, quantity, price):
    session.add(Item(ItemName=name, Quantity=quantity, Price=price))
    session.commit()
    click.echo(f"Added item: {name}")

@click.command()
@click.argument('name')
@click.argument('email')
@click.argument('phone')
def add_customer(name, email, phone):
    session.add(Customer(CustomerName=name, Email=email, Phone=phone))
    session.commit()
    click.echo(f"Added customer: {name}")

@click.command()
@click.argument('customer_id', type=int)
@click.argument('item_id', type=int)
@click.argument('quantity', type=int)
def place_order(customer_id, item_id, quantity):
    session.add(Order(CustomerID=customer_id, ItemID=item_id, OrderDate=datetime.now(), Quantity=quantity))
    session.commit()
    click.echo(f"Placed order: Customer {customer_id} ordered {quantity} of item {item_id}")

@click.command()
@click.argument('order_id', type=int)
def delete_order(order_id):
    order = session.query(Order).filter_by(OrderID=order_id).first()
    if order:
        session.delete(order)
        session.commit()
        click.echo(f"Deleted order ID: {order_id}")
    else:
        click.echo(f"Order ID: {order_id} not found")

@click.command()
@click.argument('item_id', type=int)
def delete_item(item_id):
    item = session.query(Item).filter_by(ItemID=item_id).first()
    if item:
        session.delete(item)
        session.commit()
        click.echo(f"Deleted item ID: {item_id}")
    else:
        click.echo(f"Item ID: {item_id} not found")

@click.command()
@click.argument('item_id', type=int)
@click.option('--name', default=None, help='New name of the item')
@click.option('--quantity', type=int, default=None, help='New quantity of the item')
@click.option('--price', type=float, default=None, help='New price of the item')
def update_item(item_id, name, quantity, price):
    item = session.query(Item).filter_by(ItemID=item_id).first()
    if item:
        update_data = {}
        if name is not None:
            update_data['ItemName'] = name
        if quantity is not None:
            update_data['Quantity'] = quantity
        if price is not None:
            update_data['Price'] = price

        for key, value in update_data.items():
            setattr(item, key, value)
        session.commit()
        click.echo(f"Updated item ID: {item_id}")
    else:
        click.echo(f"Item ID: {item_id} not found")

@click.command()
@click.argument('customer_id', type=int)
@click.option('--name', default=None, help='New name of the customer')
@click.option('--email', default=None, help='New email of the customer')
@click.option('--phone', default=None, help='New phone number of the customer')
def update_customer(customer_id, name, email, phone):
    customer = session.query(Customer).filter_by(CustomerID=customer_id).first()
    if customer:
        update_data = {}
        if name is not None:
            update_data['CustomerName'] = name
        if email is not None:
            update_data['Email'] = email
        if phone is not None:
            update_data['Phone'] = phone

        for key, value in update_data.items():
            setattr(customer, key, value)
        session.commit()
        click.echo(f"Updated customer ID: {customer_id}")
    else:
        click.echo(f"Customer ID: {customer_id} not found")

@click.command()
def show_items():
    items = session.query(Item).all()
    item_list = [(item.ItemID, item.ItemName, item.Quantity, item.Price) for item in items]
    for item in item_list:
        click.echo(f"ItemID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")

@click.command()
def show_customers():
    customers = session.query(Customer).all()
    customer_list = [(customer.CustomerID, customer.CustomerName, customer.Email, customer.Phone) for customer in customers]
    for customer in customer_list:
        click.echo(f"CustomerID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}, Phone: {customer[3]}")

@click.command()
def show_orders():
    orders = session.query(Order).all()
    order_list = [(order.OrderID, order.CustomerID, order.ItemID, order.OrderDate, order.Quantity) for order in orders]
    for order in order_list:
        click.echo(f"OrderID: {order[0]}, CustomerID: {order[1]}, ItemID: {order[2]}, OrderDate: {order[3]}, Quantity: {order[4]}")

@click.command()
@click.argument('name')
def search_item(name):
    items = session.query(Item).filter(Item.ItemName.like(f'%{name}%')).all()
    if items:
        for item in items:
            click.echo(f"ItemID: {item.ItemID}, Name: {item.ItemName}, Quantity: {item.Quantity}, Price: {item.Price}")
    else:
        click.echo(f"No items found with name: {name}")

cli = click.Group()
cli.add_command(main_menu)
cli.add_command(add_item)
cli.add_command(add_customer)
cli.add_command(place_order)
cli.add_command(delete_order)
cli.add_command(delete_item)
cli.add_command(update_item)
cli.add_command(update_customer)
cli.add_command(show_items)
cli.add_command(show_customers)
cli.add_command(show_orders)
cli.add_command(search_item)

if __name__ == "__main__":
    cli()
    