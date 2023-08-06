#!/usr/bin/env python
"""
The algorithms here are partially based on methods described in:
[The Fisher-Bingham Distribution on the Sphere, John T. Kent
Journal of the Royal Statistical Society. Series B (Methodological)
Vol. 44, No. 1 (1982), pp. 71-80 Published by: Wiley
Article Stable URL: http://www.jstor.org/stable/2984712]

The example code in example.py serves not only as an example
but also as a test. It performs some higher level tests but it also
generates example plots if called directly from the shell.
"""

from __future__ import print_function
import sys
import warnings
import logging

import numpy as np
from scipy.optimize import minimize, basinhopping
from scipy.special import gamma as G
from scipy.special import gammaln as LG
from scipy.special import iv as I
from scipy.special import ivp as DI
from scipy.special import hyp2f1 as H2F1
from scipy.special import hyp1f1 as H1F1
from scipy.special import hyp0f1 as H0F1
from scipy.stats import uniform
from scipy.integrate import dblquad, IntegrationWarning
# to avoid confusion with the norm of a vector we give the normal distribution a less confusing name here
from scipy.stats import norm as gauss
import scipy.linalg
from scipy.linalg import eig


# helper function
def MMul(A, B):
    return np.matmul(A, B)


def norm(x, axis=None):
    """
    helper function to compute the L2 norm. scipy.linalg.norm is not used because this function does not allow to choose an axis
    """
    if isinstance(x, list) or isinstance(x, tuple):
        x = np.array(x)
    return np.sqrt(np.sum(x * x, axis=axis))


def fb8(theta, phi, psi, kappa, beta, eta=1., alpha=0., rho=0.):
    """
    Generates the FB8 distribution based on the spherical coordinates theta, phi, psi
    with the concentration parameter kappa and the ovalness beta
    """
    gamma1, gamma2, gamma3 = FB8Distribution.spherical_coordinates_to_gammas(
        theta, phi, psi)
    nu = FB8Distribution.spherical_coordinates_to_nu(alpha, rho)
    return FB8Distribution(gamma1, gamma2, gamma3, kappa, beta, eta, nu)


def fb82(gamma1, gamma2, gamma3, kappa, beta, eta=1., nu=None):
    """
    Generates the FB8 distribution using the orthonormal vectors gamma1,
    gamma2 and gamma3, with the concentration parameter kappa and the ovalness beta
    """
    assert np.abs(np.inner(gamma1, gamma2)) < 1E-10
    assert np.abs(np.inner(gamma2, gamma3)) < 1E-10
    assert np.abs(np.inner(gamma3, gamma1)) < 1E-10
    return FB8Distribution(gamma1, gamma2, gamma3, kappa, beta, eta, nu)


def fb83(A, B, eta=1., nu=None):
    """
    Generates the FB8 distribution using the orthogonal vectors A and B
    where A = gamma1*kappa and B = gamma2*beta (gamma3 is inferred)
    A may have not have length zero but may be arbitrarily close to zero
    B may have length zero however. If so, then an arbitrary value for gamma2
    (orthogonal to gamma1) is chosen
    """
    kappa = norm(A)
    beta = norm(B)
    gamma1 = A / kappa
    if beta == 0.0:
        gamma2 = __generate_arbitrary_orthogonal_unit_vector(gamma1)
    else:
        gamma2 = B / beta
    theta, phi, psi = FB8Distribution.gammas_to_spherical_coordinates(
        gamma1, gamma2)
    gamma1, gamma2, gamma3 = FB8Distribution.spherical_coordinates_to_gammas(
        theta, phi, psi)
    return FB8Distribution(gamma1, gamma2, gamma3, kappa, beta, eta, nu)


def fb84(Gamma, kappa, beta, eta=1., nu=None):
    """
    Generates the fb8 distribution
    """
    gamma1 = Gamma[:, 0]
    gamma2 = Gamma[:, 1]
    gamma3 = Gamma[:, 2]
    return fb82(gamma1, gamma2, gamma3, kappa, beta, eta, nu)


def __generate_arbitrary_orthogonal_unit_vector(x):
    v1 = np.cross(x, np.array([1.0, 0.0, 0.0]))
    v2 = np.cross(x, np.array([0.0, 1.0, 0.0]))
    v3 = np.cross(x, np.array([0.0, 0.0, 1.0]))
    v1n = norm(v1)
    v2n = norm(v2)
    v3n = norm(v3)
    v = [v1, v2, v3][np.argmax([v1n, v2n, v3n])]
    return v / norm(v)


