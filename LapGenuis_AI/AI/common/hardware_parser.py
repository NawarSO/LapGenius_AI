import re
import pandas as pd

#======================
# Specs preprocessing (parsing)
#Extract features from row data
#=====================


def extract_cpu_brand(x):   
    brand_keywords = {
        "intel": ["core", "ultra", "xeon", "intel"],
        "amd": ["ryzen", "athlon", "amd"],
        "snapdragon": ["snapdragon"],
        "celeron": ["celeron"],
        "apple": ["m1", "m2", "m3", "m4"]
    }
    x = x.lower()
    for brand, keywords in brand_keywords.items():
        if any(keyword in x for keyword in keywords):
            return brand
    return None


#############
def extract_cpu_tier(x):  #middle2
    if pd.isna(x):
        return None
    x = str(x).lower()
    test = re.search(r'i\d{1}|ryzen \d{1}|ultra \d{1}|core \d{1}|x plus|n\d{3,4}|m\d{1}|a\d{1}|atom|a\d{1} [a-z]{3}|celeron|xeon|athlon\s*\w*', x)
    if(test):
        return test[0]
    else:
        return test
################

def extract_cpu_model(x):  #extract_model
    if not x:
        return 0

    x = x.lower()

    # Apple
    match = re.search(r'm(\d)', x)
    if match:
        return int(match.group(1))

    # أي رقم 3-5 digits 
    match = re.search(r'(\d{3,5})', x)
    if match:
        return int(match.group(1))

    return 0
#################

def extract_cpu_suffix(x): #extract_suffix
    if not x:
        return "unknown"

    x = x.lower()

    # Apple tiers
    match = re.search(r'\b(pro|max|ultra)\b', x)
    if match:
        return match.group(1)

    # Intel G-series (G1, G7...)
    match = re.search(r'\d{3,5}(g\d)', x)
    if match:
        return match.group(1)

    # Intel/AMD normal suffix (H / HX / U / P ...)
    match = re.search(r'\d{3,5}\s?([a-z]{1,2})\b', x)
    if match:
        return match.group(1)

    return "unknown"

#################

#=====================
#GPU
#====================
def extract_gpu_brand(x):
    if not x:
        return "unknown"

    x = str(x).lower()

    # Explicit brands
    if "nvidia" in x:
        return "nvidia"

    if "amd" in x or "radeon" in x:
        return "amd"

    if "intel" in x or "integrated" in x:
        return "intel"

    if "apple" in x:
        return "apple"

    # NVIDIA model keywords
    nvidia_patterns = [
        r'rtx',
        r'gtx',
        r'\bmx\d+',
        r'\bt\d+',
        r'\bp\d+',
        r'\bm\d+',
        r'gt\d+'
    ]

    for pattern in nvidia_patterns:
        if re.search(pattern, x):
            return "nvidia"

    return "unknown"

########################

def extract_gpu_model(x):
    if not x:
        return "unknown"
    x = str(x).lower()
    gmpattern = [
        r'rtx\s?\d+',
        r'gtx\s?\d+',
        r'mx\s?\d+',
        r'm\s?\d+',
        r't\s?\d+',
        r'p\s?\d+',
        ####AMD####
        r'\d{3,4}[a-z]',
        r'rx\s?\d+',
        r'r\s?\d+',
        r'wx\s?\d+',
        ##apple##
        r'apple\s?\d+',
        ##intel##
        r'iris\s?xe',
        r'uhd',
        r'hd',
        r'arc\s?\d*[a-z]?'
    ]
    for pattern in gmpattern:
        result = re.search(pattern , x)
        if(result):
            return result.group(0) #TODO: IMPORTANT NOTE this will return rtx 3050 we need to resolve it in calling to be rtx3050 sol: df['gpu_model'].replace(r'\s', '', regex=True)
    return "unknown"

#################################

#======================
#RAM
#====================
def extract_ram_size(x):
    if not x:
        return 0

    x = str(x).lower()

    # 1. GB 
    match = re.search(r'(\d{1,3})\s*gb', x)
    if match:
        return int(match.group(1))

    # 2. G  (8G)
    match = re.search(r'(\d{1,3})\s*g\b', x)
    if match:
        return int(match.group(1))

    # 3. fallback 
    match = re.search(r'\b(\d{1,3})\b', x)
    if match:
        return int(match.group(1))

    return 0


