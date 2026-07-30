def filter_by_budget(df, budget):
    return df[df['price'] <= budget].copy()

def add_performance_score(df, weights, compute_performance_score):
    df = df.copy()

    df['performance'] = df.apply(lambda row: compute_performance_score(row, weights), axis=1)

    return df

def filter_by_min_performance(df, min_score):
    return df[df['performance'] >= min_score].copy()

def add_value_score(df, compute_value_score):
    df = df.copy()

    df['value'] = df.apply(lambda row: compute_value_score(row['performance'], row['price']), axis=1)

    return df



def rank_by_value(df, top_k):
    return df.sort_values("value", ascending=False).head(top_k)


def get_best(df, column):
    return df.sort_values(column, ascending=False).head(1)


"""def recommend_laptops(df, budget, use_case, top_k=5):
    config = use_case_weights[use_case]
    weights = config['weights']
    min_score = config['min_score']

    candidate_df = df[df['price'] <= budget].copy()

    if candidate_df.empty:
        return None

    # calculate the performance
    candidate_df['performance'] = candidate_df.apply(lambda row: compute_performance_score(row, weights) ,axis =1)

    # filtering based on threshold 
    candidate_df = candidate_df[candidate_df['performance'] >= min_score].copy()

    # check if the df not empty after filtering
    if candidate_df.empty:
        return None

    # calculate the value 
    candidate_df['value'] = candidate_df.apply(lambda row: compute_value_score(row['performance'], row['price']), axis =1)

    # results
    best_performance = candidate_df.sort_values('performance', ascending =False).head(1)
    best_value = candidate_df.sort_values('value', ascending = False).head(1)
    top_k = candidate_df.sort_values("value", ascending=False).head(top_k)

    # return the results
    return{
        "best_performance": best_performance,
        "best_value": best_value,
        "top_k": top_k
        }
        
        """