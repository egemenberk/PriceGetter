
USD = [ "amazon.com",
        "ebay.com",
        "newegg.com",
]

def get_currency(url):
    if url in USD:
        return "$"
    else:
        return "₺"
