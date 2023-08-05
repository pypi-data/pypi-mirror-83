#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import pickle
import numpy as np
# import warnings               # for Python non-bayes test version
# from scipy.special import erf # for Python non-bayes test version

from .FocusingProtocol import Focusing_Protocol
from .Patterns import Pattern

from ReplicatedFocusingBeliefPropagation.rfbp.misc import _check_string
from ReplicatedFocusingBeliefPropagation.rfbp.misc import redirect_stdout
from ReplicatedFocusingBeliefPropagation.rfbp.MagP64 import MagP64
from ReplicatedFocusingBeliefPropagation.rfbp.MagT64 import MagT64

from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted
from ReplicatedFocusingBeliefPropagation.lib.rFBP import Mag
from ReplicatedFocusingBeliefPropagation.lib.rFBP import _rfbp
from ReplicatedFocusingBeliefPropagation.lib.rFBP import _nonbayes_test
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin

import multiprocessing

NTH = multiprocessing.cpu_count()

__all__ = ['ReplicatedFocusingBeliefPropagation']

__author__  = ["Nico Curti", "Daniele Dall'Olio"]
__email__   = ['nico.curti2@unibo.it', 'daniele.dallolio@studio.unibo.it']



class ReplicatedFocusingBeliefPropagation (BaseEstimator, ClassifierMixin):

  '''
  ReplicatedFocusingBeliefPropagation classifier

  Parameters
  ----------
    mag : Enum Mag (default = MagP64)
      Switch magnetization type

    hidden : int (default = 3)
      Number of hidden layers

    max_iters : int (default = 1000)
      Number of iterations

    seed : int (default = 135)
      Random seed

    damping : float (default = 0.5)
      Damping parameter

    accuracy : pair of string (default : ('accurate', 'exact'))
      Accuracy of the messages computation at the hidden units level. Possible values are ('exact', 'accurate', 'approx', 'none')

    randfact : float (default = 0.1)
      Seed random generator of Cavity Messages

    epsil : float (default = 0.1)
      Threshold for convergence

    protocol : string (default = 'pseudo_reinforcement')
      Updating protocol. Possible values are ["scoping", "pseudo_reinforcement", "free_scoping", "standard_reinforcement"]

    size : int (default = 101)
      Number of updates

    nth : int (default = max_num_of_cores)
      Number of thread to use in the computation

    verbose : bool (default = False)
      Enable or disable stdout on shell

  Example
  -------
  >>> import numpy as np
  >>> from ReplicatedFocusingBeliefPropagation import ReplicatedFocusingBeliefPropagation as rFBP
  >>>
  >>> N, M = (20, 101) # M must be odd
  >>> data = np.random.choice([-1, 1], p=[.5, .5], size=(N, M))
  >>> label = np.random.choice([-1, 1], p=[.5, .5], size=(N, ))
  >>>
  >>> rfbp = rFBP()
  >>> rfbp.fit(data, label)
    ReplicatedFocusingBeliefPropagation(randfact=0.1, damping=0.5, accuracy=('accurate', 'exact'), nth=1, epsil=0.1, seed=135, size=101, hidden=3, verbose=False, protocol=pseudo_reinforcement, mag=<class 'ReplicatedFocusingBeliefPropagation.rfbp.MagP64.MagP64'>, max_iter=1000)
  >>> predicted_labels = rfbp.predict(data)

  Notes
  -----
  .. note::
    The input data must be composed by binary variables codified as `[-1, 1]`, since the model works only with spin-like variables.

  References
  ----------
  - C. Baldassi, C. Borgs, J. T. Chayes, A. Ingrosso, C. Lucibello, L. Saglietti, and R. Zecchina. "Unreasonable effectiveness of learning neural networks: From accessible states and robust ensembles to basic algorithmic schemes", Proceedings of the National Academy of Sciences, 113(48):E7655-E7662, 2016.
  - C. Baldassi, A. Braunstein, N. Brunel, R. Zecchina. "Efficient supervised learning in networks with binary synapses", Proceedings of the National Academy of Sciences, 104(26):11079-11084, 2007.
  - C. Baldassi, F. Gerace, C. Lucibello, L. Saglietti, R. Zecchina. "Learning may need only a few bits of synaptic precision", Physical Review E, 93, 2016
  - D. Dall'Olio, N. Curti, G. Castellani, A. Bazzani, D. Remondini. "Classification of Genome Wide Association data by Belief Propagation Neural network", CCS Italy, 2019.
  '''

  _ALLOWED_ACCURACY = ('exact', 'accurate', 'approx', 'none')
  _ALLOWED_PROTOCOL = ('scoping', 'pseudo_reinforcement', 'free_scoping', 'standard_reinforcement')

  def __init__ (self, mag=MagP64,
                      hidden=3,
                      max_iter=1000,
                      seed=135,
                      damping=0.5,
                      accuracy=('accurate', 'exact'),
                      randfact=1e-1,
                      epsil=1e-1,
                      protocol='pseudo_reinforcement',
                      size=101,
                      nth=NTH,
                      verbose=False):

    if mag is not MagP64 and mag is not MagT64:
      raise TypeError('Magnetization must be an instance of Mag Enum')

    if len(accuracy) > 2:
      raise TypeError('Too many accuracies given. Max number is two')

    if not all(a in self._ALLOWED_ACCURACY for a in accuracy):
      raise ValueError('Wrong accuracy. Possible values are only {}. Given: {}, {}'.format(','.join(self._ALLOWED_ACCURACY),
                                                                                           accuracy[0], accuracy[1]))
    if protocol not in self._ALLOWED_PROTOCOL:
      raise ValueError('Incorrect Protocol found. Possible values are only {}'.format(','.join(self._ALLOWED_PROTOCOL)))

    self.mag = mag
    self.hidden = hidden
    self.max_iter = max_iter
    self.seed = seed
    self.damping = damping
    self.accuracy = accuracy
    self.randfact = randfact
    self.epsil = epsil
    self.protocol = protocol
    self.size = size
    self.nth = nth
    self.verbose = verbose
    #self.weights_ = None


  def predict (self, X):
    '''
    Predict the new labels computed by ReplicatedFocusingBeliefPropagation model

    Parameters
    ----------
      X : array of shape [n_samples, n_features]
          The input samples.

    Returns
    -------
      y : array of shape [n_samples]
          The predicted target values.
    '''

    check_is_fitted(self, 'weights_')

    if isinstance(X, Pattern):
      testset = X

    else:
      X = check_array(X)
      testset = Pattern(X, [0] * np.shape(X)[0])

    row_size, column_size = self.weights_.shape

    return np.asarray(_nonbayes_test(self.weights_.ravel(), row_size, column_size, testset.pattern, self.hidden))

    # nrow, ncol = np.shape(testset)
    # predicted_labels = np.empty(nrow, dtype=int)
    #
    # with warnings.catch_warnings(): # catch runtime warning due to s2 == 0
    #   warnings.simplefilter("ignore")
    #
    #   for i, Xi in enumerate(testset):
    #     s = sum( [erf( sum([w * x for w, x in zip(Wj, Xi)])  / np.sqrt(2. * sum([ (1 - w * w) * x * x for w, x in zip(Wj, Xi)])))
    #             for Wj in self.weights] )
    #     predicted_labels[i] = np.sign(s)
    # return predicted_labels


  def fit (self, X, y=None):
    '''
    Fit the ReplicatedFocusingBeliefPropagation model meta-transformer

    Parameters
    ----------
      X : array-like of shape (n_samples, n_features)
          The training input samples.

      y : array-like, shape (n_samples,)
          The target values (integers that correspond to classes in
          classification, real numbers in regression).

    Returns
    -------
      self : ReplicatedFocusingBeliefPropagation object
    '''

    pattern = X if isinstance(X, Pattern) else Pattern(X, y)

    acc = (_check_string(acc, exist=False) for acc in self.accuracy)

    protocol = Focusing_Protocol(protocol=self.protocol, size=self.size)

    mag = Mag.MagP64 if self.mag is MagP64 else Mag.MagT64

    with redirect_stdout(self.verbose):
      self.weights_ = _rfbp(mag=mag,
                            pattern=pattern.pattern,
                            protocol=protocol.fprotocol,
                            hidden=self.hidden,
                            max_iter=self.max_iter,
                            max_steps=protocol.num_of_replicas,
                            randfact=self.randfact,
                            damping=self.damping,
                            epsil=self.epsil,
                            accuracy=acc,
                            seed=self.seed,
                            nth=self.nth
                            )

    self.weights_ = np.asarray(self.weights_, dtype=int)

    return self


  def load_weights (self, weightfile, delimiter='\t', binary=False):
    '''
    Load weights from file

    Parameters
    ----------
      weightfile : string
        Filename of weights

      delimiter : char
        Separator for ascii loading

      binary : bool
        Switch between binary and ascii loading style

    Returns
    -------
      self : ReplicatedFocusingBeliefPropagation object

    Example
    -------
    >>> from ReplicatedFocusingBeliefPropagation import ReplicatedFocusingBeliefPropagation as rFBP
    >>>
    >>> clf = rFBP()
    >>> clf.load_weights('path/to/weights_filename.csv', delimiter=',', binary=False)
      ReplicatedFocusingBeliefPropagation(randfact=0.1, damping=0.5, accuracy=('accurate', 'exact'), nth=1, epsil=0.1, seed=135, size=101, hidden=3, verbose=False, protocol=pseudo_reinforcement, mag=<class 'ReplicatedFocusingBeliefPropagation.rfbp.MagP64.MagP64'>, max_iter=1000)
    '''

    if binary:
      with open(weightfile, 'rb') as fp:
        self.weights_ = pickle.load(fp)

    else:
      self.weights_ = np.loadtxt(weightfile, delimiter=delimiter)

    self.hidden = len(self.weights_)

    return self


  def save_weights (self, weightfile, delimiter='\t', binary=False):
    '''
    Load weights from file

    Parameters
    ----------
      weightfile : string
        Filename to dump the weights

      delimiter : char
        Separator for ascii dump

      binary : bool
        Switch between binary and ascii dumping style

    Example
    -------
    >>> import numpy as np
    >>> from ReplicatedFocusingBeliefPropagation import ReplicatedFocusingBeliefPropagation as rFBP
    >>>
    >>> N, M = (20, 101) # M must be odd
    >>> data = np.random.choice([-1, 1], p=[.5, .5], size=(N, M))
    >>> label = np.random.choice([-1, 1], p=[.5, .5], size=(N, ))
    >>>
    >>> rfbp = rFBP()
    >>> rfbp.fit(data, label)
    >>> rfbp.save_weights('path/to/weights_filename.csv', delimiter=',', binary=False)
    '''

    check_is_fitted(self, 'weights_')

    if binary:
      with open(weightfile, 'wb') as fp:
        pickle.dump(self.weights_, fp)

    else:
      np.savetxt(weightfile, self.weights_, delimiter=delimiter)

  def __repr__ (self):
    '''
    Object representation
    '''
    class_name = self.__class__.__qualname__

    params = self.__init__.__code__.co_varnames
    params = set(params) - {'self'}
    args = ', '.join(['{}={}'.format(k, str(getattr(self, k))) for k in params])

    return '{0}({1})'.format(class_name, args)
