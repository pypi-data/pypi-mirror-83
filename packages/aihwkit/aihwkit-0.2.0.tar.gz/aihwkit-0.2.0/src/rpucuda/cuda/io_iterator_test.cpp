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

#include "cuda_math_util.h"
#include "cuda_util.h"
#include "io_iterator.h"
#include "math_util.h"
#include "gtest/gtest.h"
#include <algorithm>
#include <chrono>
#include <functional>
#include <memory>
#include <random>

#define TOLERANCE 1e-5

namespace {

using namespace RPU;

// void transpose(T * x_trans, T* x, int size, int m_batch) {

//   for (int i=0;i<size;i++) {
//     for (int j=0;j<m_batch;j++) {
// 	x_trans[j + i*m_batch] = x[i+j*size];
//     }
//   }
// }

template <typename T> class IteratorTestFixture : public ::testing::Test {
public:
  void SetUp() {

    N = 4;  // number of images ("real" batch)
    m = 10; // number of kernbels for conv
    size = 20;
    unfolded_matrix_size = m * size; // in "conv" space without N.
    orig_matrix_size = 40;           // in "image" space without N

    index = new int[unfolded_matrix_size];
    orig_vector = new T[orig_matrix_size * N];
    orig_vector2 = new T[orig_matrix_size * N];
    unfolded_vector = new T[unfolded_matrix_size * N];
    unfolded_vector2 = new T[unfolded_matrix_size * N];

    auto seed = std::chrono::high_resolution_clock::now().time_since_epoch().count();
    std::default_random_engine generator{seed};
    std::uniform_real_distribution<T> udist(0, orig_matrix_size + 2);
    auto urnd = std::bind(udist, generator);

    for (int i = 0; i < orig_matrix_size * N; i++) {
      orig_vector[i] = urnd(); // some random numnbers
      orig_vector2[i] = orig_vector[i];
    }
    for (int i = 0; i < unfolded_matrix_size; i++) {
      index[i] = floor(urnd()); // indices [0.. orig_matrix_size+2)
    }

    for (int i = 0; i < unfolded_matrix_size * N; i++) {
      int idx = index[i % unfolded_matrix_size];
      unfolded_vector[i] =
          idx <= 1 ? idx : (orig_vector[idx - 2 + i / unfolded_matrix_size * orig_matrix_size]);
      unfolded_vector2[i] = unfolded_vector[i];
    }

    context = make_unique<CudaContext>(-1, false);
    dev_orig_vector = make_unique<CudaArray<T>>(&*context, orig_matrix_size * N, orig_vector);
    dev_orig_vector2 = make_unique<CudaArray<T>>(&*context, orig_matrix_size * N, orig_vector2);
    dev_unfolded_vector =
        make_unique<CudaArray<T>>(&*context, unfolded_matrix_size * N, unfolded_vector);
    dev_unfolded_vector2 =
        make_unique<CudaArray<T>>(&*context, unfolded_matrix_size * N, unfolded_vector2);
    dev_index = make_unique<CudaArray<int>>(&*context, unfolded_matrix_size, index);

    std::vector<int> v(m);
    std::iota(v.begin(), v.end(), 0);
    m_slice = MIN(5, m);
    int s = 0;
    batch_indices = new int[m * N];

    for (int i = 0; i < N; i++) {
      std::shuffle(v.begin(), v.end(), generator);
      for (int j = 0; j < m; j++) {
        batch_indices[s++] = v[j];
      }
    }
    dev_batch_indices = make_unique<CudaArray<int>>(&*context, N * m, batch_indices);

    context->synchronizeDevice();
  };

  void TearDown() {
    delete[] unfolded_vector;
    delete[] unfolded_vector2;
    delete[] orig_vector;
    delete[] orig_vector2;
    delete[] index;
    delete[] batch_indices;
  };

  std::shared_ptr<CudaContext> context;
  std::shared_ptr<CudaArray<T>> dev_orig_vector;
  std::shared_ptr<CudaArray<T>> dev_orig_vector2;
  std::shared_ptr<CudaArray<T>> dev_unfolded_vector;
  std::shared_ptr<CudaArray<T>> dev_unfolded_vector2;
  std::shared_ptr<CudaArray<int>> dev_index;
  std::shared_ptr<CudaArray<int>> dev_batch_indices;

  T *unfolded_vector, *unfolded_vector2;
  T *orig_vector, *orig_vector2;
  int *index;
  int *batch_indices;
  int unfolded_matrix_size, N, orig_matrix_size, size, m, m_slice;
};

#ifdef RPU_USE_DOUBLE
typedef ::testing::Types<float, double> num_types;
#else
typedef ::testing::Types<float> num_types;
#endif

TYPED_TEST_CASE(IteratorTestFixture, num_types);

TYPED_TEST(IteratorTestFixture, copyWithIteratorNoIterator) {
  CUDA_TIMING_INIT(*this->context);
  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, this->dev_unfolded_vector->getData(),
      this->dev_unfolded_vector2->getDataConst(), this->unfolded_matrix_size * this->N);
  CUDA_TIMING_STOP(*this->context, "Copy without iterator");

