import codecs
import re
import sys


re_muti_space = re.compile(r'\s+', flags=re.U)

APOSTROPHE_MAP = {
    '\u2018': "'",
    '\u2019': "'",
    '\u201A': "'",
    '\u2032': "'",
    '\u02BC': "'",
    '\uFF07': "'",
    '`': "'",
    '´': "'",
}

# 整词替换，优先于后缀规则。含英语与尼日皮钦语常见缩写。
CONTRACTIONS = {
    "AIN'T": "ARE NOT",
    "CAN'T": "CAN NOT",
    "C'MON": "COME ON",
    "COULD'VE": "COULD HAVE",
    "COULDN'T": "COULD NOT",
    "COULDN'T'VE": "COULD NOT HAVE",
    "D'YOU": "DO YOU",
    "DIDN'T": "DID NOT",
    "DOESN'T": "DOES NOT",
    "DON'T": "DO NOT",
    "E'ER": "EVER",
    "EVERYBODY'S": "EVERYBODY IS",
    "EVERYONE'S": "EVERYONE IS",
    "EVERYTHING'S": "EVERYTHING IS",
    "HADN'T": "HAD NOT",
    "HASN'T": "HAS NOT",
    "HAVEN'T": "HAVE NOT",
    "HE'D": "HE WOULD",
    "HE'LL": "HE WILL",
    "HE'S": "HE IS",
    "HERE'S": "HERE IS",
    "HOW'D": "HOW WOULD",
    "HOW'LL": "HOW WILL",
    "HOW'RE": "HOW ARE",
    "HOW'S": "HOW IS",
    "I'D": "I WOULD",
    "I'LL": "I WILL",
    "I'M": "I AM",
    "I'MA": "I AM GOING TO",
    "I'VE": "I HAVE",
    "ISN'T": "IS NOT",
    "IT'D": "IT WOULD",
    "IT'LL": "IT WILL",
    "IT'S": "IT IS",
    "LET'S": "LET US",
    "MA'AM": "MADAM",
    "MIGHT'VE": "MIGHT HAVE",
    "MIGHTN'T": "MIGHT NOT",
    "MUST'VE": "MUST HAVE",
    "MUSTN'T": "MUST NOT",
    "NE'ER": "NEVER",
    "NEEDN'T": "NEED NOT",
    "NOBODY'S": "NOBODY IS",
    "NOTHING'S": "NOTHING IS",
    "O'CLOCK": "OF CLOCK",
    "OUGHTN'T": "OUGHT NOT",
    "SHAN'T": "SHALL NOT",
    "SHE'D": "SHE WOULD",
    "SHE'LL": "SHE WILL",
    "SHE'S": "SHE IS",
    "SHOULD'VE": "SHOULD HAVE",
    "SHOULDN'T": "SHOULD NOT",
    "SHOULDN'T'VE": "SHOULD NOT HAVE",
    "SOMEBODY'S": "SOMEBODY IS",
    "SOMEONE'S": "SOMEONE IS",
    "SOMETHING'S": "SOMETHING IS",
    "THAT'D": "THAT WOULD",
    "THAT'LL": "THAT WILL",
    "THAT'RE": "THAT ARE",
    "THAT'S": "THAT IS",
    "THERE'D": "THERE WOULD",
    "THERE'LL": "THERE WILL",
    "THERE'RE": "THERE ARE",
    "THERE'S": "THERE IS",
    "THEY'D": "THEY WOULD",
    "THEY'LL": "THEY WILL",
    "THEY'RE": "THEY ARE",
    "THEY'VE": "THEY HAVE",
    "THIS'LL": "THIS WILL",
    "THIS'S": "THIS IS",
    "WASN'T": "WAS NOT",
    "WE'D": "WE WOULD",
    "WE'LL": "WE WILL",
    "WE'RE": "WE ARE",
    "WE'VE": "WE HAVE",
    "WEREN'T": "WERE NOT",
    "WHAT'D": "WHAT WOULD",
    "WHAT'LL": "WHAT WILL",
    "WHAT'RE": "WHAT ARE",
    "WHAT'S": "WHAT IS",
    "WHAT'VE": "WHAT HAVE",
    "WHEN'S": "WHEN IS",
    "WHERE'D": "WHERE WOULD",
    "WHERE'LL": "WHERE WILL",
    "WHERE'RE": "WHERE ARE",
    "WHERE'S": "WHERE IS",
    "WHO'D": "WHO WOULD",
    "WHO'LL": "WHO WILL",
    "WHO'RE": "WHO ARE",
    "WHO'S": "WHO IS",
    "WHO'VE": "WHO HAVE",
    "WHY'D": "WHY WOULD",
    "WHY'S": "WHY IS",
    "WON'T": "WILL NOT",
    "WOULD'VE": "WOULD HAVE",
    "WOULDN'T": "WOULD NOT",
    "WOULDN'T'VE": "WOULD NOT HAVE",
    "Y'ALL": "YOU ALL",
    "Y'ALL'D": "YOU ALL WOULD",
    "Y'ALL'LL": "YOU ALL WILL",
    "Y'ALL'RE": "YOU ALL ARE",
    "Y'ALL'VE": "YOU ALL HAVE",
    "YOU'D": "YOU WOULD",
    "YOU'LL": "YOU WILL",
    "YOU'RE": "YOU ARE",
    "YOU'VE": "YOU HAVE",
    # Nigerian Pidgin
    "DAT'S": "DAT IS",
    "DEM'S": "DEM IS",
    "DEY'S": "DEY IS",
    "DIS'S": "DIS IS",
    "NA'S": "NA IS",
    "WE'S": "WE IS",
    "WETIN'S": "WETIN IS",
    "'CAUSE": "BECAUSE",
    "'COS": "BECAUSE",
    "'EM": "THEM",
    "'IM": "HIM",
    "'TIS": "IT IS",
    "'TWAS": "IT WAS",
}