class FB8Distribution(object):
    minimum_value_for_kappa = 1E-6

    @staticmethod
    def create_matrix_H(theta, phi):
        theta = np.asarray(theta)
        phi = np.asarray(phi)
        _H = np.array([
            [np.cos(theta),          -np.sin(theta),         np.zeros(theta.shape)],
            [np.sin(theta) * np.cos(phi), np.cos(theta) * np.cos(phi), -np.sin(phi)],
            [np.sin(theta) * np.sin(phi), np.cos(theta) * np.sin(phi), np.cos(phi)]
        ])
        if len(_H.shape) > 2:
            return np.moveaxis(_H, 2, 0)
        else:
            return _H

    @staticmethod
    def create_matrix_Ht(theta, phi):
        return np.swapaxes(FB8Distribution.create_matrix_H(theta, phi),-2,-1)

    @staticmethod
    def create_matrix_K(psi):
        psi = np.asarray(psi)
        zs = np.zeros(psi.shape)
        os = np.ones(psi.shape)
        _K = np.array([
            [os, zs, zs],
            [zs, np.cos(psi), -np.sin(psi)],
            [zs, np.sin(psi), np.cos(psi)]
        ])
        if len(_K.shape) > 2:
            return np.moveaxis(_K, 2, 0)
        else:
            return _K

    @staticmethod
    def create_matrix_Kt(psi):
        return np.swapaxes(FB8Distribution.create_matrix_K(psi), -2, -1)

    @staticmethod
    def create_matrix_Gamma(theta, phi, psi):
        H = FB8Distribution.create_matrix_H(theta, phi)
        K = FB8Distribution.create_matrix_K(psi)
        return MMul(H, K)

    @staticmethod
    def create_matrix_Gammat(theta, phi, psi):
        return np.swapaxes(FB8Distribution.create_matrix_Gamma(theta, phi, psi), -2, -1)

    @staticmethod
    def spherical_coordinates_to_gammas(theta, phi, psi):
        Gamma = FB8Distribution.create_matrix_Gamma(theta, phi, psi)
        gamma1 = Gamma[..., 0]
        gamma2 = Gamma[..., 1]
        gamma3 = Gamma[..., 2]
        return gamma1, gamma2, gamma3

    @staticmethod
    def spherical_coordinates_to_nu(alpha, rho):
        return FB8Distribution.create_matrix_Gamma(
            alpha, rho, np.zeros(np.asarray(alpha).shape))[..., 0]

    @staticmethod
    def gamma1_to_spherical_coordinates(gamma1):
        theta = np.arccos(gamma1[...,0])
        phi = np.arctan2(gamma1[...,2], gamma1[...,1])
        return theta, phi

    @staticmethod
    def gammas_to_spherical_coordinates(gamma1, gamma2):
        theta, phi = FB8Distribution.gamma1_to_spherical_coordinates(gamma1)
        Ht = FB8Distribution.create_matrix_Ht(theta, phi)
        u = MMul(Ht, gamma2.T.reshape(3, np.asarray(theta).size))
        psi = np.arctan2(u[...,2,:][0], u[...,1,:][0])
        return theta, phi, psi

    def __init__(self, gamma1, gamma2, gamma3, kappa, beta, eta=1., nu=None):
        assert not kappa < 0.
        assert not beta < 0.
        assert not abs(eta) > 1.001
        for gamma in gamma1, gamma2, gamma3:
            assert len(gamma) == 3

        self._gamma1 = np.array(gamma1, dtype=np.float64)
        self._gamma2 = np.array(gamma2, dtype=np.float64)
        self._gamma3 = np.array(gamma3, dtype=np.float64)
        self._kappa = float(kappa)
        self._beta = float(beta)
        # Bingham-Mardia, 4-param, small-circle distribution has eta=-1
        self._eta = float(eta)
        # FB8 param nu
        if nu is None:
            nu = FB8Distribution.spherical_coordinates_to_nu(0,0)
        self._nu = nu

        self._theta, self._phi, self._psi = FB8Distribution.gammas_to_spherical_coordinates(
            self._gamma1, self._gamma2)
        self._alpha, self._rho = FB8Distribution.gamma1_to_spherical_coordinates(self._nu)

        self._cached_rvs = np.empty((0,3))

        # save rvs used to calculated level contours to keep levels self-consistent
        self._level_log_pdf = np.empty((0,))

    @property
    def gamma1(self):
        return self._gamma1

    @property
    def gamma2(self):
        return self._gamma2

    @property
    def gamma3(self):
        return self._gamma3

    @property
    def nu(self):
        return self._nu

    @property
    def kappa(self):
        return self._kappa

    @kappa.setter
    def kappa(self, val):
        self._kappa = val
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def beta(self):
        return self._beta

    @beta.setter
    def beta(self, val):
        self._beta = val
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def eta(self):
        return self._eta

    @eta.setter
    def eta(self, val):
        self._eta = val
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, val):
        self._theta = val
        self._gamma1, self._gamma2, self._gamma3 = self.Gamma.T
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def phi(self):
        return self._phi

    @phi.setter
    def phi(self, val):
        self._phi = val
        self._gamma1, self._gamma2, self._gamma3 = self.Gamma.T
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def psi(self):
        return self._psi

    @psi.setter
    def psi(self, val):
        self._psi = val
        self._gamma1, self._gamma2, self._gamma3 = self.Gamma.T
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        self._alpha = val
        self._nu = FB8Distribution.spherical_coordinates_to_nu(
            self._alpha, self._rho)
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def rho(self):
        return self._rho

    @rho.setter
    def rho(self, val):
        self._rho = val
        self._nu = FB8Distribution.spherical_coordinates_to_nu(
            self._alpha, self._rho)
        self._level_log_pdf = np.empty((0,))
        self._cached_rvs = np.empty((0,3))

    @property
    def Gamma(self):
        return self.create_matrix_Gamma(self.theta, self.phi, self.psi)

    def _nnormalize(self, epsabs=1e-3, epsrel=1e-3):
        """
        Perform numerical integration with dblquad. This function can be used for testing and 
        exception handling in self.normalize
        """
        # numerical integration
        k, b, m = self.kappa, self.beta, self.eta
        n1, n2, n3 = self.nu
        return dblquad(
            lambda th, ph: np.sin(th)*\
            np.exp(k*(n1*np.cos(th)+n2*np.sin(th)*np.cos(ph)+n3*np.sin(th)*np.sin(ph))+\
                   b*np.sin(th)**2*(np.cos(ph)**2-m*np.sin(ph)**2)),
                   0., 2.*np.pi, lambda x: 0., lambda x: np.pi,
                   epsabs=epsabs, epsrel=epsrel)[0]
    
    def normalize(self, cache=dict(), return_num_iterations=False):
        """
        Returns the normalization constant of the FB8 distribution.
        The proportional error may be expected not to be greater than
        1E-11.


        >>> gamma1 = np.array([1.0, 0.0, 0.0])
        >>> gamma2 = np.array([0.0, 1.0, 0.0])
        >>> gamma3 = np.array([0.0, 0.0, 1.0])
        >>> tiny = FB8Distribution.minimum_value_for_kappa
        >>> np.abs(fb82(gamma1, gamma2, gamma3, tiny, 0.0).normalize() - 4*np.pi) < 4*np.pi*1E-12
        True
        >>> for kappa in [0.01, 0.1, 0.2, 0.5, 2, 4, 8, 16]:
        ...     print(np.abs(fb82(gamma1, gamma2, gamma3, kappa, 0.0).normalize() - 4*np.pi*np.sinh(kappa)/kappa) < 1E-15*4*np.pi*np.sinh(kappa)/kappa, end=' ')
        ...
        True True True True True True True True 
        """
        k, b, m = self.kappa, self.beta, self.eta
        n1, n2, n3 = self.nu
        j = 0

        def a_c6(j, b, k, m):
            assert b > 0
            v = j + 0.5
            return (
                    np.exp(
                        np.log(b) * j +
                        + LG(j + 0.5) - LG(j+1) - LG(v+1)
                        )
                    ) * H0F1(v+1, k**2/4) * H2F1(-j, 0.5, 0.5-j, -m)

        def a_c8(jj, kk, ll, b, k, m, n1, n2, n3):
            assert k > 0
            v = jj + ll + kk + 0.5
            z = k*n1
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                ln_n2 = np.log(n2**2) * ll
                ln_n3 = np.log(n3**2) * kk
                ln_b = np.log(b) * jj

            # prevent issues with log for edge cases
            if n2 == 0.:
                ln_n2[ll==0] = 0
            if n3 == 0.:
                ln_n3[kk==0] = 0
            if b == 0.:
                ln_b[jj==0] = 0
            return (
                np.exp(
                    ln_n2 + ln_n3 + ln_b +
                    np.log(k) * 2 * (ll+kk) -
                    LG(2 * ll + 1) - LG(2 * kk + 1) - LG(jj + 1) +
                    LG(jj + ll + 0.5) + LG(kk + 0.5) - LG(v + 1)
                    ) * H0F1(v+1, z**2/4) * H2F1(-jj, kk+0.5, 0.5-jj-ll, -m)
                ) / np.sqrt(np.pi)
        
        if (k, b, m, n1, n2) not in cache:
            result = 0.
            if b == 0. and k == 0.:
                result = 2
            # FB6 or BM4-with-eta
            # This is faster than the full FB8 sum
            elif n1 == 1. or k == 0.:
                # exact solution (vmF)
                if b == 0.0:
                    result = 2/k * np.sinh(k)
                else:
                    prev_abs_a = 0
                    while True:
                        js = np.arange(j*100,(j+1)*100)
                        a = a_c6(js, b, k, m)
                        evens = js % 2==0
                        if np.any(a[evens] < 0):
                            logging.info('a < 0 for even j, masking. This is due to an inaccuracy in H2F1')
                            # hack around H2F1 inaccuracy
                            a[(evens) & (a < 0)] = 0
                        sa = a.sum()
                        abs_sa = np.abs(sa).sum()
                        ### DEBUG ###
                        # print j, sa
                        result += sa
                        if np.isnan(result):
                            logging.warning('Series result is nan')
                            raise RuntimeWarning
                        if np.isinf(result):
                            logging.warning('Series result is infinity')
                            raise RuntimeWarning
                        j += 1
                        if abs_sa < np.abs(result) * 1E-12 and abs_sa <= prev_abs_a:
                            break
                        prev_abs_a = abs_sa
            # FB8
            else:
                try:
                    ll = 0
                    prev_abs_sa_ll = 0
                    _l, _k, _j = (14,)*3
                    _jjs, _kks, _lls = np.mgrid[0:_j,0:_k,0:_l]
                    while True:
                        curr_abs_sa_ll = 0
                        kk = 0
                        prev_abs_sa_kk = 0
                        while True:
                            curr_abs_sa_kk = 0
                            jj = 0
                            prev_abs_sa_jj = 0
                            while True:
                                jjs = jj*_j+_jjs
                                a = a_c8(jjs, kk*_k+_kks, ll*_l+_lls, b, k, m, n1, n2, n3)
                                evens = jjs%2==0
                                if np.any(a[evens] < 0):
                                    logging.info('a < 0 for even j, masking. This is due to an inaccuracy in H2F1.')
                                    # hack around H2F1 inaccuracy
                                    a[(evens) & (a < 0)] = 0
                                sa = a.sum()
                                abs_sa = np.abs(a).sum()
                                ### DEBUG ###
                                # print ll, kk, jj, sa, abs_sa
                                # print j, a, I(j+0.5, k)
                                curr_abs_sa_kk += abs_sa
                                curr_abs_sa_ll += abs_sa
                                result += sa
                                if np.isnan(result):
                                    logging.warning('Series result is nan')
                                    raise RuntimeWarning
                                j += 1
                                jj += 1
                                if abs_sa < np.abs(result) * 1E-12 and abs_sa <= prev_abs_sa_jj:
                                    break
                                prev_abs_sa_jj = abs_sa
                                ### DEBUG ###
                                # print ll, kk, jj, sa, result
                                # if ll == 13 and kk==1 and jj==0:
                                #     print ll, kk, jj, a, result
                                #     import pdb
                                #     pdb.set_trace()

                            assert not curr_abs_sa_kk < 0
                            ### DEBUG ###
                            # if ll == 2 and kk==44:
                            #     import pdb
                            #     pdb.set_trace()
                            # print ll, kk, curr_abs_sa_kk, result
                            # assert not curr_abs_sa_kk < 0
                            kk += 1
                            if curr_abs_sa_kk < np.abs(result) * 1E-12 and curr_abs_sa_kk <= prev_abs_sa_kk:
                                break
                            prev_abs_sa_kk = curr_abs_sa_kk

                        assert not curr_abs_sa_ll < 0
                        ### DEBUG ###
                        # print ll, curr_abs_sa_ll, result
                        ll += 1
                        if curr_abs_sa_ll < np.abs(result) * 1E-12 and curr_abs_sa_ll <= prev_abs_sa_ll:
                            break
                        prev_abs_sa_ll = curr_abs_sa_ll
                    if not result > 0:
                        logging.warning('Series result not positive')
                        raise RuntimeWarning
                except (RuntimeWarning, OverflowError) as e:
                    logging.warning('Series calculation of normalization failed. Attempting numerical integration... '+self.__repr__())
                    try:
                        # numerical integration
                        result = self._nnormalize()/(2*np.pi)
                    except RuntimeWarning as e:
                        result = np.inf
                    j = -1

            cache[k, b, m, n1, n2] = 2 * np.pi * result

        if return_num_iterations:
            return cache[k, b, m, n1, n2], j
        else:
            return cache[k, b, m, n1, n2]

    def _approx_log_normalize(self):
        """
        >>> from itertools import product
        >>> for x in product([0], [0], [0], range(10, 200, 10),
        ...                 range(10, 200, 10),
        ...                 np.linspace(-1, 1, 5), [0], [0]):
        ...    lnorm = np.log(fb8(*x).normalize())
        ...    lnormapprox = fb8(*x)._approx_log_normalize()
        ...    if np.abs(lnorm-lnormapprox)/lnorm > 0.1:
        ...        print(fb8(*x), lnorm, lnormapprox)
        """
        assert self.nu[0] == 1. # should only reach here if it's FB6
        k = self.kappa
        b = self.beta
        m = self.eta
        if k > 2 * b:
            lnormalize = np.log(2 * np.pi) + k - \
                np.log((k - 2 * b) * (k + 2 * b * m)) / 2.
        else:
            # normal approximation in z = cos(theta) with correction factor for floating eta
            # correction factor by fixing sin(theta)**2 = (1-k**2/(4*b**2)), corresponding to theta_max
            # Written in terms of 1F1 using A&S (13.1.27) in which
            # I(0, z) = M(1/2, 1, -2z) exp(z)
            _ = k**2/(4*b**2)
            z = (1+m) * b * (1-_)/2
            lnormalize = ((np.log(np.pi) - np.log(b))/2 + b*(1+_) + 
                              np.log(2*np.pi) +np.log(H1F1(1/2., 1., -2*z)))

        return lnormalize
        
    def log_normalize(self):
        """
        Returns the logarithm of the normalization constant.


        >>> from itertools import product
        >>> for x in product([0], [0], [0], [0, 2, 32, 128, 256],
        ...                  [0, 2, 32, 128, 256], np.linspace(-1, 1, 5),
        ...                  np.linspace(0.0, np.pi, 3),
        ...                  np.linspace(0, np.pi/3, 3)):
        ...    lnorm = fb8(*x).log_normalize()
        ...    lnnorm = np.log(fb8(*x)._nnormalize())
        ...    if np.abs(lnorm-lnnorm)/lnorm > 0.1:
        ...        print(fb8(*x), lnorm, lnnorm)
        fb8(0.00, 0.00, 0.00, 256.00, 128.00, 1.00, 1.57, 1.05) 337.9290151254215 289.8261422778405
        fb8(0.00, 0.00, 0.00, 256.00, 256.00, 1.00, 1.57, 1.05) 466.23216200690393 400.40834745629957
        """
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            try:
                return np.log(self.normalize())
            except (OverflowError, RuntimeWarning) as e:
                logging.warning('Series calculation of normalization failed. Approximating normalization... '+self.__repr__())
                return self._approx_log_normalize()

    def max(self):
        k, b, m = self.kappa, self.beta, self.eta
        n1, n2, n3 = self.nu
        if n1 == 1.:
            if self.beta == 0.0:
                x1 = 1
            else:
                x1 = self.kappa / (2 * self.beta)
            if x1 > 1:
                x1 = 1
            x2 = np.sqrt(1 - x1**2)
            x3 = 0
        else:
            # FB8
            # Line search along solution set with BFGS run over x_max
            ntests = 1001
            radicalz = lambda z: 4*m**2*z**2*(z**2-1)*b**2+\
              4*m*z*(z**2-1)*b*k*n1+k**2*((z**2-1)*n1**2+z**2*n3**2)

            curr_max = -np.inf
            x_max = None
            for sgn_0 in [-1,1]:
                for sgn_1 in [-1,1]:
                    x1 = np.linspace(-1,1,ntests)
                    x2 = sgn_0*np.sqrt(-radicalz(x1))/(2*m*x1*b+k*n1)
                    x3 = sgn_1*np.sqrt(1-x1**2-x2**2)

                    x = np.asarray((x1, x2, x3))
                    lpdfs = self.log_pdf(np.dot(self.Gamma, x).T, normalize=False)
                    lpdfs_max = np.nanmax(lpdfs)
                    # print lpdfs_max
                    if lpdfs_max > curr_max:
                        x_max = x.T[np.nanargmax(lpdfs)]
                        curr_max = lpdfs_max

            f = lambda x: -k*(
                n1*np.cos(x[0])+n2*np.sin(x[0])*np.cos(x[1])+n3*np.sin(x[0])*np.sin(x[1])) -\
                b*np.sin(x[0])**2*(np.cos(x[1])**2-m*np.sin(x[1])**2)
            _x = minimize(f, self.gamma1_to_spherical_coordinates(x_max))
            if not _x.success:
                warning_message = _x.message
                warnings.warn(warning_message, RuntimeWarning)
            x1,x2,x3= self.spherical_coordinates_to_nu(*_x.x)

        x = np.dot(self.Gamma, np.asarray((x1, x2, x3)))
        return FB8Distribution.gamma1_to_spherical_coordinates(x)

    def pdf_max(self, normalize=True):
        return np.exp(self.log_pdf_max(normalize))

    def log_pdf_max(self, normalize=True):
        """
        Returns the maximum value of the log(pdf)
        """
        return self.log_pdf(FB8Distribution.spherical_coordinates_to_nu(
            *self.max()),normalize)

    def pdf(self, xs, normalize=True):
        """
        Returns the pdf of the fb8 distribution for 3D vectors that
        are stored in xs which must be an array of N x 3 or N x M x 3
        N x M x P x 3 etc.

        The code below shows how points in the pdf can be evaluated. An integral is
        calculated using random points on the sphere to determine wether the pdf is
        properly normalized.

        >>> from numpy.random import seed
        >>> from scipy.stats import norm as gauss
        >>> seed(666)
        >>> num_samples = 400000
        >>> xs = gauss(0, 1).rvs((num_samples, 3))
        >>> xs = np.divide(xs, np.reshape(norm(xs, 1), (num_samples, 1)))
        >>> assert np.abs(4*np.pi*np.average(fb8(1.0, 1.0, 1.0, 4.0,  2.0).pdf(xs)) - 1.0) < 0.01
        >>> assert np.abs(4*np.pi*np.average(fb8(1.0, 2.0, 3.0, 4.0,  2.0).pdf(xs)) - 1.0) < 0.01
        >>> assert np.abs(4*np.pi*np.average(fb8(1.0, 2.0, 3.0, 4.0,  8.0).pdf(xs)) - 1.0) < 0.01
        >>> assert np.abs(4*np.pi*np.average(fb8(1.0, 2.0, 3.0, 16.0, 8.0).pdf(xs)) - 1.0) < 0.01
        """
        return np.exp(self.log_pdf(xs, normalize))

    def log_pdf(self, xs, normalize=True):
        """
        Returns the log(pdf) of the fb8 distribution.
        """
        g1x, g2x, g3x = MMul(self.Gamma.T, np.asarray(xs).T)
        k, b, m = self.kappa, self.beta, self.eta
        ngx = self.nu.dot(np.asarray([g1x, g2x, g3x]))

        f = k * ngx + b * (g2x**2 - m * g3x**2)
        if normalize:
            return f - self.log_normalize()
        else:
            return f

    def log_likelihood(self, xs):
        """
        Returns the log likelihood for xs.
        """
        retval = self.log_pdf(xs)
        return sum(retval, len(np.shape(retval)) - 1)

    def _rvs_helper(self):
        num_samples = 10000
        xs = gauss(0, 1).rvs((num_samples, 3))
        xs = np.divide(xs, np.reshape(norm(xs, 1), (num_samples, 1)))
        lpvalues = self.log_pdf(xs, normalize=False)
        lfmax = self.log_pdf_max(normalize=False)
        ## DEBUG
        # print lfmax, lpvalues.max()
        # assert lfmax > lpvalues.max()
        ## END
        shifted = lpvalues - lfmax
        return xs[uniform(0, 1).rvs(num_samples) < np.exp(shifted)]

    def rvs(self, n_samples=None):
        """
        Returns random samples from the FB8 distribution by rejection sampling.
        May become inefficient for large kappas.

        The returned random samples are 3D unit vectors.
        If n_samples == None then a single sample x is returned with shape (3,)
        If n_samples is an integer value N then N samples are returned in an array with shape (N, 3)
        """
        num_samples = 1 if n_samples == None else n_samples
        rvs = self._cached_rvs
        while len(rvs) < num_samples:
            new_rvs = self._rvs_helper()
            rvs = np.concatenate([rvs, new_rvs])
        if n_samples == None:
            self._cached_rvs = rvs[1:]
            return rvs[0]
        else:
            self._cached_rvs = rvs[num_samples:]
            retval = rvs[:num_samples]
            return retval

    def level(self, percentile=50, n_samples=10000):
        """
        Returns the -log_pdf level at percentile by generating a set of rvs and their log_pdfs
        """
        if 0 <= percentile < 100:
            curr_len = self._level_log_pdf.size
            if curr_len < n_samples:
                new_rvs = self.rvs(n_samples)
                self._level_log_pdf = -self.log_pdf(new_rvs)
                self._level_log_pdf.sort()
            log_pdf = self._level_log_pdf
            loc = (log_pdf.size - 1) * percentile / 100.
            idx, frac = int(loc), loc - int(loc)
            return log_pdf[idx] + frac * (log_pdf[idx + 1] - log_pdf[idx])
        else:
            print('{} percentile out of bounds'.format(percentile))
            return nan

    def contour(self, percentile=50):
        """
        Returns the (spherical) coordinates that correspond to a contour percentile

        Solution is based on Eq 1.4 (Kent 1982)
        """
        k = self.kappa
        b = self.beta
        m = self.eta
        ln = self.log_normalize()
        lev = self.level(percentile)

        # FB6, exact
        if self.nu[0] == 1.:
            # work in coordinate system x' = Gamma'*x
            # range over which x1 remains real is [-x2_max, x2_max]
            # assume -1 < m < 1
            x2_max = min(np.abs(np.sqrt(k**2 + 4 * b * m * (b * m - lev + ln)
                                ) / (2 * np.sqrt(m * (1 + m)) * b)), 1)
            if np.isnan(x2_max):
                x2_max = 1
            x2 = np.linspace(-x2_max, x2_max, 10000)
            if np.abs(m) < 1E-4:
                x1_0 = -(lev - ln + b * x2**2) / k
                x1_1 = x1_0
            else:
                x1_0 = (-k + np.sqrt(k**2 + 4 * m * b * (m * b - lev +
                                                      ln - (1 + m) * b * x2**2))) / (2 * b * m)
                x1_1 = (-k - np.sqrt(k**2 + 4 * m * b * (m * b - lev +
                                                      ln - (1 + m) * b * x2**2))) / (2 * b * m)
            x3_0 = np.sqrt(1 - x1_0**2 - x2**2)
            x3_1 = np.sqrt(1 - x1_1**2 - x2**2)
            x2 = np.concatenate([x2, -x2, x2, -x2])
            x1 = np.concatenate([x1_0, x1_0, x1_1, x1_1])
            x3 = np.concatenate([x3_0, -x3_0, x3_1, -x3_1])

            # Since Kent distribution is well-defined for points not on a sphere,
            # possible solutions for L=-log_pdf(kent) extend beyond surface of
            # sphere. For the contour evaluation, only use points that lie on sphere.
            ok = x1**2 + x2**2 <= 1
            x123 = np.asarray((x1[ok], x2[ok], x3[ok]))

            # rotate back into x coordinates
            x = np.dot(self.Gamma, x123).T
        # FB8 approximate
        else:
            npts = 10000
            rvs = self.rvs(npts)
            x = rvs[np.argsort(np.abs(lev+self.log_pdf(rvs)))[:200]]
        return FB8Distribution.gamma1_to_spherical_coordinates(x)

    def __repr__(self):
        return 'fb8({:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f})'.format(self.theta, self.phi, self.psi, self.kappa, self.beta, self.eta, self.alpha, self.rho)


