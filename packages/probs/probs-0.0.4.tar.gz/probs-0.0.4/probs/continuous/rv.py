from __future__ import annotations

from typing import cast, no_type_check

import numpy as np
from scipy.integrate import quad

from probs.rv import RandomVariable


class ContinuousRV(RandomVariable):
    """
    We currently use @no_type_check because there currently isn't any valuable type-info
    for these methods. We will eventually use # type: ignore once there is something
    important to typecheck.
    """

    @no_type_check
    def __add__(self, other: object) -> ContinuousRV:
        if isinstance(other, ContinuousRV):
            other_var = other
            result = type(self)()
            result.pdf = lambda z: quad(
                lambda x: self.pdf(x) + other_var.pdf(z - x), -np.inf, np.inf
            )[0]
            result.expectation = lambda: self.expectation() + other_var.expectation()
            # Assumes Independence of X and Y, else add (+ 2 * Cov(X, Y)) term
            result.variance = lambda: self.variance() + other_var.variance()
            return result
        return cast(ContinuousRV, super().__add__(other))

    @no_type_check
    def __sub__(self, other: object) -> ContinuousRV:
        if isinstance(other, ContinuousRV):
            result = type(self)()
            result.pdf = lambda z: quad(
                lambda x: self.pdf(x) + other.pdf(z + x), -np.inf, np.inf
            )[0]
            result.expectation = lambda: self.expectation() - other.expectation()
            # Variances are added regardless of addition/subtraction.
            result.variance = lambda: self.variance() + other.variance()
            return result
        return cast(ContinuousRV, super().__sub__(other))

    @no_type_check
    def __mul__(self, other: object) -> ContinuousRV:
        if isinstance(other, ContinuousRV):
            result = type(self)()
            result.pdf = lambda z: quad(
                lambda x: (self.pdf(x) + other.pdf(z / x)) / abs(x),
                -np.inf,
                np.inf,
                full_output=True,
            )[0]
            # Assumes Independence of X and Y
            result.expectation = lambda: self.expectation() * other.expectation()
            result.variance = (
                lambda: (self.variance() ** 2 + self.expectation() ** 2)
                + (other.variance() ** 2 + other.expectation() ** 2)
                - (self.expectation() * other.expectation()) ** 2
            )
            return result
        return cast(ContinuousRV, super().__mul__(other))

    @no_type_check
    def __truediv__(self, other: object) -> ContinuousRV:
        if isinstance(other, ContinuousRV):
            result = type(self)()
            result.pdf = lambda z: quad(
                lambda x: (self.pdf(x) + other.pdf(z * x)) / abs(x),
                -np.inf,
                np.inf,
                full_output=True,
            )[0]
            result.expectation = lambda: (_ for _ in ()).throw(
                NotImplementedError("Expectation cannot be implemented for division.")
            )
            result.variance = lambda: (_ for _ in ()).throw(
                NotImplementedError("Variance cannot be implemented for division.")
            )
            return result
        return cast(ContinuousRV, super().__truediv__(other))

    def median(self) -> float:
        raise NotImplementedError

    def mode(self) -> float:
        raise NotImplementedError

    def expectation(self) -> float:
        raise NotImplementedError

    def variance(self) -> float:
        raise NotImplementedError

    def pdf(self, x: float) -> float:
        raise NotImplementedError

    def cdf(self, x: float) -> float:
        """
        General implementation of the cdf function, which may be overridden
        in child classes to provide a clearer/more efficient implementation.
        """
        return float(quad(self.pdf, -np.inf, x, full_output=True)[0])
