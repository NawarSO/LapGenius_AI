# TODO: improvements (ordering + clarity + use-case awareness)
def generate_explanation(row):
    reasons = []

    # CPU
    cpu_score = row.get("cpu_score_norm", 0)
    if cpu_score > 0.7:
        reasons.append("Strong CPU performance suitable for heavy tasks")
    elif cpu_score > 0.4:
        reasons.append("Moderate CPU performance for general use")
    #############
    gpu_score = row.get("gpu_score_norm", 0)
    if gpu_score > 0.8:
        reasons.append("High-end GPU suitable for gaming and design")
    elif gpu_score > 0.5:
        reasons.append("Decent GPU for light gaming and graphics tasks")
    #############
    ram = row.get("ram_size", 0)
    if ram >= 32:
        reasons.append("Excellent RAM capacity for multitasking and heavy workloads")
    elif ram >= 16:
        reasons.append("Good RAM for most modern applications")
    else:
        reasons.append("Limited RAM, suitable for basic tasks")
    #############
    if row.get("storage_type") == "ssd":
        reasons.append("Fast SSD storage improves system responsiveness")
    else:
        reasons.append("HDD storage may reduce performance speed")
    ############
    price = row.get("price", 0)
    performance = row.get("performance", 0)

    if performance / (price + 1) > 0.05:
        reasons.append("Excellent performance-to-price ratio")
    elif performance / (price + 1) > 0.03:
        reasons.append("Balanced value for the price")
    else:
        reasons.append("Higher price relative to performance")
    ###########
    return reasons