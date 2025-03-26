from flask import Flask, request, jsonify
import logging
import traceback
from amazon_paapi import AmazonApi

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/search', methods=['GET'])
def search_products():
    keywords = request.args.get('keywords')
    access_key = request.args.get('access_key')
    secret_key = request.args.get('secret_key')
    associate_tag = request.args.get('associate_tag')

    amazon = AmazonApi(access_key, secret_key, associate_tag, 'US')

    # Perform the product search
    try:
        search_result = amazon.search_items(keywords=keywords)
        
        return jsonify(search_result.items)
    except Exception as e:
        logging.error("An error occurred during product search:", exc_info=e)
        traceback_str = traceback.format_exc()
        logging.debug("Complete traceback: %s", traceback_str)
        return jsonify({'error': str(e), 'traceback': traceback_str})

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
