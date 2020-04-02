from app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(120), index=True, nullable=False)


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(7), nullable=False)

    def __repr__(self):
        return f'{self.firstname} {self.lastname}, street {self.street}, city {self.city}, province {self.province}'



class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sale_price = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.name} sold at price {self.sale_price} with sale_cost {self.unit_cost}'


class Transaction(db.Model):
    __tablename__ = "transaction"

    customerid = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False, primary_key=True)
    productid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity_sold = db.Column(db.Integer, nullable=False)
    total_sales = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, primary_key=True)    

    def __repr__(self):
        return f'{self.customerid} bought {self.productid}'


class Inventory(db.Model):
	productid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
	quanity_left = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f'{self.productid} left items {self.quanity_left}'    


class Procurement(db.Model):
    __tablename__ = "procurement"

    productid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
    quantity_purchased = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, primary_key=True)    

    def __repr__(self):
        return f'productid:{self.productid} acquired {self.quantity_purchased} on date {self.date}'