def kent_me(xs):
    """Generates and returns a FB8Distribution based on a FB5 (Kent) moment estimation."""
    lenxs = len(xs)
    xbar = np.average(xs, 0)  # average direction of samples from origin
    # dispersion (or covariance) matrix around origin
    S = np.average(xs.reshape((lenxs, 3, 1)) * xs.reshape((lenxs, 1, 3)), 0)
    # has unit length and is in the same direction and parallel to xbar
    gamma1 = xbar / norm(xbar)
    theta, phi = FB8Distribution.gamma1_to_spherical_coordinates(gamma1)

    H = FB8Distribution.create_matrix_H(theta, phi)
    Ht = FB8Distribution.create_matrix_Ht(theta, phi)
    B = MMul(Ht, MMul(S, H))

    eigvals, eigvects = eig(B[1:, 1:])
    eigvals = np.real(eigvals)
    if eigvals[0] < eigvals[1]:
        eigvals[0], eigvals[1] = eigvals[1], eigvals[0]
        eigvects = eigvects[:, ::-1]
    K = np.diag([1.0, 1.0, 1.0])
    K[1:, 1:] = eigvects

    G = MMul(H, K)
    Gt = np.swapaxes(G,-2,-1)
    T = MMul(Gt, MMul(S, G))

    r1 = norm(xbar)
    t22, t33 = T[1, 1], T[2, 2]
    r2 = t22 - t33

    # kappa and beta can be estimated but may not lie outside their permitted ranges
    min_kappa = FB8Distribution.minimum_value_for_kappa
    kappa = max(min_kappa, 1.0 / (2.0 - 2.0 * r1 - r2) +
                1.0 / (2.0 - 2.0 * r1 + r2))
    beta = 0.5 * (1.0 / (2.0 - 2.0 * r1 - r2) - 1.0 / (2.0 - 2.0 * r1 + r2))

    return fb84(G, kappa, beta)


