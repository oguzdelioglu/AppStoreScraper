
STOPWORDS = {
    'en': {'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'your', 'you', 'app', 'apps', 'get', 'we', 'our', 'us', 'is', 'are', 'it', 'its', 'this', 'that', 'these', 'those', 'has', 'have', 'had', 'do', 'does', 'did', 'was', 'were', 'be', 'been', 'being', 'i', 'me', 'my', 'myself', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn', 'app', 'apps', 'game', 'games', 'mobile', 'phone', 'user', 'users', 'play', 'playing', 'new', 'best', 'top', 'free', 'paid', 'version', 'update', 'updates', 'feature', 'features', 'experience', 'time', 'world', 'story', 'level', 'levels', 'challenge', 'challenges', 'fun', 'enjoy', 'great', 'good', 'amazing', 'awesome', 'fantastic', 'super', 'cool', 'easy', 'simple', 'addictive', 'download', 'install', 'get', 'make', 'made', 'like', 'love', 'much', 'many', 'little', 'big', 'small', 'long', 'short', 'first', 'second', 'third', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundred', 'thousand', 'million', 'billion', 'trillion', 'etc', 'etcetera', 'example', 'examples', 'e.g', 'i.e', 'vs', 'via'},
    'tr': {'acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey', 'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep', 'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya', 'yani'},
    'de': {'aber', 'als', 'am', 'an', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis', 'bist', 'da', 'dadurch', 'daher', 'darum', 'das', 'daß', 'dass', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'dem', 'den', 'der', 'des', 'dessen', 'deshalb', 'die', 'dies', 'dieser', 'dieses', 'doch', 'dort', 'du', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines', 'er', 'es', 'euer', 'eure', 'für', 'hat', 'hatte', 'hatten', 'hattest', 'hattet', 'hier', 'hinter', 'ich', 'ihr', 'ihre', 'im', 'in', 'ist', 'ja', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jener', 'jenes', 'jetzt', 'kann', 'kannst', 'können', 'könnt', 'machen', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'mit', 'muß', 'mußt', 'musst', 'müssen', 'müßt', 'nach', 'nachdem', 'nein', 'nicht', 'nun', 'oder', 'seid', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst', 'sich', 'sie', 'sind', 'soll', 'sollen', 'sollst', 'sollt', 'sonst', 'soweit', 'sowie', 'und', 'unser', 'unsere', 'unserer', 'unseres', 'unter', 'vom', 'von', 'vor', 'wann', 'war', 'warum', 'was', 'weiter', 'weitere', 'wenn', 'wer', 'werde', 'werden', 'werdet', 'weshalb', 'wie', 'wieder', 'will', 'willst', 'wir', 'wird', 'wirst', 'wo', 'woher', 'wohin', 'zu', 'zum', 'zur'},
    'es': {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'ha', 'sí', 'porque', 'esta', 'son', 'entre', 'está', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'hasta', 'hay', 'donde', 'quien', 'sigue', 'desde', 'todo', 'nos', 'durante', 'todos', 'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí', 'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa', 'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas', 'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras', 'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro', 'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos', 'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás', 'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos', 'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve', 'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras', 'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos', 'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad', 'he', 'has', 'ha', 'hemos', 'habéis', 'han', 'haya', 'hayas', 'hayamos', 'hayáis', 'hayan', 'habré', 'habrás', 'habrá', 'habremos', 'habréis', 'habrán', 'habría', 'habrías', 'habríamos', 'habríais', 'habrían', 'había', 'habías', 'habíamos', 'habíais', 'habían', 'hube', 'hubiste', 'hubo', 'hubimos', 'hubisteis', 'hubieron', 'hubiera', 'hubieras', 'hubiéramos', 'hubierais', 'hubieran', 'hubiese', 'hubieses', 'hubiésemos', 'hubieseis', 'hubiesen', 'habiendo', 'habido', 'habida', 'habidos', 'habidas', 'soy', 'eres', 'es', 'somos', 'sois', 'son', 'sea', 'seas', 'seamos', 'seáis', 'sean', 'seré', 'serás', 'será', 'seremos', 'seréis', 'serán', 'sería', 'serías', 'seríamos', 'seríais', 'serían', 'era', 'eras', 'éramos', 'erais', 'eran', 'fui', 'fuiste', 'fue', 'fuimos', 'fuisteis', 'fueron', 'fuera', 'fueras', 'fuéramos', 'fuerais', 'fueran', 'fuese', 'fueses', 'fuésemos', 'fueseis', 'fuesen', 'sintiendo', 'sentido', 'sentida', 'sentidos', 'sentidas', 'siente', 'sentid', 'tengo', 'tienes', 'tiene', 'tenemos', 'tenéis', 'tienen', 'tenga', 'tengas', 'tengamos', 'tengáis', 'tengan', 'tendré', 'tendrás', 'tendrá', 'tendremos', 'tendréis', 'tendrán', 'tendría', 'tendrías', 'tendríamos', 'tendríais', 'tendrían', 'tenía', 'tenías', 'teníamos', 'teníais', 'tenían', 'tuve', 'tuviste', 'tuvo', 'tuvimos', 'tuvisteis', 'tuvieron', 'tuviera', 'tuvieras', 'tuviéramos', 'tuvierais', 'tuvieran', 'tuviese', 'tuvieses', 'tuviésemos', 'tuvieseis', 'tuviesen', 'teniendo', 'tenido', 'tenida', 'tenidos', 'tenidas', 'tened'},
}

COUNTRY_TO_LANG = {
    'af': 'ps',  # Pashto, Dari
    'al': 'sq',  # Albanian
    'dz': 'ar',  # Arabic
    'ad': 'ca',  # Catalan
    'ao': 'pt',  # Portuguese
    'ag': 'en',  # English
    'ar': 'es',  # Spanish
    'am': 'hy',  # Armenian
    'au': 'en',  # English
    'at': 'de',  # German
    'az': 'az',  # Azerbaijani
    'bs': 'en',  # English
    'bh': 'ar',  # Arabic
    'bd': 'bn',  # Bengali
    'bb': 'en',  # English
    'by': 'be',  # Belarusian
    'be': 'nl',  # Dutch, French, German
    'bz': 'en',  # English
    'bj': 'fr',  # French
    'bt': 'dz',  # Dzongkha
    'bo': 'es',  # Spanish
    'ba': 'bs',  # Bosnian
    'bw': 'en',  # English
    'br': 'pt',  # Portuguese
    'bn': 'ms',  # Malay
    'bg': 'bg',  # Bulgarian
    'bf': 'fr',  # French
    'bi': 'fr',  # French
    'kh': 'km',  # Khmer
    'cm': 'fr',  # French, English
    'ca': 'en',  # English, French
    'cv': 'pt',  # Portuguese
    'cf': 'fr',  # French
    'td': 'fr',  # French
    'cl': 'es',  # Spanish
    'cn': 'zh',  # Chinese
    'co': 'es',  # Spanish
    'km': 'ar',  # Arabic, French
    'cg': 'fr',  # French
    'cd': 'fr',  # French
    'cr': 'es',  # Spanish
    'hr': 'hr',  # Croatian
    'cu': 'es',  # Spanish
    'cy': 'el',  # Greek, Turkish
    'cz': 'cs',  # Czech
    'dk': 'da',  # Danish
    'dj': 'fr',  # French, Arabic
    'dm': 'en',  # English
    'do': 'es',  # Spanish
    'ec': 'es',  # Spanish
    'eg': 'ar',  # Arabic
    'sv': 'es',  # Spanish
    'gq': 'es',  # Spanish, French, Portuguese
    'er': 'ti',  # Tigrinya, Arabic, English
    'ee': 'et',  # Estonian
    'sz': 'en',  # English, Swazi
    'et': 'am',  # Amharic
    'fj': 'en',  # English, Fijian, Hindi
    'fi': 'fi',  # Finnish
    'fr': 'fr',  # French
    'ga': 'fr',  # French
    'gm': 'en',  # English
    'ge': 'ka',  # Georgian
    'de': 'de',  # German
    'gh': 'en',  # English
    'gr': 'el',  # Greek
    'gd': 'en',  # English
    'gt': 'es',  # Spanish
    'gn': 'fr',  # French
    'gw': 'pt',  # Portuguese
    'gy': 'en',  # English
    'ht': 'fr',  # French, Haitian Creole
    'hn': 'es',  # Spanish
    'hu': 'hu',  # Hungarian
    'is': 'is',  # Icelandic
    'in': 'hi',  # Hindi, English
    'id': 'id',  # Indonesian
    'ir': 'fa',  # Persian
    'iq': 'ar',  # Arabic, Kurdish
    'ie': 'en',  # English, Irish
    'il': 'he',  # Hebrew
    'it': 'it',  # Italian
    'jm': 'en',  # English
    'jp': 'ja',  # Japanese
    'jo': 'ar',  # Arabic
    'kz': 'kk',  # Kazakh, Russian
    'ke': 'sw',  # Swahili, English
    'ki': 'en',  # English
    'kw': 'ar',  # Arabic
    'kg': 'ky',  # Kyrgyz, Russian
    'la': 'lo',  # Lao
    'lv': 'lv',  # Latvian
    'lb': 'ar',  # Arabic
    'ls': 'en',  # English, Sesotho
    'lr': 'en',  # English
    'ly': 'ar',  # Arabic
    'li': 'de',  # German
    'lt': 'lt',  # Lithuanian
    'lu': 'fr',  # French, German, Luxembourgish
    'mg': 'fr',  # French, Malagasy
    'mw': 'en',  # English, Chichewa
    'my': 'ms',  # Malay
    'mv': 'dv',  # Dhivehi
    'ml': 'fr',  # French
    'mt': 'mt',  # Maltese, English
    'mh': 'en',  # English, Marshallese
    'mr': 'ar',  # Arabic
    'mu': 'en',  # English, French
    'mx': 'es',  # Spanish
    'fm': 'en',  # English
    'md': 'ro',  # Romanian
    'mc': 'fr',  # French
    'mn': 'mn',  # Mongolian
    'me': 'sr-ME',# Montenegrin
    'ma': 'ar',  # Arabic
    'mz': 'pt',  # Portuguese
    'mm': 'my',  # Burmese
    'na': 'en',  # English
    'nr': 'en',  # English, Nauruan
    'np': 'ne',  # Nepali
    'nl': 'nl',  # Dutch
    'nz': 'en',  # English, Maori
    'ni': 'es',  # Spanish
    'ne': 'fr',  # French
    'ng': 'en',  # English
    'kp': 'ko',  # Korean
    'mk': 'mk',  # Macedonian
    'no': 'no',  # Norwegian
    'om': 'ar',  # Arabic
    'pk': 'ur',  # Urdu, English
    'pw': 'en',  # English, Palauan
    'pa': 'es',  # Spanish
    'pg': 'en',  # English, Tok Pisin, Hiri Motu
    'py': 'es',  # Spanish, Guarani
    'pe': 'es',  # Spanish
    'ph': 'en',  # English, Filipino
    'pl': 'pl',  # Polish
    'pt': 'pt',  # Portuguese
    'qa': 'ar',  # Arabic
    'ro': 'ro',  # Romanian
    'ru': 'ru',  # Russian
    'rw': 'rw',  # Kinyarwanda, French, English
    'kn': 'en',  # English
    'lc': 'en',  # English
    'vc': 'en',  # English
    'ws': 'sm',  # Samoan, English
    'sm': 'it',  # Italian
    'st': 'pt',  # Portuguese
    'sa': 'ar',  # Arabic
    'sn': 'fr',  # French
    'rs': 'sr',  # Serbian
    'sc': 'fr',  # French, English, Seychellois Creole
    'sl': 'en',  # English
    'sg': 'en',  # English, Malay, Mandarin, Tamil
    'sk': 'sk',  # Slovak
    'si': 'sl',  # Slovenian
    'sb': 'en',  # English
    'so': 'so',  # Somali, Arabic
    'za': 'en',  # English, Afrikaans, Zulu, Xhosa, etc.
    'kr': 'ko',  # Korean
    'ss': 'en',  # English
    'es': 'es',  # Spanish
    'lk': 'si',  # Sinhala, Tamil
    'sd': 'ar',  # Arabic, English
    'sr': 'nl',  # Dutch
    'se': 'sv',  # Swedish
    'ch': 'de',  # German, French, Italian
    'sy': 'ar',  # Arabic
    'tw': 'zh',  # Chinese
    'tj': 'tg',  # Tajik
    'tz': 'sw',  # Swahili, English
    'th': 'th',  # Thai
    'tl': 'pt',  # Portuguese, Tetum
    'tg': 'fr',  # French
    'to': 'en',  # English, Tongan
    'tt': 'en',  # English
    'tn': 'ar',  # Arabic
    'tr': 'tr',  # Turkish
    'tm': 'tk',  # Turkmen
    'tv': 'en',  # English, Tuvaluan
    'ug': 'en',  # English, Swahili
    'ua': 'uk',  # Ukrainian
    'ae': 'ar',  # Arabic
    'gb': 'en',  # English
    'us': 'en',  # English
    'uy': 'es',  # Spanish
    'uz': 'uz',  # Uzbek
    'vu': 'en',  # English, Bislama, French
    'va': 'it',  # Italian, Latin
    've': 'es',  # Spanish
    'vn': 'vi',  # Vietnamese
    'ye': 'ar',  # Arabic
    'zm': 'en',  # English
    'zw': 'en',  # English, Shona, Ndebele
    'xk': 'sq', # Albanian
}

def get_stopwords_for_country(country_code):
    lang = COUNTRY_TO_LANG.get(country_code, 'en') # Default to English
    return STOPWORDS.get(lang, STOPWORDS['en'])
