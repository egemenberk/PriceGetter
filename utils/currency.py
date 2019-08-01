
USD = [ "amazon.com",
        "ebay.com",
        "newegg.com",
]

EUR = [ "amazon.de" ]

def get_currency(url):
    if url in USD:
        return "$"
    elif url in EUR:
        return "€"
    else:
        return "₺"