def __fb8_mle_output1(k_me, callback):
    print()
    print("******** Maximum Likelihood Estimation ********")
    print("Initial estimates are:")
    print("theta =", k_me.theta)
    print("phi   =", k_me.phi)
    print("psi   =", k_me.psi)
    print("kappa =", k_me.kappa)
    print("beta  =", k_me.beta)
    print("eta   =", k_me.eta)
    print("alpha =", k_me.alpha)
    print("rho   =", k_me.rho)
    print("******** Starting the Gradient Descent ********")
    print("[iteration]   fb8(theta, phi, psi, kappa, beta, eta, alpha, rho)   -L")


def fb8_mle(xs, verbose=False, return_intermediate_values=False, warning='warn', fb5_only=False):
    """
    Generates a FB8Distribution fitted to xs using maximum likelihood estimation
    For a first approximation kent_me() is used. The function
    -k.log_likelihood(xs)/len(xs) (where k is an instance of FB8Distribution) is
    minimized.

    Input:
      - xs: values on the sphere to be fitted by MLE, ordering is (z, x, y)
      - verbose: if True, output is given for every step
      - return_intermediate_values: if true the values of all intermediate steps
        are returned as well
      - warning: choices are
        - "warn": issues any warning via warning.warn
        - a file object: which results in any warning message being written to a file
          (e.g. stdout)
        - "none": or any other value for this argument results in no warnings to be issued
    Output:
      - an instance of the fitted FB8Distribution
    Extra output:
      - if return_intermediate_values is specified then
      a tuple is returned with the FB8Distribution argument as the first element
      and containing the extra requested values in the rest of the elements.
    """
    # method that generates the minus L to be minimized
    # x = theta phi psi kappa beta eta alpha rho
    def minus_log_likelihood(x):
        if np.any(np.isnan(x)):
            return np.inf
        if x[3] < 0 or x[4] < 0:
            return np.inf
        ### DEBUG ###
        # if len(x) > 5 and (x[5] > 1 or x[5] < -1):
        #     return np.inf
        return -fb8(*x).log_likelihood(xs) / len(xs)

    # callback for keeping track of the values
    intermediate_values = list()

    def callback(x, output_count=[0]):
        kx = fb8(*x)
        minusL = -kx.log_likelihood(xs)
        imv = intermediate_values
        imv.append((x, minusL))
        if verbose:
            print(len(imv), kx, minusL)

    # first get estimated moments
    k_me = kent_me(xs)
    theta, phi, psi, kappa, beta = k_me.theta, k_me.phi, k_me.psi, k_me.kappa, k_me.beta

    # here the mle is done
    x_start = np.array([theta, phi, psi, kappa, beta])
    y_start = np.array([theta, phi, psi, beta, kappa, -0.99])

    # First try a FB5 fit
    # constrain kappa, beta >= 0 and 2*beta <= kappa for FB5 (Kent 1982)
    if verbose:
        __fb8_mle_output1(fb8(*x_start), callback)
    cons = ({"type": "ineq",
             "fun": lambda x: x[3] - 2 * x[4]},
            {"type": "ineq",
             "fun": lambda x: x[3]},
            {"type": "ineq",
             "fun": lambda x: x[4]})
    all_values = minimize(minus_log_likelihood,
                          x_start,
                          method="SLSQP",
                          constraints=cons,
                          callback=callback,
                          options={"disp": False, "ftol": 1e-08,
                                   "maxiter": 100})

    if not fb5_only:
        # Then try a FB6 fit with seed: eta = -0.99
        # note eta=-1 with 2*beta >= kappa is the small-circle distribution (Bingham-Mardia 1978)
        if verbose:
            __fb8_mle_output1(fb8(*y_start), callback)
        ### constraint for SLSQP ###
        # cons = ({"type": "ineq", # kappa >= 0
        #          "fun": lambda x: x[3]},
        #         {"type": "ineq", # beta >= 0
        #          "fun": lambda x: x[4]},
        #         {"type": "ineq", # -1 <= eta <=1
        #          "fun": lambda x: 1 - np.abs(x[5])})
        #         # {"type": "ineq",
        #         #  "fun": lambda x: -x[3] + 2 * x[4]})
        _y = minimize(minus_log_likelihood,
                      y_start,
                      method="L-BFGS-B",
                      bounds=list(zip([None]*5+[-1,], [None]*5+[1,])),
                      callback=callback)

        # default seed
        z_starts = [np.array([theta, phi, psi, beta, kappa, -0.9, np.pi/4, 0]),]
        # Choose better of FB5 vs FB6 as another seed for FB8
        # Last three parameters determine if FB5, FB6, or FB8
        if _y.success and _y.fun < all_values.fun:
            all_values = _y
            z_starts.append(np.concatenate((_y.x, [0.,0.])))
        else:
            z_starts.append(np.concatenate((all_values.x, [0.9,0.,0.])))

        for z_start in z_starts:
            if verbose:
                __fb8_mle_output1(fb8(*z_start), callback)
            # _z = basinhopping(minus_log_likelihood,
            #                   z_start,
            #                   niter=10,
            #                   niter_success=3,
            #                   minimizer_kwargs= dict(
            #                       method="L-BFGS-B",
            #                       callback=callback,
            #                       options={"disp": False,
            #                                "maxiter": 100})).lowest_optimization_result
            _z = minimize(minus_log_likelihood,
                      z_start,
                      method="L-BFGS-B",
                      bounds=list(zip([None]*5+[-1,]+[None]*2, [None]*5+[1,]+[None]*2)),
                      callback=callback,
                      options={'ftol':1e-8, 'gtol':1e-4})
            if _z.success and _z.fun < all_values.fun:
                all_values = _z
    if not all_values.success:
        warning_message = all_values.message
        if warning == "warn":
            warnings.warn(warning_message, RuntimeWarning)
        if hasattr(warning, "write"):
            warning.write("Warning: " + warning_message + "\n")

    k = (fb8(*all_values.x),)
    if return_intermediate_values:
        k += (intermediate_values,)
    if len(k) == 1:
        k = k[0]
    return k


