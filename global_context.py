
import time
from colorist import ColorRGB

PATH_TO_RESULT = './dist/locales/'
PATH_TO_RESULT_CHUNKS= './dist/locales_chunks/'

# чи фетчити без тегів
FETCH_NO_TAGS = False

# скільки разів пінгувати при обриві відповіді chatGPT. Оптимально - від 2 до 4, щоб виключити 0
MAX_PING_TRIES = 3

C_RED = ColorRGB(222, 79, 84)
C_GREEN = ColorRGB(121, 220, 154)
C_BLUE = ColorRGB(114, 159, 207)

TODAY_DATE = time.strftime("%Y-%m-%d")

# Product name to avoid it translation
PRODUCT_NAME = "ChessHelper"