from flask import Flask, request, jsonify
# from amazon.api import AmazonAPI
import logging
import amazonscraper

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/search', methods=['GET'])
def search_products():
    keywords = request.args.get('keywords')
    access_key = request.args.get('access_key')
    secret_key = request.args.get('secret_key')
    associate_tag = request.args.get('associate_tag')

    # Initialize the Amazon Product Advertising API client
    # amazon = AmazonAPI(access_key, secret_key, associate_tag)

    # Perform the product search
    try:
        results = amazonscraper.search(keywords, max_product_nb=5)

        # products = amazon.search(Keywords=keywords, SearchIndex='All')
        # try:
        #     logging.debug(products)
        # except Exception as e:
        #     logging.error("Error occurred while debugging:", exc_info=e)
        # response = []

        # for i, product in enumerate(products):
        #     response.append({
        #         'title': product.title,
        #         'url': product.offer_url
        #     })
        return jsonify(results)
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
