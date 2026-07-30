from AI.data_provider.client import fetch_all_laptops
import pandas as pd
# brand,model,cpu,ram,hard,gpu,new,price,source
def parse_laptops():
    laptops = fetch_all_laptops()
    parsed_laptops = []
    for lap in laptops:
        l = {
            'id': lap['id'],
            'brand': lap['brand'],
            'model': lap['name'],
            'cpu': lap['cpu_type'],
            'ram': lap['ram_size'],
            'hard': lap['storage_size'],
            'gpu': lap['gpu_type'],
            'price': lap['price'],
            'new': True if lap['condition'] == 'new' else False,
        }
        parsed_laptops.append(l)
    df = pd.DataFrame(parsed_laptops)
    #convert price str -> int Because my model and algo work on int price however the api returned it as str.
    df["price"] = pd.to_numeric(df["price"], errors="coerce") 

    print(df.isna().sum())


    return df
