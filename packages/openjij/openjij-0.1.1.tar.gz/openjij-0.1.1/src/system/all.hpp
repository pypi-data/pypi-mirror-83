//    Copyright 2019 Jij Inc.

//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at

//        http://www.apache.org/licenses/LICENSE-2.0

//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.

#ifndef OPENJIJ_SYSTEM_ALL_HPP__
#define OPENJIJ_SYSTEM_ALL_HPP__

//disable eigen -Wdeprecated-copy warning
#include <utility/disable_eigen_warning.hpp>

#include <system/classical_ising.hpp>
#include <system/transverse_ising.hpp>
#include <system/continuous_time_ising.hpp>

#ifdef USE_CUDA
#include <system/gpu/chimera_gpu_transverse.hpp>
#include <system/gpu/chimera_gpu_classical.hpp>
#endif

#endif