  this->dev_unfolded_vector->copyTo(this->unfolded_vector);
  this->dev_unfolded_vector2->copyTo(this->unfolded_vector2);

  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->unfolded_vector[i], this->unfolded_vector2[i]);
  }
  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, IndexReaderInputIterator) {
  CUDA_TIMING_INIT(*this->context);

  IndexReaderInputIterator<TypeParam> in_iter(
      this->dev_orig_vector->getDataConst(), this->dev_index->getDataConst(),
      this->orig_matrix_size, this->unfolded_matrix_size);
  this->dev_unfolded_vector->setConst(0);
  this->context->synchronizeDevice();

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, this->dev_unfolded_vector->getData(), in_iter,
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with IndexReaderInputIterator");

  this->dev_unfolded_vector->copyTo(this->unfolded_vector);

  // compare to reference
  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->unfolded_vector[i], this->unfolded_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, IndexReaderTransInputIterator) {
  CUDA_TIMING_INIT(*this->context);

  RPU::math::permute132(
      this->unfolded_vector2, this->unfolded_vector, this->m, this->size, this->N, false);

  IndexReaderTransInputIterator<TypeParam> in_iter(
      this->dev_orig_vector->getDataConst(), this->dev_index->getDataConst(),
      this->orig_matrix_size, this->m, this->unfolded_matrix_size, this->m * this->N);
  this->dev_unfolded_vector->setConst(0);
  this->context->synchronizeDevice();

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, this->dev_unfolded_vector->getData(), in_iter,
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with IndexReaderTransInputIterator");

  this->dev_unfolded_vector->copyTo(this->unfolded_vector);

  // compare to reference
  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->unfolded_vector[i], this->unfolded_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, PermuterTransInputIterator) {
  CUDA_TIMING_INIT(*this->context);

  RPU::math::permute132(
      this->unfolded_vector, this->unfolded_vector2, this->m, this->size, this->N, false);

  PermuterTransInputIterator<TypeParam> in_iter(
      this->dev_unfolded_vector->getDataConst(), this->m, this->m * this->size, this->m * this->N);
  this->dev_unfolded_vector2->setConst(0);
  this->context->synchronizeDevice();

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, this->dev_unfolded_vector2->getData(), in_iter,
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with PermuterTransInputIterator");

  this->dev_unfolded_vector2->copyTo(this->unfolded_vector2);

  // compare to reference
  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->unfolded_vector[i], this->unfolded_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, PermuterTransOutputIterator) {
  CUDA_TIMING_INIT(*this->context);

  // first permute and set to device. PermuterTrans should de-permute it to match the original
  RPU::math::permute132(
      this->unfolded_vector2, this->unfolded_vector, this->m, this->size, this->N, false);

  this->dev_unfolded_vector->assign(this->unfolded_vector2);
  this->dev_unfolded_vector2->setConst(0);
  this->context->synchronizeDevice();

  PermuterTransOutputIterator<TypeParam> out_iter(
      this->dev_unfolded_vector2->getData(), this->m, this->m * this->size, this->m * this->N);

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, out_iter, this->dev_unfolded_vector->getDataConst(),
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with PermuterTransOutputIterator");

  this->dev_unfolded_vector2->copyTo(this->unfolded_vector2);

  // compare to reference
  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->unfolded_vector[i], this->unfolded_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, IndexReaderTransOutputIterator) {
  CUDA_TIMING_INIT(*this->context);

  RPU::math::permute132(
      this->unfolded_vector2, this->unfolded_vector, this->m, this->size, this->N, false);
  this->dev_unfolded_vector->assign(this->unfolded_vector2); // now transposed

  this->dev_orig_vector2->setConst(0);
  this->context->synchronizeDevice();

  IndexReaderTransOutputIterator<TypeParam> out_iter(
      this->dev_orig_vector2->getData(), this->dev_index->getDataConst(), this->orig_matrix_size,
      this->m, this->m * this->size, this->m * this->N);

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, out_iter,
      this->dev_unfolded_vector->getDataConst(), // transposed
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with IndexReaderTransOutputIterator");

  for (int i = 0; i < this->orig_matrix_size * this->N; i++) {
    this->orig_vector[i] = 0;
  }

  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    int idx = this->index[i % this->unfolded_matrix_size] - 2;
    if (idx >= 0) {
      int j = idx + i / this->unfolded_matrix_size * this->orig_matrix_size;
      this->orig_vector[j] += this->unfolded_vector[i]; // the not transposed one
    }
  }
  // compare to reference
  this->dev_orig_vector2->copyTo(this->orig_vector2);
  for (int i = 0; i < this->orig_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->orig_vector[i], this->orig_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

TYPED_TEST(IteratorTestFixture, IndexReaderOutputIterator) {
  CUDA_TIMING_INIT(*this->context);

  this->dev_orig_vector2->setConst(0);
  this->context->synchronizeDevice();

  IndexReaderOutputIterator<TypeParam> out_iter(
      this->dev_orig_vector2->getData(), this->dev_index->getDataConst(), this->orig_matrix_size,
      this->m * this->size);

  CUDA_TIMING_START(*this->context);
  math::copyWithIterator(
      &*this->context, out_iter, this->dev_unfolded_vector->getDataConst(),
      this->unfolded_matrix_size * this->N);

  CUDA_TIMING_STOP(*this->context, "Copy with IndexReaderOutputIterator");

  for (int i = 0; i < this->orig_matrix_size * this->N; i++) {
    this->orig_vector[i] = 0;
  }

  for (int i = 0; i < this->unfolded_matrix_size * this->N; i++) {
    int idx = this->index[i % this->unfolded_matrix_size] - 2;
    if (idx >= 0) {
      int j = idx + i / this->unfolded_matrix_size * this->orig_matrix_size;
      this->orig_vector[j] += this->unfolded_vector[i];
    }
  }
  // compare to reference
  this->dev_orig_vector2->copyTo(this->orig_vector2);
  for (int i = 0; i < this->orig_matrix_size * this->N; i++) {
    ASSERT_FLOAT_EQ(this->orig_vector[i], this->orig_vector2[i]);
  }

  CUDA_TIMING_DESTROY;
}

} // namespace

int main(int argc, char **argv) {
  resetCuda();
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
