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

#pragma once

#include "cuda_util.h"

namespace RPU {

template <typename T> class PulsedRPUDeviceCuda;

template <typename T> class PulsedUpdateMetaParameter;

template <typename T> class BitLineMaker;

// base class
template <typename T> class PWUKernelParameterBase {

public:
  PWUKernelParameterBase(){}; // default
  PWUKernelParameterBase(
      CudaContext *construction_context,
      int x_size_in,
      int d_size_in,
      int m_batch,
      int nK32_in,
      int use_bo64_in,
      bool out_trans_in,
      const PulsedUpdateMetaParameter<T> &up,
      std::string update_name) {

    // returns only valid=true if kernel type is allowed with
    // given m_batch/nK32/out_trans/sizeof_count settings

    // CAUTION: nblock + nthreads is expected to NOT depend on
    // out_trans/m_batch/nK32/sizeof_count

    max_block_count = construction_context->getSMCount() * RPU_UPDATE_BLOCKS_PER_SM;

    x_size = x_size_in;
    d_size = d_size_in;
    nK32 = nK32_in;
    size = d_size * x_size;
    m_batch = m_batch;
    out_trans = out_trans_in;
    use_bo64 = use_bo64_in;
    valid = true;

    if (use_bo64 > 0) {
      sizeof_count = sizeof(uint64_t);
    } else {
      sizeof_count = sizeof(uint32_t);
    }

    name = update_name;
    if (out_trans) {
      name += "/Trans";
    }
    if (use_bo64 == 1) {
      name += "/BO64direct";
    }
    if (use_bo64 > 1) {
      name += "/BO64";
    }

    if (use_bo64 > 0 && (nK32 > 1)) {
      valid = false;
    }

    if (use_bo64 > 0 && (!out_trans)) { // not supported by BLM
      valid = false;
    }
  };

  virtual void
  run(cudaStream_t s,
      T *dev_weights,
      int m_batch,
      const BitLineMaker<T> *blm,
      PulsedRPUDeviceCuda<T> *rpucuda_device,
      const PulsedUpdateMetaParameter<T> &up,
      curandState_t *dev_states,
      int one_sided = 0,
      uint32_t *x_counts_chunk = nullptr,
      uint32_t *d_counts_chunk = nullptr) = 0;

  inline int getNStates() { return this->nstates; };
  inline void setNStates(int n) { this->nstates = n; };
  inline bool isValid() { return this->valid; };
  inline std::string getName() { return this->name; };
  inline bool getOutTrans() { return this->out_trans; };
  inline int getUseBo64() { return this->use_bo64; };

  inline void forceBo64Translate() {
    if (this->use_bo64 == 1) {
      this->use_bo64 = 2;
    }
  };                                                        // debug hack
  inline void forceNonTrans() { this->out_trans = false; }; // debug hack
  inline void force32() { this->use_bo64 = 0; };            // debug hack

  inline void ensureChunk() {
    if (use_bo64 || out_trans) {
      valid = false;
    }
  };

  virtual void print() const {

    std::cout << name << std::endl;
    std::cout << "\t nthreads:\t " << nthreads << std::endl;
    std::cout << "\t nblocks:\t " << nblocks << std::endl;
    std::cout << "\t shared_mem:\t " << shared_mem << std::endl;
    std::cout << "\t out_trans:\t " << out_trans << std::endl;
    std::cout << "\t sizeof_count:\t " << sizeof_count << std::endl;
    std::cout << "\t nstates:\t " << nstates << std::endl;
    std::cout << "\t batch_stride:\t " << batch_load_stride << std::endl;
    std::cout << "\t nK32:\t\t " << nK32 << std::endl;
    std::cout << "\t m_batch:\t " << m_batch << std::endl;
    std::cout << "\t timing:\t " << timing << std::endl;
  };

public:
  T timing = 0.0;

protected:
  int x_size = 0;
  int d_size = 0;
  int size = 0;

  std::string name;
  int shared_mem = 0;
  int shared_mem_per_batch = 0;
  bool out_trans = false;
  int sizeof_count = 4;
  int use_bo64 = 0;
  int nK32 = 1;
  int m_batch = 1;
  int batch_load_stride = 0;
  int nstates = 0;

  int nthreads = 0;
  int nblocks = 0;
  int max_block_count = 0;

  bool valid = false;
};

template <typename T> using pwukp_t = std::shared_ptr<PWUKernelParameterBase<T>>;

template <typename T> using pwukpvec_t = std::vector<pwukp_t<T>>;

} // namespace RPU
