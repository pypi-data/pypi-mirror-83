# distutils: language = c++
# cython: language_level=2

from libcpp cimport bool
from libcpp.string cimport string

from Patterns cimport Patterns
from FocusingProtocol cimport FocusingProtocol

cdef extern from "rfbp.h" nogil:

  cdef long int ** focusingBP[Mag](const long int & K,
                                   const Patterns & patterns,
                                   const long int & max_iters,
                                   const long int & max_steps,
                                   const long int & seed,
                                   const double & damping,
                                   const string & accuracy1,
                                   const string & accuracy2,
                                   const double & randfact,
                                   const FocusingProtocol & fprotocol,
                                   const double & epsil,
                                   int nth#,
                                   #string outfile=*,
                                   #string outmessfiletmpl=*,
                                   #string initmess=*,
                                   #const bool & bin_mess=*
                                   );

  cdef long int * nonbayes_test(long int ** sign_m_j_star, const Patterns & patterns, const long int & K);