S_IS_STEMS = {
    "HE", "SHE", "IT", "THAT", "THIS", "WHAT", "WHO", "WHERE", "WHEN", "WHY",
    "HOW", "THERE", "HERE", "WHICH", "SOMEONE", "SOMEBODY", "SOMETHING",
    "EVERYONE", "EVERYBODY", "EVERYTHING", "NOBODY", "NOTHING", "WETIN",
    "DAT", "DIS", "DEM", "DEY", "NA", "WE",
}

SUFFIX_RULES = (
    ("N'T'VE", " NOT HAVE"),
    ("N'T", " NOT"),
    ("'RE", " ARE"),
    ("'VE", " HAVE"),
    ("'LL", " WILL"),
    ("'M", " AM"),
    ("'D", " WOULD"),
)

# ASR 等价写法：识别成任一侧都算对，统一映射到规范形式。
VARIANT_MAP = {
    "OK": "OKAY",
    "ALRIGHT": "ALL RIGHT",
    "ALLRIGHT": "ALL RIGHT",
    "COS": "BECAUSE",
    "COZ": "BECAUSE",
    "CUZ": "BECAUSE",
    "BCOS": "BECAUSE",
    "BCOZ": "BECAUSE",
    "BCUZ": "BECAUSE",
    "BECOS": "BECAUSE",
    "BIKOS": "BECAUSE",
    "GONNA": "GOING TO",
    "WANNA": "WANT TO",
    "GOTTA": "GOT TO",
    "LEMME": "LET ME",
    "GIMME": "GIVE ME",
    "KINDA": "KIND OF",
    "SORTA": "SORT OF",
    "OUTTA": "OUT OF",
    "DUNNO": "DO NOT KNOW",
    "IMMA": "I AM GOING TO",
    "THRU": "THROUGH",
    "THO": "THOUGH",
    "TIL": "UNTIL",
    "TILL": "UNTIL",
    "UNTILL": "UNTIL",
    "PLS": "PLEASE",
    "PLZ": "PLEASE",
    "PLIS": "PLEASE",
    "THX": "THANKS",
    "THANX": "THANKS",
    "YEAH": "YES",
    "YEP": "YES",
    "YUP": "YES",
    "NOPE": "NO",
    "NAH": "NO",
    "TANKU": "THANK YOU",
}

