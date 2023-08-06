from implicit.als import AlternatingLeastSquares
import numpy as np

from rs_tools.utils import encode, to_csc, dict_to_pandas


class Wrapper:
    def fit(
        self,
        df,
        show_progress=True,
        user_col='user_id',
        item_col='item_id',
        rating_col='rating',
    ):
        df, ue, ie = encode(df, user_col, item_col)
        self.ue, self.ie = ue, ie
        item_users = to_csc(df, user_col, item_col, rating_col).T
        self.model.fit(item_users, show_progress)
        df.loc[:, user_col] = ue.inverse_transform(df[user_col])
        df.loc[:, item_col] = ie.inverse_transform(df[item_col])

    def predict(
        self,
        df,
        k,
        filter_already_liked_items=True,
        filter_items=None,
        recalculate_user=False,
        user_col='user_id',
        item_col='item_id',
        rating_col='rating',
    ):
        df.loc[:, user_col] = self.ue.transform(df[user_col])
        df.loc[:, item_col] = self.ie.transform(df[item_col])
        user_items = to_csc(df, user_col, item_col, rating_col)
        df.loc[:, user_col] = self.ue.inverse_transform(df[user_col])
        df.loc[:, item_col] = self.ie.inverse_transform(df[item_col])
        pred = self.model.recommend_all(
            user_items, k, recalculate_user, filter_already_liked_items, filter_items
        )
        p = self.model.user_factors.dot(self.model.item_factors.T)
        scores = [p[row][vals].tolist() for row, vals in enumerate(pred)]
        pred = dict_to_pandas(
            {user: items for user, items in enumerate(pred)}, user_col, item_col
        )
        scores = dict_to_pandas(
            {user: score for user, score in enumerate(scores)},
            user_col,
            val_col=rating_col,
        )
        pred[rating_col] = scores[rating_col]
        pred.loc[:, item_col] = self.ie.inverse_transform(pred[item_col].astype(int))
        return pred


class ALS(Wrapper):
    def __init__(
        self,
        factors=100,
        regularization=0.01,
        dtype=np.float32,
        use_native=True,
        use_cg=True,
        use_gpu=False,
        iterations=15,
        calculate_training_loss=False,
        num_threads=0,
    ):
        self.model = AlternatingLeastSquares(
            factors=factors,
            regularization=regularization,
            dtype=dtype,
            use_native=use_native,
            use_cg=use_cg,
            use_gpu=use_gpu,
            iterations=iterations,
            calculate_training_loss=calculate_training_loss,
            num_threads=num_threads,
        )
