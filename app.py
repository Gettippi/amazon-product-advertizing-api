from flask import Flask, request, jsonify
from amazon.api import AmazonAPI


app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search_products():
    keywords = request.args.get('keywords')
    access_key = request.args.get('access_key')
    secret_key = request.args.get('secret_key')
    associate_tag = request.args.get('associate_tag')

    # Initialize the Amazon Product Advertising API client
    amazon = AmazonAPI(access_key, secret_key, associate_tag)

    # Perform the product search
    try:
        products = amazon.search(Keywords=keywords, SearchIndex='All')

        response = []

        for i, product in enumerate(products):
            response.append({
                'id': product.asin,
                'title': product.title,
                'url': product.offer_url,
                'price': product.price_and_currency[0],
                'currency': product.price_and_currency[1],
                'image_url': product.large_image_url
            })
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/convert_to_stripe', methods=['POST'])
def convert_to_stripe():
    data = request.json
    product_id = data.get('product_id')
    associate_tag = data.get('associate_tag')

    # Create an affiliate URL
    try:
        
        affiliate_url = f"http://www.amazon.com/dp/{product_id}/ref=nosim?tag={associate_tag}"
        return jsonify({'affiliate_url': affiliate_url})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
