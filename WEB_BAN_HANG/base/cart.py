from .models import Product
class Cart():
    def __init__(self, request):
        self.session = request.session

        #Get the current session key if exists
        cart = self.session.get('session_key')
        
        #If the user is new, no session, create a new one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages of site
        self.cart = cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #Logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price_sell)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
    def __len__(self):
        return len(self.cart)
    #Get product
    def get_prods(self):
        #Get ids from cart
        product_ids = self.cart.keys()
        #Use ids to lookup products in DB
        products = Product.objects.filter(id__in=product_ids) 
        #Return list of found products
        return products
    def get_quants(self):
        quantites = self.cart
        return quantites
    def update(self,product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        #Get cart
        ourcart = self.cart
        #Update cart, which is by now a dictionary {'4':2, '1':3}
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing