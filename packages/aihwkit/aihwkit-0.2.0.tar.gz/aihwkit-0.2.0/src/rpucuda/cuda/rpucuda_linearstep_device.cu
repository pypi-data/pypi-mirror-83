/**
 * (C) Copyright 2020 IBM. All Rights Reserved.
 *
 * This code is licensed under the Apache License, Version 2.0. You may
 * obtain a copy of this license in the LICENSE.txt file in the root directory
 * of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Any modifications or derivative works of this code must retain this
 * copyright notice, and modified files need to carry a notice indicating
 * that they have been altered from the originals.
 */

#include "pwu_kernel_parameter.h"
#include "rpu_pulsed_meta_parameter.h"
#include "rpucuda_linearstep_device.h"
#include <memory>

namespace RPU {

template <typename T> struct UpdateFunctorLinearStepMult {

  __device__ __forceinline__ void operator()(
      T &w,
      uint32_t n,
      uint32_t negative,
      const float4 par_4,
      const float2 lin_slope,
      T &par_1,
      const T *global_par,
      T noise_std_dw,
      curandState &local_state) {
    T lin_dw = (negative > 0) ? (par_4.w) : (-par_4.y);        //[3], [1]
    T lin_a = (negative > 0) ? (lin_slope.y) : (-lin_slope.x); // [1],[0]

    // n is larger 0 in any case
    if (n == 1) {
      if (noise_std_dw > 0) {
        T stoch_value = curand_normal(&local_state);
        stoch_value *= noise_std_dw;
        w += (lin_a * w + lin_dw) * (1.0 + stoch_value);
      } else {
        w += lin_a * w + lin_dw;
      }
    } else {
      if (noise_std_dw > 0) {
        for (int i_updates = 0; i_updates < n; i_updates++) {
          T stoch_value = curand_normal(&local_state);
          stoch_value *= noise_std_dw;
          w += (lin_a * w + lin_dw) * (1.0 + stoch_value);
        }
      } else {
        for (int i_updates = 0; i_updates < n; i_updates++) {
          w += lin_a * w + lin_dw;
        }
      }
    }
    // better always check both bounds
    T wmax = par_4.z; // [2]
    w = (w > wmax) ? wmax : w;
    T wmin = par_4.x; // [0]
    w = (w < wmin) ? wmin : w;
  }
};

template <typename T> struct UpdateFunctorLinearStepAdd {

  __device__ __forceinline__ void operator()(
      T &w,
      uint32_t n,
      uint32_t negative,
      const float4 par_4,
      const float2 lin_slope,
      T &par_1,
      const T *global_par,
      T noise_std_dw,
      curandState &local_state) {
    T lin_dw = (negative > 0) ? (par_4.w) : (-par_4.y);        // [3] [1]
    T lin_a = (negative > 0) ? (lin_slope.y) : (-lin_slope.x); //[1],[0]

    // n is larger 0 in any case
    if (n == 1) {
      if (noise_std_dw > 0) {
        T stoch_value = curand_normal(&local_state);
        stoch_value *= noise_std_dw;
        w += lin_a * w + lin_dw * (1.0 + stoch_value);
      } else {
        w += lin_a * w + lin_dw;
      }
    } else {
      if (noise_std_dw > 0) {
        for (int i_updates = 0; i_updates < n; i_updates++) {
          T stoch_value = curand_normal(&local_state);
          stoch_value *= noise_std_dw;
          w += lin_a * w + lin_dw * (1.0 + stoch_value);
        }
      } else {
        for (int i_updates = 0; i_updates < n; i_updates++) {
          w += lin_a * w + lin_dw;
        }
      }
    }
    T wmax = par_4.z; // [2]
    w = (w > wmax) ? wmax : w;
    T wmin = par_4.x; // [0]
    w = (w < wmin) ? wmin : w;
  }
};

#define ARGS                                                                                       \
  (this->context_, this->x_size_, this->d_size_, m_batch, nK32, use_bo64, out_trans, up,           \
   par.getName())

template <typename T>
pwukpvec_t<T> LinearStepRPUDeviceCuda<T>::getUpdateKernels(
    int m_batch, int nK32, int use_bo64, bool out_trans, const PulsedUpdateMetaParameter<T> &up) {

  pwukpvec_t<T> v;
  const auto &par = getPar();
  if (par.ls_mult_noise) {
    v.push_back(
        make_unique<PWUKernelParameterSingleFunctor<T, UpdateFunctorLinearStepMult<T>, 1>> ARGS);
    v.push_back(
        make_unique<PWUKernelParameterBatchFunctor<T, UpdateFunctorLinearStepMult<T>, 1>> ARGS);
    v.push_back(
        make_unique<PWUKernelParameterBatchSharedFunctor<T, UpdateFunctorLinearStepMult<T>, 1>>
            ARGS);

  } else {

    v.push_back(
        make_unique<PWUKernelParameterSingleFunctor<T, UpdateFunctorLinearStepAdd<T>, 1>> ARGS);
    v.push_back(
        make_unique<PWUKernelParameterBatchFunctor<T, UpdateFunctorLinearStepAdd<T>, 1>> ARGS);
    v.push_back(
        make_unique<PWUKernelParameterBatchSharedFunctor<T, UpdateFunctorLinearStepAdd<T>, 1>>
            ARGS);
  }
  return v;
}

#undef ARGS

template class LinearStepRPUDeviceCuda<float>;
#ifdef RPU_USE_DOUBLE
template class LinearStepRPUDeviceCuda<double>;
#endif

} // namespace RPU