# 语气词：思考、犹豫、应声、笑声。连写和长短音统一到规范形式。
FILLER_MAP = {
    "UM": "UM",
    "UMM": "UM",
    "UMMM": "UM",
    "UHM": "UM",
    "UHHM": "UM",
    "ERM": "UM",
    "URM": "UM",
    "EHM": "UM",
    "EM": "UM",
    "EMM": "UM",
    "UH": "UH",
    "UHH": "UH",
    "UHHH": "UH",
    "ER": "UH",
    "ERR": "UH",
    "ERRR": "UH",
    "AH": "AH",
    "AHH": "AH",
    "AHHH": "AH",
    "OH": "OH",
    "OHH": "OH",
    "OHHH": "OH",
    "EH": "EH",
    "EHH": "EH",
    "HMM": "HMM",
    "HMMM": "HMM",
    "HM": "HMM",
    "MM": "HMM",
    "MMM": "HMM",
    "MMMM": "HMM",
    "MHM": "HMM",
    "MMHM": "HMM",
    "MMHMM": "HMM",
    "MHMM": "HMM",
    "UHHUH": "UH HUH",
    "MMMHMM": "UH HUH",
    "UHOH": "UH OH",
    "AHA": "AHA",
    "AHHA": "AHA",
    "HAHA": "HAHA",
    "HAHAHA": "HAHA",
    "HAHAHAHA": "HAHA",
    "HEHE": "HAHA",
    "HEHEHE": "HAHA",
    "EHN": "EHN",
    "EHHN": "EHN",
    "EHNN": "EHN",
    "ENH": "EHN",
    "EHNEHN": "EHN",
    "CHAI": "CHAI",
    "CHEI": "CHAI",
    "CHEY": "CHAI",
    "CHEII": "CHAI",
}


def normalize_apostrophes(text):
    for src, dst in APOSTROPHE_MAP.items():
        text = text.replace(src, dst)
    return text


def expand_token(token):
    if "'" not in token and token not in CONTRACTIONS:
        return token
    if token in CONTRACTIONS:
        return CONTRACTIONS[token]
    for suffix, repl in SUFFIX_RULES:
        if token.endswith(suffix) and len(token) > len(suffix):
            return token[:-len(suffix)] + repl
    if token.endswith("'S") and len(token) > 2:
        stem = token[:-2]
        if stem in S_IS_STEMS:
            return stem + " IS"
        return stem
    return token.replace("'", " ")


def map_variant(token):
    return VARIANT_MAP.get(token, token)


def map_filler(token):
    key = token.replace("-", "")
    if key in FILLER_MAP:
        return FILLER_MAP[key]
    if re.fullmatch(r"U+M+", token):
        return "UM"
    if re.fullmatch(r"U+H+", token) or re.fullmatch(r"E+R+", token):
        return "UH"
    if re.fullmatch(r"A+H+", token):
        return "AH"
    if re.fullmatch(r"O+H+", token):
        return "OH"
    if re.fullmatch(r"E+H+", token):
        return "EH"
    if (re.fullmatch(r"H+M+", token) or re.fullmatch(r"M+H+M+", token)
            or re.fullmatch(r"M{2,}", token)):
        return "HMM"
    if re.fullmatch(r"(HA){2,}", token) or re.fullmatch(r"(HE){2,}", token):
        return "HAHA"
    if re.fullmatch(r"EH+N+", token) or re.fullmatch(r"EN+H+", token):
        return "EHN"
    return token


def normalize_text(text):
    text = normalize_apostrophes(text)
    text = text.upper()
    tokens = text.split()
    expanded = []
    for token in tokens:
        for part in expand_token(token).split():
            for variant in map_variant(part).split():
                expanded.extend(map_filler(variant).split())
    return ' '.join(expanded)


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