if __name__ == "__main__":
    __doc__ += """
>>> import numpy as np
>>> from sphere.example import test_example_normalization, test_example_mle, test_example_mle2
>>> from numpy.random import seed
>>> test_example_normalization(gridsize=10)
Calculating the matrix M_ij of values that can be calculated: kappa=100.0*i+1, beta=100.0*j+1
with eta=1.0, alpha=0.0, rho=0.0
Calculating normalization factor for combinations of kappa and beta:
Iterations necessary to calculate normalize(kappa, beta):
  2   3   5   6   7   8   9  10   x   x
  2   3   4   6   7   8   9  10   x   x
  2   3   4   6   7   8   9   x   x   x
  2   2   4   5   7   8   9   x   x   x
  2   2   3   5   6   7   9   x   x   x
  2   2   2   4   6   7   8   x   x   x
  2   2   2   3   5   7   x   x   x   x
  2   2   2   3   4   x   x   x   x   x
  x   x   x   x   x   x   x   x   x   x
  x   x   x   x   x   x   x   x   x   x

>>> logging.getLogger().setLevel('ERROR')
>>> test_example_normalization(gridsize=10,alpha=0.5)
Calculating the matrix M_ij of values that can be calculated: kappa=100.0*i+1, beta=100.0*j+1
with eta=1.0, alpha=0.5, rho=0.0
Calculating normalization factor for combinations of kappa and beta:
Iterations necessary to calculate normalize(kappa, beta):
  6  25  42  57  73  88 103 119   x   x
 12  65 110 153 192 233 273   x   x   x
 18  83 150 234 304 367 434   x   x   x
 21  95 181 286 374 457   x   x   x   x
 24  96 202 304 433   x   x   x   x   x
 30  99 202 338   x   x   x   x   x   x
 33 100 215   x   x   x   x   x   x   x
 36   x   x   x   x   x   x   x   x   x
  x   x   x   x   x   x   x   x   x   x
  x   x   x   x   x   x   x   x   x   x
>>> logging.getLogger().setLevel('WARNING')

A test to ensure that the vectors gamma1 ... gamma3 are orthonormal
>>> ks = [
...   fb8(0.0,      0.0,      0.0,    20.0, 0.0),
...   fb8(-0.25*np.pi, -0.25*np.pi, 0.0,    20.0, 0.0),
...   fb8(-0.25*np.pi, -0.25*np.pi, 0.0,    20.0, 5.0),
...   fb8(0.0,      0.0,      0.5*np.pi, 10.0, 7.0),
...   fb8(0.0,      0.0,      0.5*np.pi, 0.1,  0.0),
...   fb8(0.0,      0.0,      0.5*np.pi, 0.1,  0.1),
...   fb8(0.0,      0.0,      0.5*np.pi, 0.1,  8.0),
... ]
>>> pdf_values = [
...   3.18309886184,
...   0.00909519370,
...   0.09865564569,
...   0.59668931662,
...   0.08780030026,
...   0.08768344462,
...   0.00063128997
... ]
>>> for k in ks:
...   assert(np.abs(np.sum(k.gamma1 * k.gamma2)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma1 * k.gamma3)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma3 * k.gamma2)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma1 * k.gamma1) - 1.0) < 1E-14)
...   assert(np.abs(np.sum(k.gamma2 * k.gamma2) - 1.0) < 1E-14)
...   assert(np.abs(np.sum(k.gamma3 * k.gamma3) - 1.0) < 1E-14)

A test to ensure that the pdf() and the pdf_max() are calculated
correctly.
>>> from numpy.random import seed
>>> from scipy.stats import norm as gauss
>>> seed(666)
>>> for k, pdf_value in zip(ks, pdf_values):
...   assert np.abs(k.pdf(np.array([1.0, 0.0, 0.0])) - pdf_value) < 1E-8
...   assert np.abs(k.log_pdf(np.array([1.0, 0.0, 0.0])) - np.log(pdf_value)) < 1E-8
...   num_samples = 100000
...   xs = gauss(0, 1).rvs((num_samples, 3))
...   xs = np.divide(xs, np.reshape(norm(xs, 1), (num_samples, 1)))
...   values = k.pdf(xs, normalize=False)
...   fmax = k.pdf_max(normalize=False)
...   assert np.all(values <= fmax)
...   assert np.any(values > fmax*0.999)
...   values = k.pdf(xs)
...   fmax = k.pdf_max()
...   assert np.all(values <= fmax)
...   assert np.any(values > fmax*0.999)

These are tests to ensure that the coordinate transformations are done correctly
that the functions that generate instances of FB8Distribution are consistent and
that the derivatives are calculated correctly. In addition some more orthogonality
testing is done.

>>> from distribution import *
>>> from numpy.random import seed
>>> from scipy.stats import uniform
>>> def test_orth(k):
...   # a bit more orthonormality testing for good measure
...   assert(np.abs(np.sum(k.gamma1 * k.gamma2)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma1 * k.gamma3)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma3 * k.gamma2)) < 1E-14)
...   assert(np.abs(np.sum(k.gamma1 * k.gamma1) - 1.0) < 1E-14)
...   assert(np.abs(np.sum(k.gamma2 * k.gamma2) - 1.0) < 1E-14)
...   assert(np.abs(np.sum(k.gamma3 * k.gamma3) - 1.0) < 1E-14)
...
>>> # generating some specific boundary values and some random values
>>> seed(666)
>>> upi, u2pi = uniform(0, np.pi), uniform(-np.pi, 2*np.pi)
>>> thetas, phis, psis = list(upi.rvs(925)), list(u2pi.rvs(925)), list(u2pi.rvs(925))
>>> for a in (0.0, 0.5*np.pi, np.pi):
...   for b in (-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi):
...     for c in (-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi):
...       thetas.append(a)
...       phis.append(b)
...       psis.append(c)
...
>>> # testing consintency of angles (specifically kent())
>>> for theta, phi, psi in zip(thetas, phis, psis):
...   k = fb8(theta, phi, psi, 1.0, 1.0)
...   assert np.abs(theta - k.theta) < 1E-12
...   a = np.abs(phi - k.phi)
...   b = np.abs(psi - k.psi)
...   if theta != 0 and theta != np.pi:
...     assert a < 1E-12 or np.abs(a-2*np.pi) < 1E-12
...     assert b < 1E-12 or np.abs(b-2*np.pi) < 1E-12
...   test_orth(k)
...
>>> # testing consistency of gammas and consistency of back and forth
>>> # calculations between gammas and angles (specifically fb82(), fb83() and fb84())
>>> kappas = gauss(0, 2).rvs(1000)**2
>>> betas = gauss(0, 2).rvs(1000)**2
>>> for theta, phi, psi, kappa, beta in zip(thetas, phis, psis, kappas, betas):
...   gamma1, gamma2, gamma3 = FB8Distribution.spherical_coordinates_to_gammas(theta, phi, psi)
...   theta, phi, psi = FB8Distribution.gammas_to_spherical_coordinates(gamma1, gamma2)
...   gamma1a, gamma2a, gamma3a = FB8Distribution.spherical_coordinates_to_gammas(theta, phi, psi)
...   assert np.all(np.abs(gamma1a-gamma1) < 1E-12)
...   assert np.all(np.abs(gamma2a-gamma2) < 1E-12)
...   assert np.all(np.abs(gamma3a-gamma3) < 1E-12)
...   k2 = fb82(gamma1, gamma2, gamma3, kappa, beta)
...   assert np.all(np.abs(gamma1 - k2.gamma1) < 1E-12)
...   assert np.all(np.abs(gamma2 - k2.gamma2) < 1E-12)
...   assert np.all(np.abs(gamma3 - k2.gamma3) < 1E-12)
...   A = gamma1*kappa
...   B = gamma2*beta
...   k3 = fb83(A, B)
...   assert np.all(np.abs(gamma1 - k3.gamma1) < 1E-12)
...   assert np.all(np.abs(gamma2 - k3.gamma2) < 1E-12)
...   assert np.all(np.abs(gamma3 - k3.gamma3) < 1E-12)
...   test_orth(k)
...   gamma = np.array([
...     [gamma1[0], gamma2[0], gamma3[0]],
...     [gamma1[1], gamma2[1], gamma3[1]],
...     [gamma1[2], gamma2[2], gamma3[2]],
...   ])
...   k4 = fb84(gamma, kappa, beta)
...   assert np.all(k2.gamma1 == k4.gamma1)
...   assert np.all(k2.gamma2 == k4.gamma2)
...   assert np.all(k2.gamma3 == k4.gamma3)
...
>>> # testing special case for B with zero length (fb83())
>>> for theta, phi, psi, kappa, beta in zip(thetas, phis, psis, kappas, betas):
...   gamma1, gamma2, gamma3 = FB8Distribution.spherical_coordinates_to_gammas(theta, phi, psi)
...   A = gamma1*kappa
...   B = gamma2*0.0
...   k = fb83(A, B)
...   assert np.all(np.abs(gamma1 - k.gamma1) < 1E-12)
...   test_orth(k)

>>> # testing property handlers and cache
>>> for k in ks:
...    G = k.Gamma
...    for attr in 'theta phi psi kappa beta eta alpha rho'.split():
...      curr = k.__getattribute__(attr)
...      k.__setattr__(attr, curr*gauss(0,1).rvs())
...      test_orth(k)
...      _ = k.rvs()
...      assert len(k._cached_rvs) > 0
...      k.__setattr__(attr, curr)
...      test_orth(k)
...      assert len(k._cached_rvs) == 0

>>> seed(888)
>>> test_example_mle()
Original Distribution: k = fb8(0.00, 0.00, 0.00, 1.00, 0.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(0.01, -1.57, -1.44, 1.43, 0.00, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(0.01, -1.57, -1.44, 0.96, 0.04, 1.00, 0.00, 0.00)
Original Distribution: k = fb8(0.75, 2.39, 2.39, 20.00, 0.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(0.75, 2.40, -1.51, 20.11, 0.16, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(0.75, 2.40, -1.51, 20.11, 0.18, 1.00, 0.00, 0.00)
Original Distribution: k = fb8(0.79, 2.36, -2.83, 20.00, 2.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(0.78, 2.36, 0.30, 20.24, 1.75, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(0.78, 2.36, 0.30, 20.29, 2.06, 1.00, 0.00, 0.00)
Original Distribution: k = fb8(0.79, 2.36, -2.95, 20.00, 5.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(0.79, 2.36, 0.18, 19.55, 3.85, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(0.79, 2.36, 0.18, 19.94, 4.77, 1.00, 0.00, 0.00)
Original Distribution: k = fb8(1.10, 2.36, -3.04, 50.00, 25.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(1.10, 2.36, 0.10, 37.52, 14.85, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(1.10, 2.36, 0.10, 50.19, 24.98, 1.00, 0.00, 0.00)
Original Distribution: k = fb8(0.00, 0.00, 0.10, 50.00, 25.00, 1.00, 0.00, 0.00)
Drawing 10000 samples from k
Moment estimation:  k_me = fb8(0.00, 0.24, -0.14, 37.71, 14.95, 1.00, 0.00, 0.00)
Fitted with MLE:   k_mle = fb8(0.01, 0.21, -0.11, 50.55, 25.18, 1.00, 0.00, 0.00)
>>> seed(2323)
>>> assert test_example_mle2(300)
Testing various combinations of kappa and beta for 300 samples.
MSE of MLE is higher than 0.7 times the moment estimate for beta/kappa <= 0.2
MSE of MLE is higher than moment estimate for beta/kappa >= 0.3
MSE of MLE is five times higher than moment estimates for beta/kappa >= 0.5
"""

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
