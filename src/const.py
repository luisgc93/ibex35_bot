TW_CHAR_LIMIT = 280

MINIMUM_PARAGRAPH_LENGTH = 30

SHORTENED_URL_LENGTH = 23

TRUNCATED_TEXT_STRING = "(...)"

MAX_TRUNCATED_CHARACTER_COUNT = (
    TW_CHAR_LIMIT - SHORTENED_URL_LENGTH - len(TRUNCATED_TEXT_STRING)
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
    "Safari/537.36"
}

SITES = [
    {
        "home_url": "https://www.eleconomista.es/mercados-cotizaciones/",
        "xpath": '//div[@class="firstContent-centerColumn '
        "col-xl-5 col-lg-5 col-md-12 col-12 order-1 order-md-1 "
        'order-lg-2"]//a/@href',
    },
    {
        "home_url": "https://www.bolsamania.com/indice/IBEX-35/noticias",
        "xpath": "//article/header/h2/a/@href",
    },
    {
        "home_url": "https://www.abc.es/economia/bolsa/ibex-35/",
        "xpath": "//article/span/h1/a/@href",
    },
]

API_LIMIT_EXCEEDED_MESSAGE = (
    "Our standard API call frequency is 5 calls per minute and 500 calls per day."
)

API_LIMIT_EXCEEDED_RESPONSE = "Se ha excedido el límite de búsquedas (5/minuto y 500/día). Vuelve a probar más tarde."

STOCK_NOT_FOUND_RESPONSE = (
    "Disculpa, solo puedo buscar acciones que cotizan en el NASDAQ, "
    "lo que excluye ciertas empresas del IBEX 😓: "
    "https://www.nasdaq.com/market-activity/stocks/screener."
)
