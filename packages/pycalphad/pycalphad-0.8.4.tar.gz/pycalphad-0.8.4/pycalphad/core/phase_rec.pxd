# distutils: language = c++

cimport cython
import numpy
cimport numpy

ctypedef void (*math_function_t)(double*, const double*, void* user_data) nogil

cdef class FastFunction:
    cdef readonly object _objref
    cdef math_function_t f_ptr
    cdef void *func_data
    cdef void call(self, double *out, double *inp) nogil

@cython.final
cdef public class PhaseRecord(object)[type PhaseRecordType, object PhaseRecordObject]:
    cdef FastFunction _obj
    cdef FastFunction _grad
    cdef FastFunction _hess
    cdef FastFunction _internal_cons_func
    cdef FastFunction _internal_cons_jac
    cdef FastFunction _internal_cons_hess
    cdef FastFunction _multiphase_cons_func
    cdef FastFunction _multiphase_cons_jac
    cdef FastFunction _multiphase_cons_hess
    cdef numpy.ndarray _masses
    cdef void** _masses_ptr
    cdef numpy.ndarray _massgrads
    cdef void** _massgrads_ptr
    cdef numpy.ndarray _masshessians
    cdef void** _masshessians_ptr
    cdef public size_t num_internal_cons
    cdef public size_t num_multiphase_cons
    cdef public object variables
    cdef public object state_variables
    cdef public object components
    cdef public object pure_elements
    cdef public object nonvacant_elements
    cdef public double[::1] parameters
    cdef public int phase_dof
    cdef public int num_statevars
    cdef public unicode phase_name
    cpdef void obj(self, double[::1] out, double[::1] dof) nogil
    cpdef void obj_2d(self, double[::1] out, double[:, ::1] dof) nogil
    cpdef void obj_parameters_2d(self, double[:, ::1] out, double[:, ::1] dof, double[:, ::1] parameters) nogil
    cpdef void grad(self, double[::1] out, double[::1] dof) nogil
    cpdef void hess(self, double[:,::1] out, double[::1] dof) nogil
    cpdef void internal_cons_func(self, double[::1] out, double[::1] dof) nogil
    cpdef void internal_cons_jac(self, double[:,::1] out, double[::1] dof) nogil
    cpdef void internal_cons_hess(self, double[:,:,::1] out, double[::1] dof) nogil
    cpdef void multiphase_cons_func(self, double[::1] out, double[::1] dof_with_phasefrac) nogil
    cpdef void multiphase_cons_jac(self, double[:,::1] out, double[::1] dof_with_phasefrac) nogil
    cpdef void multiphase_cons_hess(self, double[:, :, ::1] out, double[::1] dof_with_phasefrac) nogil
    cpdef void mass_obj(self, double[::1] out, double[::1] dof, int comp_idx) nogil
    cpdef void mass_obj_2d(self, double[::1] out, double[:, ::1] dof, int comp_idx) nogil
    cpdef void mass_grad(self, double[::1] out, double[::1] dof, int comp_idx) nogil
    cpdef void mass_hess(self, double[:,::1] out, double[::1] dof, int comp_idx) nogil
    # Used only to reconstitute if pickled (i.e. via __reduce__)
    cdef public object ofunc_
    cdef public object gfunc_
    cdef public object hfunc_
    cdef public object internal_cons_func_
    cdef public object internal_cons_jac_
    cdef public object internal_cons_hess_
    cdef public object multiphase_cons_func_
    cdef public object multiphase_cons_jac_
    cdef public object multiphase_cons_hess_
    cdef public object massfuncs_
    cdef public object massgradfuncs_
    cdef public object masshessianfuncs_
