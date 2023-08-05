#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import numpy as np
from sklearn.utils import check_X_y
from sklearn.utils import check_array
from ReplicatedFocusingBeliefPropagation.lib.Patterns import _Patterns
from ReplicatedFocusingBeliefPropagation.rfbp.misc import _check_string
from ReplicatedFocusingBeliefPropagation.rfbp.misc import get_int_size

__all__ = ['Pattern']

__author__  = ['Nico Curti', "Daniele Dall'Olio"]
__email__   = ['nico.curti2@unibo.it', 'daniele.dallolio@studio.unibo.it']

class Pattern (object):

  '''
  Pattern object for C++ compatibility.
  The Pattern object is just a simple wrap of a data (matrix) + labels (vector).
  This object type provide a compatibility with the rFBP functions in C++ and it provides also a series of checks
  for the input validity.

  Parameters
  ----------
    X : None or 2D array-like or string
      Input matrix of variables as (Nsample, Nfeatures) or filename with the input stored in the same way

    y : None or 1D array-like
      Input labels. The label can be given or read from the input filename as first row in the file.

  Example
  -------
  >>> import numpy as np
  >>> from ReplicatedFocusingBeliefPropagation import Pattern
  >>>
  >>> n_sample, n_feature = (20, 101) # n_feature must be odd
  >>> data = np.random.choice(a=(-1, 1), p=(.5, .5), size=(n_sample, n_feature))
  >>> labels = np.random.choice(a=(-1, 1), p=(.5, .5), size=(n_sample, ))
  >>>
  >>> pt = Pattern(X=data, y=labels)
  >>> # dimensions
  >>> assert pt.shape == (n_sample, n_feature)
  >>> # data
  >>> np.testing.assert_allclose(pt.data, data)
  >>> # labels
  >>> np.testing.assert_allclose(pt.labels, labels)
  '''

  def __init__ (self, X=None, y=None):

    if X is not None and y is not None:

      # check array
      X, y = check_X_y(X, y)
      N, M = X.shape

      X = check_array(X)
      X = X.ravel()

      X = np.ascontiguousarray(X)
      y = np.ascontiguousarray(y)

      X = X.astype('float64')
      y = y.astype(get_int_size())

      self._pattern = _Patterns(X=X, y=y, M=M, N=N)
      self._check_binary()

    else:

      self._pattern = None

  def random (self, shape):
    '''
    Generate Random pattern.
    The pattern is generated using a Bernoulli distribution and thus it creates a data (matrix) + labels (vector)
    of binary values. The values are converted into the range (-1, 1) for the compatibility with the rFBP algorithm.

    Parameters
    ----------
      shapes : tuple
        a 2-D tuple with (M, N) where M is the number of samples and N the number of probes

    Example
    -------
    >>> from ReplicatedFocusingBeliefPropagation import Pattern
    >>>
    >>> n_sample = 10
    >>> n_feature = 20
    >>> data = Pattern().random(shape=(n_sample, n_feature))
    >>> assert data.shape == (n_sample, n_feature)
    >>> data
      Pattern[shapes=(10, 20)]
    '''

    try:
      M, N = map(int, shape)

    except ValueError:
      raise ValueError('Incorrect dimensions. Shapes must be a 2-D tuple with (M, N)')

    if M <= 0 or N <= 0:
      raise ValueError('Incorrect dimensions. M and N must be greater than 0. Given ({0:d}, {1:d})'.format(M, N))

    self._pattern = _Patterns(M=M, N=N)

    # We do not need to check the variables since they are correctly generated into the C++ code!

    return self


  def load (self, filename, binary=False, delimiter='\t'):
    '''
    Load pattern from file.
    This is the main utility of the Pattern object. You can use this function to load data from csv-like files OR from a binary file.

    Parameters
    ----------
      filename : str
        Filename/Path to the Pattern file

      binary : bool
        True if the filename is in binary fmt; False for ASCII fmt

      delimiter : str
        Separator of input file (valid if binary is False)

    Example
    -------
    >>> from ReplicatedFocusingBeliefPropagation import Pattern
    >>>
    >>> data = Pattern().load(filename='path/to/datafile.csv', delimiter=',', binary=False)
    >>> data
      Pattern[shapes=(10, 20)]
    '''

    if not isinstance(filename, str):
      raise ValueError('Invalid filename found. Filename must be a string. Given : {0}'.format(filename))

    filename = _check_string(filename, exist=True)
    delimiter = _check_string(delimiter, exist=False)

    self._pattern = _Patterns(filename=filename, binary=binary, delimiter=delimiter)
    self._check_binary()

    return self

  @property
  def shape (self):
    '''
    Return the shape of the data matrix

    Returns
    -------
      shape: tuple
        The tuple related to the data dimensions (n_sample, n_features)
    '''
    try:
      return (self._pattern.Nrow, self._pattern.Ncol)

    except AttributeError:
      return (0, 0)

  @property
  def labels (self):
    '''
    Return the label array

    Returns
    -------
      labels: array-like
        The labels vector as (n_sample, ) casted to integers.
    '''
    try:
      return np.asarray(self._pattern.labels, dtype=int)

    except AttributeError:
      return None

  @property
  def data (self):
    '''
    Return the data matrix

    Returns
    -------
      data: array-like
        The data matrix as (n_sample, n_features) casted to integers.
    '''
    try:
      return np.asarray(self._pattern.data, dtype=int)

    except AttributeError:
      return None

  @property
  def pattern (self):
    '''
    Return the pattern Cython object

    Returns
    -------
      pattern: Cython object
        The cython object wrapped by the Pattern class

    Notes
    -----
    .. warning::
      We discourage the use of this property if you do not know exactly what you are doing!
    '''
    return self._pattern

  def _check_binary (self):
    '''
    Check if the input data and labels satisfy the binary
    requirements
    '''

    if not (((-1 == self.data) | (1 == self.data)).all() or ((-1 == self.labels) | (1 == self.labels)).all()):
      self._pattern = None # remove the loaded object
      raise ValueError('Invalid input parameters! Input variables must be +1 or -1')

  def __repr__ (self):
    '''
    Object representation
    '''
    class_name = self.__class__.__qualname__
    if self._pattern is not None:
      return '{0}[shapes=({1:d}, {2:d})]'.format(class_name, self._pattern.Nrow, self._pattern.Ncol)

    else:
      return '{0}[shapes=(0, 0)]'.format(class_name)
