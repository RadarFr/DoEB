from flask import Flask, request
from buyProdFunction import buyProd

hash = "82Jfo_()hP~''##"
app_key = "YOUR_APP_KEY"
app_secret = "YOUR_APP_SECRET"

app = Flask(__name__)

@app.route('/buy_item', methods=['POST'])
def buy_item():
    hash_value = request.form['hash']
    if hash == hash_value:
        product_ids = request.form.getlist("productIds")
        quantities = request.form.getlist("quantities")
        address = request.form["address"]
        currency = request.form["currency"]
        payment_method = "YOUR_DEFAULT_PAYMENT_METHOD"
        buyProd(product_ids, quantities, address, payment_method, currency, app_key, app_secret)
        return 'OK'
    else:
        return 'Unauthorized'
    
if __name__ == '__main__':
    app.run(debug=True)