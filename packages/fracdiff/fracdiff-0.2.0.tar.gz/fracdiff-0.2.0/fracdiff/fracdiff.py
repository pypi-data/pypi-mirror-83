from sklearn.base import TransformerMixin
from sklearn.utils.validation import check_array
from sklearn.utils.validation import check_is_fitted

from fracdiff.base import fdiff
from fracdiff.base import fdiff_coef


class Fracdiff(TransformerMixin):
    """
    Fractional differentiation of time-series.

    Parameters
    ----------
    - d : float, default 1.0
        Order of differentiation.
    - window : int > 0 or None, default 10
        Number of observations to compute each element in the output.
    - mode : {"full", "valid"}, default "full"
        "full" (default) :
            Return elements where at least one coefficient is used.
            Shape of a transformed array is the same with the original array.
            At the beginning of a transformed array, boundary effects may be seen.
        "valid" :
            Return elements where all coefficients are used.
            Output size along axis 1 is `n_features - window_`.
            At the beginning of a time-series, boundary effects is not seen.
    - window_policy : {"fixed"}, default "fixed"
        If "fixed" :
            Fixed window method.
            Every term in the output is evaluated using `window_` observations.
            In other words, a fracdiff operator, which is a polynominal of a backshift
            operator, is truncated up to the `window_`-th term.
            The beginning `window_ - 1` elements in output are filled with `numpy.nan`.
        If "expanding" (not available yet) :
            Expanding window method.
            Every term in fracdiff time-series is evaluated using at least `window_`
            observations.
            The beginning `window_ - 1` elements in output are filled with `numpy.nan`.

    Attributes
    ----------
    - coef_ : numpy.array, shape (window_,)
        Sequence of coefficients in fracdiff operator.

    Examples
    --------
    >>> import numpy as np
    >>> X = np.arange(10).reshape(5, 2)
    >>> fracdiff = Fracdiff(0.5, window=3)
    >>> fracdiff.fit_transform(X)
    array([[0.   , 1.   ],
           [2.   , 2.5  ],
           [3.   , 3.375],
           [3.75 , 4.125],
           [4.5  , 4.875]])
    >>> fracdiff.coef_
    array([ 1.   , -0.5  , -0.125])

    Valid mode:
    >>> fracdiff = Fracdiff(0.5, window=3, mode="valid")
    >>> fracdiff.fit_transform(X)
    array([[3.   , 3.375],
           [3.75 , 4.125],
           [4.5  , 4.875]])

    Fracdiff is essentially a convolution:
    >>> X = np.array([1, 0, 0, 0]).reshape(-1, 1)
    >>> fracdiff = Fracdiff(0.5, window=4)
    >>> fracdiff.fit_transform(X)
    array([[ 1.    ],
           [-0.5   ],
           [-0.125 ],
           [-0.0625]])
    """

    def __init__(
        self,
        d=1.0,
        window=10,
        mode="full",
        window_policy="fixed",
    ):
        self.d = d
        self.window = window
        self.mode = mode
        self.window_policy = window_policy

    def __repr__(self):
        """
        Examples
        --------
        >>> Fracdiff(0.5)
        Fracdiff(d=0.5, window=10, mode=full, window_policy=fixed)
        """
        name = self.__class__.__name__
        attrs = ["d", "window", "mode", "window_policy"]
        params = ", ".join("{}={}".format(attr, getattr(self, attr)) for attr in attrs)
        return "{}({})".format(name, params)

    def fit(self, X=None, y=None):
        """
        Fit the model with `X`.
        Set `self.window_` and `self.coef_`.

        Parameters
        ----------
        - X : array-like, shape (n_samples, n_features), default None
            Ignored.
        - y : array-like, shape (n_samples,), default None
            Ignored.

        Returns
        -------
        self
        """
        self.coef_ = fdiff_coef(self.d, self.window)
        return self

    def transform(self, X, y=None):
        """
        Return fractional differentiation of X.

        Parameters
        ----------
        - X : array-like, shape (n_samples, n_series)
            Time-series to perform fractional differentiation.
            Raises ValueError if `n_samples < self.window_`.
        - y : None
            Ignored.

        Returns
        -------
        - diff : array, shape (n_samples, n_series)
            Fractionally differentiated time-series.
        """
        check_is_fitted(self, ["coef_"])
        check_array(X, estimator=self)
        return fdiff(X, n=self.d, axis=0, window=self.window, mode=self.mode)