###################
def extract_ram_type(x):
    if  pd.isna(x):
        return "unknown"

    x = x.lower()

    match = re.search(r'ddr\d', x)
    if match:
        return match.group(0)

    match = re.search(r'lpddr\d', x)
    if match:
        return match.group(0)

    return "unknown"
#####################

##########################################################################
#=======================
#storage
#====================
def extract_storage_size(x):
    if not x:
        return 0

    x = str(x).lower()

    # TB → 1000 GB
    match = re.search(r'(\d+)\s*tb', x)
    if match:
        return int(match.group(1)) * 1000

    # GB (512G / 512GB)
    match = re.search(r'(\d{3,4})\s*g\b', x)
    if match:
        return int(match.group(1))

    match = re.search(r'(\d{3,4})\s*gb', x)
    if match:
        return int(match.group(1))

    # fallback (last chance only valid sizes)
    match = re.findall(r'\b(128|256|512|1000|2000|64)\b', x)
    if match:
        return max([int(i) for i in match])

    return 0
###############################
def extract_storage_type(x):
    if not x:
        return "unknown"

    x = str(x).lower()

    # HDD explicit
    if "hdd" in x:
        return "hdd"

    # SSD explicit
    if "ssd" in x:
        return "ssd"

    # implicit SSD indicators
    if any(k in x for k in ["nvme", "m.2", "pcie", "emmc"]):
        return "ssd"

    return "unknown"

###############################

def strip_columns(df):
    df.columns = df.columns.str.strip()

def clean_cpu_and_gpu(df):
    df = df.copy()
    df['cpu'] = (
            df['cpu']
            .str.replace('®', '', regex=False)
            .str.replace('™', '', regex=False)
            .str.replace(r'[^A-Za-z0-9\s]', ' ', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
    )
    df['gpu'] = (df['gpu']
            .str.replace("®", "", regex=False)
            .str.replace("™", "", regex=False)
            .str.replace("ᵉ", "e", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(r'\s+', '', regex=True)
            .str.strip()
              )
    return df

def clean_ram_and_storage(x):
    if pd.isna(x):
        return ""
    # keep only English letters, numbers, spaces
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', x)


brand_map = {
    "LENOVO":"Lenovo",
    "Asus":"ASUS",
    "DELL":"Dell",
    "HP":"hp",
    "TOSHIBA":"Toshiba",
    "MICROSOFT":"Microsoft"
}

def prepare_new(df):
    df = df.copy()
    df['new'] = (
        df['new']
        .astype(str)
        .str.lower()
        .str.strip()
)

    df['new'] = df['new'].map({
        'true': 1,
        'false': 0
    }).astype(int)

    return df

 

def extract_hardware_features(df):
    
    df = df.copy()
    #clean columns name
    strip_columns(df)
    #normalize brands
    df['brand'] = df['brand'].replace(brand_map) #TODO: implement clear handler for brands
    #clean cpu & gpu values
    df = clean_cpu_and_gpu(df)
    #clean ram values
    df['ram'] = df['ram'].apply(clean_ram_and_storage)
    #clean \ storage values
    df['hard'] = df['hard'].apply(clean_ram_and_storage)
    #extract specs
    #cpu
    df['cpu_brand'] =   df['cpu'].apply(extract_cpu_brand)
    df['cpu_tier'] = df['cpu'].apply(extract_cpu_tier)
    df['cpu_model'] = df['cpu'].apply(extract_cpu_model)
    df['cpu_suffix'] = df['cpu'].apply(extract_cpu_suffix)
    #gpu
    df['gpu_brand'] = df['gpu'].apply(extract_gpu_brand)
    df['gpu_model'] = df['gpu'].apply(extract_gpu_model)
    #ram
    df['ram_size'] = df['ram'].apply(extract_ram_size)
    df['ram_type'] = df['ram'].apply(extract_ram_type)
    #storage
    df['storage_size'] =  df['hard'].apply(extract_storage_size) 
    df['storage_type'] =  df['hard'].apply(extract_storage_type)
    #new
    df = prepare_new(df)
    
    return df
