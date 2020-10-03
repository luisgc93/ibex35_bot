TW_CHAR_LIMIT = 280

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
    "Safari/537.36"
}

SITES = [
    {
        "home_url": "https://www.eleconomista.es/mercados-cotizaciones/",
        "xpath":         '//div[@class="firstContent-centerColumn '
                         "col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 "
                         'order-lg-2"]//a/@href',
     },
    {
        "home_url": "https://www.bolsamania.com/indice/IBEX-35/noticias",
        "xpath": "//article/header/h2/a/@href"
    }
]
