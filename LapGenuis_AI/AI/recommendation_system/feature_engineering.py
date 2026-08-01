import re
import pandas as pd
import numpy as np

from AI.recommendation_system.config import (family_scores,
                    suffix_scores,
                    cpu_family_scores,
                    storage_type_scores,
                    storage_size_scores,
                    ram_type_scores,
                    ram_size_scores,
                    CPU_MIN,
                    CPU_MAX,
                    GPU_MIN,
                    GPU_MAX,
                    RAM_MIN,
                    RAM_MAX,
                    STORAGE_MIN,
                    STORAGE_MAX)

from AI.common.hardware_parser import extract_hardware_features

############################################
# Specs extracting 
#############################################
# GPU Extracting
def extract_gpu_family(model):

    model = str(model).lower()

    if model.startswith("rtx"):
        return "rtx"

    elif model.startswith("gtx"):
        return "gtx"

    elif model.startswith("mx"):
        return "mx"

    elif model.startswith(("p", "t", "m")):
        return "quadro"

    elif model.startswith("wx"):
        return "quadro"

    elif model.startswith("arc") or model in ["140v", "140t"]:
        return "arc"

    elif "iris" in model:
        return "iris"

    elif model == "uhd":
        return "uhd"

    elif model.startswith("apple"):
        return "apple"

    elif model in ["610m", "560x", "8650g", "7400m", "r5"]:
        return "radeon"

    elif model.startswith("hd"):
        return "hd"

    else:
        return "unknown"
    
###################

def extract_nvidia_scores(model):
    
    digits = re.findall(r"\d+", model)

    if not digits:
        return None, None

    number = digits[0]

    generation_score = int(number[0])

    tier = int(number[2:])

    tier_score = (tier // 10) - 4

    return generation_score, tier_score

###################

#gpu_score = 10 +generation_score + tier_score
# TODO: handle gtx 3 digits ex: gtx960
def gpu_score(gpu):
    family = extract_gpu_family(gpu)
    if family in ['rtx', 'gtx']:
        generation_score, tier_score = extract_nvidia_scores(gpu)
        result =  family_scores[family] + generation_score + tier_score
    elif family == 'mx':
        generation_score, tier_score = extract_nvidia_scores(gpu)
        result = family_scores[family] + generation_score
    else:
        result = family_scores[family]
    return  result 

###################

###############################################################################################
# CPU Extracting

def intel_generation_score(model):

    model = int(model)

    if model >= 14000:
        return 5

    elif model >= 13000:
        return 4

    elif model >= 12000:
        return 3

    elif model >= 10000:
        return 2

    else:
        return 1

#######################
def amd_generation_score(model):

    model = int(model)

    if model >= 9000:
        return 5

    elif model >= 7000:
        return 4

    elif model >= 5000:
        return 3

    else:
        return 2
    
#######################

def cpu_score(row):
    #cpu_family_scores.get(row["cpu_tier"], 0) #TODO: replace every thing like (cpu_family_scores[row["cpu_tier"]]) with this line
    family = cpu_family_scores.get(row["cpu_tier"], 0)
    
    suffix = suffix_scores[row["cpu_suffix"]]

    generation = 0

    if row["cpu_brand"]== "intel":
        generation = intel_generation_score(
            row["cpu_model"]
        )

    elif row["cpu_brand"] == "amd":
        generation = amd_generation_score(
            row["cpu_model"]
        )

    return (family + generation + suffix)

########################

#################################################################################################

# RAM Extracting


def ram_score(row):
    size = row['ram_size']
    rtype = row['ram_type']
    return (ram_size_scores[size] + ram_type_scores[rtype])

################################################################
# Storage Extracting



def storage_score(row):
    size = row['storage_size']
    stype = row['storage_type']
    return (storage_size_scores[size] + storage_type_scores[stype])

######################################################################

# compute gaming, programming, design, general performance score based on weights
def compute_performance_score(row, weights):
    return (
        weights['cpu'] * row["cpu_score_norm"] +
        weights['gpu'] * row["gpu_score_norm"] +
        weights['ram'] * row["ram_score_norm"] +
        weights['storage'] * row["storage_score_norm"]
    )


##################################################################
#normalization
def normalize_scores(df):
    df = df.copy()

    df['cpu_score_norm'] = (df['cpu_score'] - CPU_MIN) / (CPU_MAX - CPU_MIN)
    df['gpu_score_norm'] = (df['gpu_score'] - GPU_MIN) / (GPU_MAX - GPU_MIN)
    df['ram_score_norm'] = (df['ram_score'] - RAM_MIN) / (RAM_MAX - RAM_MIN)
    df['storage_score_norm'] = (df['storage_score'] - STORAGE_MIN) / (STORAGE_MAX - STORAGE_MIN)

    return df

##################################################################

def add_hardware_scores(df):
    df = df.copy()

    df["cpu_score"] = df.apply(cpu_score, axis=1)
    df["gpu_score"] = df["gpu_model"].apply(gpu_score)
    df["ram_score"] = df.apply(ram_score, axis=1)
    df["storage_score"] = df.apply(storage_score, axis=1)

    return df

#################################################################
def compute_value_score(performance_score, price):
    return performance_score / np.log1p(price)


################################################################

def prepare_recommendation_data(df):
    df = extract_hardware_features(df)

    df = add_hardware_scores(df)

    df = normalize_scores(df)

    return df