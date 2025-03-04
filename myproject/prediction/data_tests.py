from  .models import NewsArticle
from .scripts  import  transform_to_df
#  if the funciton  returns   1 the test  for  data  is   past  and 0 if not 
def    test_data(data):
    df =   transform_to_df(data)
    required_columns = {'content', 'sentiment', 'real_price_change'}
    warnings = []

    # Check if all required columns exist
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        warnings.append(f"Warning: Missing columns: {missing_columns}")

    # Check for missing values in required columns
    for column in required_columns:
        if column in df.columns and df[column].isnull().sum() > 0:
            warnings.append(f"Warning: Column '{column}' contains {df[column].isnull().sum()} missing values")

    # Print warnings if any
    if warnings:
        for warning in warnings:
            print(warning)
        return 0    
    else:
        return 1

# Example Usage:
# Assuming df is your DataFrame

