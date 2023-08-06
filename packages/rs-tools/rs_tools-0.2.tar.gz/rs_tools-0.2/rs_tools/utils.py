from scipy.sparse import csc_matrix
from sklearn import preprocessing
import pandas as pd


def to_csc(df, user_col='user_id', item_col='item_id', rating_col='rating'):
    """ids should be label encoded ints"""
    row_count = df.user_id.max() + 1
    col_count = df.item_id.max() + 1

    return csc_matrix(
        (df[rating_col], (df[user_col], df[item_col])), shape=(row_count, col_count),
    )


def encode(df, user_col='user_id', item_col='item_id'):
    ue = preprocessing.LabelEncoder()
    ie = preprocessing.LabelEncoder()
    df.loc[:, user_col] = ue.fit_transform(df[user_col])
    df.loc[:, item_col] = ie.fit_transform(df[item_col])
    return df, ue, ie


def pandas_to_dict(df, user_col='user_id', item_col='item_id'):
    return df.groupby(user_col)[item_col].agg(list).to_dict()


def dict_to_pandas(d, key_col='user_id', val_col='item_id'):
    return (
        pd.DataFrame(d.items(), columns=[key_col, val_col])
        .explode(val_col)
        .reset_index(drop=True)
    )
