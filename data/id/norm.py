import codecs
import re
import sys


re_useless_char = re.compile(r'[^A-Za-z0-9\s]+', flags=re.U)
re_muti_space = re.compile(r'\s+', flags=re.U)
re_unk = re.compile(r'<unk>', flags=re.IGNORECASE)
UNK_PLACEHOLDER = 'UNKPLACEHOLDER'

# 先处理整词会拆错的短语。PAPA 单独出现时是称呼，不能改。
PHRASE_PATTERNS = (
    (re.compile(
        r'\b(?:NGGAK|NGGA|ENGGAK|ENGGA|NGAK|GAK|GA|GK|NDAK|KAGAK|KAGA)\s+PAPA\b'
    ), 'TIDAK APA APA'),
    (re.compile(r'\b(?:GAPAPA|GPP)\b'), 'TIDAK APA APA'),
    (re.compile(r'\b(?:GAUSAH|GAUSA|NGGAUSAH)\b'), 'TIDAK USAH'),
    (re.compile(r'\bTHANK\s+YOU\b'), 'TERIMA KASIH'),
)

# 同一个词的口语写法，归一到规范形式。
VARIANT_MAP = {
    "NGGAK": "TIDAK",
    "NGGA": "TIDAK",
    "ENGGAK": "TIDAK",
    "ENGGA": "TIDAK",
    "NGAK": "TIDAK",
    "GAK": "TIDAK",
    "GA": "TIDAK",
    "GK": "TIDAK",
    "NDAK": "TIDAK",
    "KAGAK": "TIDAK",
    "KAGA": "TIDAK",
    "UDAH": "SUDAH",
    "DAH": "SUDAH",
    "BELOM": "BELUM",
    "BLOM": "BELUM",
    "GIMANA": "BAGAIMANA",
    "BAGIMANA": "BAGAIMANA",
    "KNAPA": "KENAPA",
    "NGAPA": "KENAPA",
    "GITU": "BEGITU",
    "GINI": "BEGINI",
    "AJA": "SAJA",
    "KARNA": "KARENA",
    "KALO": "KALAU",
    "TRUS": "TERUS",
    "EMANG": "MEMANG",
    "BENER": "BENAR",
    "TAU": "TAHU",
    "LIAT": "LIHAT",
    "ABIS": "HABIS",
    "SAMPE": "SAMPAI",
    "SAMPEI": "SAMPAI",
    "BOLE": "BOLEH",
    "ATO": "ATAU",
    "CUMAN": "CUMA",
    "BGT": "BANGET",
    "BNGET": "BANGET",
    "BANGEET": "BANGET",
    "GUA": "GUE",
    "GW": "GUE",
    "ELO": "LO",
    "ELU": "LO",
    "LU": "LO",
    "LOE": "LO",
    "IYAH": "IYA",
    "IYE": "IYA",
    "IYEH": "IYA",
    "YOI": "IYA",
    "OK": "OKE",
    "OKAY": "OKE",
    "OKEH": "OKE",
    "OKEY": "OKE",
    "MAKASIH": "TERIMA KASIH",
    "MAKASI": "TERIMA KASIH",
    "MAKACIH": "TERIMA KASIH",
    "TERIMAKASIH": "TERIMA KASIH",
    "THANKS": "TERIMA KASIH",
    "THX": "TERIMA KASIH",
    "NOMER": "NOMOR",
    "TELPON": "TELEPON",
    "TELFON": "TELEPON",
    "IJIN": "IZIN",
    "SILAHKAN": "SILAKAN",
    "RUPIYAH": "RUPIAH",
    "WHATAPP": "WHATSAPP",
    "WATSAP": "WHATSAPP",
    "WHATSAP": "WHATSAPP",
    "WA": "WHATSAPP",
    "TOPUP": "TOP UP",
    "DISINI": "DI SINI",
    "DISITU": "DI SITU",
    "DISANA": "DI SANA",
    "DIMANA": "DI MANA",
}

# 语气词只合并长短音，不把 ya / loh / dong / kok 并掉。
FILLER_MAP = {
    "UM": "UM",
    "UMM": "UM",
    "UHM": "UM",
    "EHM": "UM",
    "EM": "UM",
    "EMM": "UM",
    "UH": "UH",
    "UHH": "UH",
    "AH": "AH",
    "AHH": "AH",
    "OH": "OH",
    "OHH": "OH",
    "EH": "EH",
    "EHH": "EH",
    "HMM": "HMM",
    "HM": "HMM",
    "MM": "HMM",
    "MMM": "HMM",
    "ADUH": "ADUH",
    "ADUHH": "ADUH",
    "DUH": "DUH",
    "DUHH": "DUH",
    "WAH": "WAH",
    "WAHH": "WAH",
    "HAHA": "HAHA",
    "HAHAHA": "HAHA",
    "HEHE": "HAHA",
    "HIHI": "HAHA",
    "WKWK": "HAHA",
    "WKWKWK": "HAHA",
}


def apply_phrases(text):
    for pattern, repl in PHRASE_PATTERNS:
        text = pattern.sub(repl, text)
    return text


def map_filler(token):
    key = token.replace("-", "")
    if key in FILLER_MAP:
        return FILLER_MAP[key]
    if re.fullmatch(r"U+M+", token) or re.fullmatch(r"E+HM+", token):
        return "UM"
    if re.fullmatch(r"U+H+", token):
        return "UH"
    if re.fullmatch(r"A+H+", token):
        return "AH"
    if re.fullmatch(r"O+H+", token):
        return "OH"
    if re.fullmatch(r"E+H+", token):
        return "EH"
    if re.fullmatch(r"H+M+", token) or re.fullmatch(r"M{2,}", token):
        return "HMM"
    if re.fullmatch(r"ADU+H+", token):
        return "ADUH"
    if re.fullmatch(r"DU+H+", token):
        return "DUH"
    if re.fullmatch(r"WA+H+", token):
        return "WAH"
    if (re.fullmatch(r"(HA){2,}", token) or re.fullmatch(r"(HE){2,}", token)
            or re.fullmatch(r"(HI){2,}", token) or re.fullmatch(r"(WK){2,}", token)):
        return "HAHA"
    return token


def map_token(token):
    token = VARIANT_MAP.get(token, token)
    parts = []
    for part in token.split():
        parts.extend(map_filler(part).split())
    return parts


def normalize_text(text):
    text = re_unk.sub(UNK_PLACEHOLDER, text)
    text = text.upper()
    text = re_useless_char.sub(" ", text)
    text = re_muti_space.sub(" ", text).strip()
    text = apply_phrases(text)
    expanded = []
    for token in text.split():
        expanded.extend(map_token(token))
    return ' '.join(expanded).replace(UNK_PLACEHOLDER, '<unk>')


def split_key_text(line):
    if '\t' in line:
        key, text = line.split('\t', 1)
        return key.strip(), text.strip()
    parts = line.split()
    if not parts:
        return '', ''
    return parts[0], ' '.join(parts[1:])


src_file = sys.argv[1]
dst_file = sys.argv[2]

with codecs.open(src_file, 'r') as src_fp, \
        codecs.open(dst_file, 'w') as dst_fp:
    for line in src_fp:
        line = line.strip()
        if not line:
            continue
        key, text = split_key_text(line)
        text = normalize_text(text)
        text = re_muti_space.sub(" ", text).strip()
        if text:
            dst_fp.write('{} {}\n'.format(key, text))
        else:
            dst_fp.write('{}\n'.format(key))
