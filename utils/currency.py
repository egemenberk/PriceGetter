
TL = [  "vatanbilgisayar.com",
        "hepsiburada.com",
        "qp.com.tr",
        "amazon.com.tr",
        "ebrarbilgisayar.com",
        "incehesap.com",
        "trendyol.com",
        "itopya.com",
        "sinerji.gen.tr",
        "gameekstra.com",
        "urun.n11.com"
        ]

USD = [ "amazon.com",
        "ebay.com",
        "newegg.com",
]

def get_currency(url):
    if url in TL:
        return "₺"
    elif url in USD:
        return "$"
    else:
        return "#"
