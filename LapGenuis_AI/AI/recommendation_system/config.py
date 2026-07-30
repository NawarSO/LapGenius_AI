use_case_weights = {
"general" : {
    "weights":{
        "cpu": 0.35,
        "ram": 0.35,
        "storage": 0.2,
        "gpu": 0.1
    },
    "min_score": 0.35
    },

"programming" : {
    "weights":{"cpu": 0.45,
    "ram": 0.3,
    "storage": 0.15,
    "gpu": 0.1
    },
    "min_score": 0.5
    },

"design" : {
    "weights":{"gpu": 0.4,
    "ram": 0.3,
    "cpu": 0.2, 
    "storage": 0.1
    },
     "min_score": 0.6
    },

"gaming" : {
    "weights":{"gpu": 0.45,
    "cpu": 0.3,
    "ram": 0.2,
    "storage": 0.05},
     "min_score": 0.6
    }
}

storage_size_scores = {
0: 0,
128: 1,
256: 2,
512: 4,
500: 4,
1024: 7,
1000: 7,
2000: 9,
2048: 9,
4096: 10
}
storage_type_scores = {
'ssd': 2,
'hdd': 0,
'unknown':0
}

ram_size_scores = {
    0: 0,
    2: 1,
    4: 2,
    8: 4,
    12: 5,
    16: 7,
    24: 8,
    32: 9,
    64: 10
}
ram_type_scores ={
'ddr4':1,
'ddr5':2,
'ddr6':3,
'unknown':0
}

cpu_family_scores = {
    # Very Low
    "atom": 1,
    "a1": 1,
    "a6": 1,
    "a8": 1,

    # Low
    "celeron": 2,
    "athlon silver": 2,
    "n100": 2,

    # Entry
    "i3": 4,
    "core 3": 4,
    "ryzen 3": 4,

    # Mid
    "i5": 6,
    "core 5": 6,
    "ryzen 5": 6,

    # High
    "i7": 8,
    "core 7": 8,
    "ryzen 7": 8,

    # Enthusiast
    "i9": 10,
    "ultra 9": 10,
    "ryzen 9": 10,

    # Special
    "ultra 5": 7,
    "ultra 7": 9,

    "xeon": 8,

    "m1": 8,
    "m2": 9,
    "m3": 10,

    "x plus": 8
}

suffix_scores = {
    "unknown": 0,

    "g1": 1,
    "g7": 1,

    "u": 2,

    "h": 4,
    "hq": 4,
    "hs": 4,

    "hk": 5,
    "hx": 6,

    "pro": 3,

    "m": 5,

    "ultra": 4
}

family_scores = {
    "rtx": 10,
    "gtx": 8,
    "rx":9,
    "quadro": 7,

    "arc": 7,

    "apple": 6,

    "mx": 5,

    "iris": 4,
    "radeon": 4,

    "uhd": 2,
    "hd": 1,

    "unknown": 0
}

CPU_MIN = 2
CPU_MAX = 21

GPU_MIN = 0
GPU_MAX = 19

RAM_MIN = 0
RAM_MAX = 11

STORAGE_MIN = 0
STORAGE_MAX = 11