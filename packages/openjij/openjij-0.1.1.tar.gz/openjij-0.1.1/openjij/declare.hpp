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

#ifndef OPENJIJ_DECLARE_HPP__
#define OPENJIJ_DECLARE_HPP__

#include <graph/all.hpp>
#include <system/all.hpp>
#include <updater/all.hpp>
#include <algorithm/all.hpp>
#include <result/all.hpp>

#include <pybind11_json/pybind11_json.hpp>
#include <nlohmann/json.hpp>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

using namespace py::literals;
using namespace openjij;

//graph
inline void declare_Graph(py::module& m){
    py::class_<graph::Graph>(m, "Graph")
        .def(py::init<std::size_t>(), "num_spins"_a)
        .def("gen_spin", [](const graph::Graph& self, std::size_t seed){
                RandomEngine rng(seed);
                return self.gen_spin(rng);
                }, "seed"_a)
    .def("gen_spin", [](const graph::Graph& self){
            RandomEngine rng(std::random_device{}());
            return self.gen_spin(rng);
            })
    .def("size", &graph::Graph::size);
}

//dense
template<typename FloatType>
inline void declare_Dense(py::module& m, const std::string& suffix){

    using json = nlohmann::json;

    auto str = std::string("Dense") + suffix;
    py::class_<graph::Dense<FloatType>, graph::Graph>(m, str.c_str())
        .def(py::init<std::size_t>(), "num_spins"_a)
        .def(py::init([](py::object obj){return std::unique_ptr<graph::Dense<FloatType>>(new graph::Dense<FloatType>(static_cast<json>(obj)));}), "obj"_a)
        .def(py::init<const graph::Dense<FloatType>&>(), "other"_a)
        .def("set_interaction_matrix", &graph::Dense<FloatType>::set_interaction_matrix, "interaction"_a)
        .def("calc_energy", [](const graph::Dense<FloatType>& self, const Eigen::Matrix<FloatType, Eigen::Dynamic, 1, Eigen::ColMajor>& spins){return self.calc_energy(spins);}, "spins"_a)
        .def("calc_energy", [](const graph::Dense<FloatType>& self, const graph::Spins& spins){return self.calc_energy(spins);}, "spins"_a)
        .def("__setitem__", [](graph::Dense<FloatType>& self, const std::pair<std::size_t, std::size_t>& key, FloatType val){self.J(key.first, key.second) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Dense<FloatType>& self, const std::pair<std::size_t, std::size_t>& key){return self.J(key.first, key.second);}, "key"_a)
        .def("__setitem__", [](graph::Dense<FloatType>& self, std::size_t key, FloatType val){self.h(key) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Dense<FloatType>& self, std::size_t key){return self.h(key);}, "key"_a)
        .def("get_interactions", &graph::Dense<FloatType>::get_interactions);
}

//sparse
template<typename FloatType>
inline void declare_Sparse(py::module& m, const std::string& suffix){

    using json = nlohmann::json;

    auto str = std::string("Sparse") + suffix;
    py::class_<graph::Sparse<FloatType>, graph::Graph>(m, str.c_str())
        .def(py::init<std::size_t, std::size_t>(), "num_spins"_a, "num_edges"_a)
        .def(py::init<std::size_t>(),  "num_spins"_a)
        .def(py::init([](py::object obj, std::size_t num_edges){return std::unique_ptr<graph::Sparse<FloatType>>(new graph::Sparse<FloatType>(static_cast<json>(obj), num_edges));}), "obj"_a, "num_edges"_a)
        .def(py::init([](py::object obj){return std::unique_ptr<graph::Sparse<FloatType>>(new graph::Sparse<FloatType>(static_cast<json>(obj)));}), "obj"_a)
        .def(py::init<const graph::Sparse<FloatType>&>(), "other"_a)
        .def("adj_nodes", &graph::Sparse<FloatType>::adj_nodes)
        .def("get_num_edges", &graph::Sparse<FloatType>::get_num_edges)
        .def("calc_energy", [](const graph::Sparse<FloatType>& self, const Eigen::Matrix<FloatType, Eigen::Dynamic, 1, Eigen::ColMajor>& spins){return self.calc_energy(spins);}, "spins"_a)
        .def("calc_energy", [](const graph::Sparse<FloatType>& self, const graph::Spins& spins){return self.calc_energy(spins);}, "spins"_a)
        .def("__setitem__", [](graph::Sparse<FloatType>& self, const std::pair<std::size_t, std::size_t>& key, FloatType val){self.J(key.first, key.second) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Sparse<FloatType>& self, const std::pair<std::size_t, std::size_t>& key){return self.J(key.first, key.second);}, "key"_a)
        .def("__setitem__", [](graph::Sparse<FloatType>& self, std::size_t key, FloatType val){self.h(key) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Sparse<FloatType>& self, std::size_t key){return self.h(key);}, "key"_a);
}

//enum class Dir
inline void declare_Dir(py::module& m){
    py::enum_<graph::Dir>(m, "Dir")
        .value("PLUS_R", graph::Dir::PLUS_R)
        .value("MINUS_R", graph::Dir::MINUS_R)
        .value("PLUS_C", graph::Dir::PLUS_C)
        .value("MINUS_C", graph::Dir::MINUS_C);
}

//square
template<typename FloatType>
inline void declare_Square(py::module& m, const std::string& suffix){

    using json = nlohmann::json;

    auto str = std::string("Square") + suffix;
    py::class_<graph::Square<FloatType>, graph::Sparse<FloatType>>(m, str.c_str())
        .def(py::init<std::size_t, std::size_t, FloatType>(), "num_row"_a, "num_column"_a, "init_val"_a=0)
        .def(py::init<const graph::Square<FloatType>&>(), "other"_a)
        .def(py::init([](py::object obj, std::size_t num_row, std::size_t num_column, FloatType init_val){return std::unique_ptr<graph::Square<FloatType>>(new graph::Square<FloatType>(static_cast<json>(obj), num_row, num_column, init_val));}), "obj"_a, "num_row"_a, "num_column"_a, "init_val"_a = 0)
        .def("to_ind", &graph::Square<FloatType>::to_ind)
        .def("to_rc", &graph::Square<FloatType>::to_rc)
        .def("get_num_row", &graph::Square<FloatType>::get_num_row)
        .def("get_num_column", &graph::Square<FloatType>::get_num_column)
        .def("__setitem__", [](graph::Square<FloatType>& self, const std::tuple<std::size_t, std::size_t, graph::Dir>& key, FloatType val){self.J(std::get<0>(key), std::get<1>(key), std::get<2>(key)) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Square<FloatType>& self, const std::tuple<std::size_t, std::size_t, graph::Dir>& key){return self.J(std::get<0>(key), std::get<1>(key), std::get<2>(key));}, "key"_a)
        .def("__setitem__", [](graph::Square<FloatType>& self, const std::pair<std::size_t, std::size_t>& key, FloatType val){self.h(key.first, key.second) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Square<FloatType>& self, const std::pair<std::size_t, std::size_t>& key){return self.h(key.first, key.second);}, "key"_a);
}

//enum class ChimeraDir
inline void declare_ChimeraDir(py::module& m){
    py::enum_<graph::ChimeraDir>(m, "ChimeraDir")
        .value("PLUS_R", graph::ChimeraDir::PLUS_R)
        .value("MINUS_R", graph::ChimeraDir::MINUS_R)
        .value("PLUS_C", graph::ChimeraDir::PLUS_C)
        .value("MINUS_C", graph::ChimeraDir::MINUS_C)
        .value("IN_0or4", graph::ChimeraDir::IN_0or4)
        .value("IN_1or5", graph::ChimeraDir::IN_1or5)
        .value("IN_2or6", graph::ChimeraDir::IN_2or6)
        .value("IN_3or7", graph::ChimeraDir::IN_3or7);
}

//chimera
template<typename FloatType>
inline void declare_Chimera(py::module& m, const std::string& suffix){

    using json = nlohmann::json;

    auto str = std::string("Chimera") + suffix;
    py::class_<graph::Chimera<FloatType>, graph::Sparse<FloatType>>(m, str.c_str())
        .def(py::init<std::size_t, std::size_t, FloatType>(), "num_row"_a, "num_column"_a, "init_val"_a=0)
        .def(py::init<const graph::Chimera<FloatType>&>(), "other"_a)
        .def(py::init([](py::object obj, std::size_t num_row, std::size_t num_column, FloatType init_val){return std::unique_ptr<graph::Chimera<FloatType>>(new graph::Chimera<FloatType>(static_cast<json>(obj), num_row, num_column, init_val));}), "obj"_a, "num_row"_a, "num_column"_a, "init_val"_a = 0)
        .def("to_ind", &graph::Chimera<FloatType>::to_ind)
        .def("to_rci", &graph::Chimera<FloatType>::to_rci)
        .def("get_num_row", &graph::Chimera<FloatType>::get_num_row)
        .def("get_num_column", &graph::Chimera<FloatType>::get_num_column)
        .def("get_num_in_chimera", &graph::Chimera<FloatType>::get_num_in_chimera)
        .def("__setitem__", [](graph::Chimera<FloatType>& self, const std::tuple<std::size_t, std::size_t, std::size_t, graph::ChimeraDir>& key, FloatType val){self.J(std::get<0>(key), std::get<1>(key), std::get<2>(key), std::get<3>(key)) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Chimera<FloatType>& self, const std::tuple<std::size_t, std::size_t, std::size_t, graph::ChimeraDir>& key){return self.J(std::get<0>(key), std::get<1>(key), std::get<2>(key), std::get<3>(key));}, "key"_a)
        .def("__setitem__", [](graph::Chimera<FloatType>& self, const std::tuple<std::size_t, std::size_t, std::size_t>& key, FloatType val){self.h(std::get<0>(key), std::get<1>(key), std::get<2>(key)) = val;}, "key"_a, "val"_a)
        .def("__getitem__", [](const graph::Chimera<FloatType>& self, const std::tuple<std::size_t, std::size_t, std::size_t>& key){return self.h(std::get<0>(key), std::get<1>(key), std::get<2>(key));}, "key"_a);
}

//system

//ClassicalIsing
template<typename GraphType>
inline void declare_ClassicalIsing(py::module &m, const std::string& gtype_str){
    //ClassicalIsing
    using ClassicalIsing = system::ClassicalIsing<GraphType>;

    auto str = std::string("ClassicalIsing")+gtype_str;
    py::class_<ClassicalIsing>(m, str.c_str())
        .def(py::init<const graph::Spins&, const GraphType&>(), "init_spin"_a, "init_interaction"_a)
        .def("reset_spins", [](ClassicalIsing& self, const graph::Spins& init_spin){self.reset_spins(init_spin);},"init_spin"_a)
        .def_readwrite("spin", &ClassicalIsing::spin)
        .def_readonly("interaction", &ClassicalIsing::interaction)
        .def_readonly("num_spins", &ClassicalIsing::num_spins);

    //make_classical_ising
    auto mkci_str = std::string("make_classical_ising");
    m.def(mkci_str.c_str(), [](const graph::Spins& init_spin, const GraphType& init_interaction){
            return system::make_classical_ising(init_spin, init_interaction);
            }, "init_spin"_a, "init_interaction"_a);
}


//TransverseIsing
template<typename GraphType>
inline void declare_TransverseIsing(py::module &m, const std::string& gtype_str){
    //TransverseIsing
    using TransverseIsing = system::TransverseIsing<GraphType>;
    using FloatType = typename GraphType::value_type;

    auto str = std::string("TransverseIsing")+gtype_str;
    py::class_<TransverseIsing>(m, str.c_str())
        .def(py::init<const system::TrotterSpins&, const GraphType&, FloatType>(), "init_spin"_a, "init_interaction"_a, "gamma"_a)
        .def(py::init<const graph::Spins&, const GraphType&, FloatType, size_t>(), "init_classical_spins"_a, "init_interaction"_a, "gamma"_a, "num_trotter_slices"_a)
        .def("reset_spins", [](TransverseIsing& self, const system::TrotterSpins& init_trotter_spins){self.reset_spins(init_trotter_spins);},"init_trotter_spins"_a)
        .def("reset_spins", [](TransverseIsing& self, const graph::Spins& classical_spins){self.reset_spins(classical_spins);},"classical_spins"_a)
        .def_readwrite("trotter_spins", &TransverseIsing::trotter_spins)
        .def_readonly("interaction", &TransverseIsing::interaction)
        .def_readonly("num_classical_spins", &TransverseIsing::num_classical_spins)
        .def_readwrite("gamma", &TransverseIsing::gamma);

    //make_transverse_ising
    auto mkci_str = std::string("make_transverse_ising");
    m.def(mkci_str.c_str(), [](const system::TrotterSpins& init_trotter_spins, const GraphType& init_interaction, double gamma){
            return system::make_transverse_ising(init_trotter_spins, init_interaction, gamma);
            }, "init_trotter_spins"_a, "init_interaction"_a, "gamma"_a);

    m.def(mkci_str.c_str(), [](const graph::Spins& classical_spins, const GraphType& init_interaction, double gamma, std::size_t num_trotter_slices){
            return system::make_transverse_ising(classical_spins, init_interaction, gamma, num_trotter_slices);
            }, "classical_spins"_a, "init_interaction"_a, "gamma"_a, "num_trotter_slices"_a);
}

//Continuous Time Transverse Ising
template<typename GraphType>
inline void declare_ContinuousTimeIsing(py::module &m, const std::string& gtype_str){
    //TransverseIsing
    using TransverseIsing = system::ContinuousTimeIsing<GraphType>;
    using FloatType = typename GraphType::value_type;
    using SpinConfiguration = typename TransverseIsing::SpinConfiguration;

    auto str = std::string("ContinuousTimeIsing")+gtype_str;
    py::class_<TransverseIsing>(m, str.c_str())
        .def(py::init<const SpinConfiguration&, const GraphType&, FloatType>(), "init_spin_config"_a, "init_interaction"_a, "gamma"_a)
        .def(py::init<const graph::Spins&, const GraphType&, FloatType>(), "init_spins"_a, "init_interaction"_a, "gamma"_a)
        .def("reset_spins", [](TransverseIsing& self, const SpinConfiguration& init_spin_config){self.reset_spins(init_spin_config);},"init_spin_config"_a)
        .def("reset_spins", [](TransverseIsing& self, const graph::Spins& classical_spins){self.reset_spins(classical_spins);},"classical_spins"_a)
        .def_readwrite("spin_config", &TransverseIsing::spin_config)
        .def_readonly("interaction", &TransverseIsing::interaction)
        .def_readonly("num_spins", &TransverseIsing::num_spins)
        .def_readonly("gamma", &TransverseIsing::gamma);

    //make_continuous_ising
    auto mkci_str = std::string("make_continuous_time_ising");
    m.def(mkci_str.c_str(), [](const graph::Spins& classical_spins, const GraphType& init_interaction, double gamma){
            return system::make_continuous_time_ising(classical_spins, init_interaction, gamma);
            }, "classical_spins"_a, "init_interaction"_a, "gamma"_a);
}

#ifdef USE_CUDA

//ChimeraTransverseGPU
template<typename FloatType,
    std::size_t rows_per_block,
    std::size_t cols_per_block,
    std::size_t trotters_per_block>
    inline void declare_ChimeraTranseverseGPU(py::module &m){
        using ChimeraTransverseGPU = system::ChimeraTransverseGPU<FloatType, rows_per_block, cols_per_block, trotters_per_block>;
        py::class_<ChimeraTransverseGPU>(m, "ChimeraTransverseGPU")
            .def(py::init<const system::TrotterSpins&, const graph::Chimera<FloatType>&, FloatType, int>(), "init_trotter_spins"_a, "init_interaction"_a, "gamma"_a, "device_num"_a=0)
            .def(py::init<const graph::Spins&, const graph::Chimera<FloatType>&, FloatType, size_t, int>(), "classical_spins"_a, "init_interaction"_a, "gamma"_a, "num_trotter_slices"_a, "device_num"_a=0)
            .def("reset_spins", [](ChimeraTransverseGPU& self, const system::TrotterSpins& init_trotter_spins){self.reset_spins(init_trotter_spins);},"init_trotter_spins"_a)
            .def("reset_spins", [](ChimeraTransverseGPU& self, const graph::Spins& classical_spins){self.reset_spins(classical_spins);},"classical_spins"_a)
            .def_readwrite("gamma", &ChimeraTransverseGPU::gamma);

        //make_chimera_transverse_gpu
        m.def("make_chimera_transverse_gpu", [](const system::TrotterSpins& init_trotter_spins, const graph::Chimera<FloatType>& init_interaction, double gamma, int device_num){
                return system::make_chimera_transverse_gpu<rows_per_block, cols_per_block, trotters_per_block>(init_trotter_spins, init_interaction, gamma, device_num);
                }, "init_trotter_spins"_a, "init_interaction"_a, "gamma"_a, "device_num"_a=0);

        m.def("make_chimera_transverse_gpu", [](const graph::Spins& classical_spins, const graph::Chimera<FloatType>& init_interaction, double gamma, size_t num_trotter_slices, int device_num){
                return system::make_chimera_transverse_gpu<rows_per_block, cols_per_block, trotters_per_block>(classical_spins, init_interaction, gamma, num_trotter_slices, device_num);
                }, "classical_spins"_a, "init_interaction"_a, "gamma"_a, "num_trotter_slices"_a, "device_num"_a=0);
    }

//ChimeraClassicalGPU
template<typename FloatType,
    std::size_t rows_per_block,
    std::size_t cols_per_block>
    inline void declare_ChimeraClassicalGPU(py::module &m){
        using ChimeraClassicalGPU = system::ChimeraClassicalGPU<FloatType, rows_per_block, cols_per_block>;
        py::class_<ChimeraClassicalGPU, typename ChimeraClassicalGPU::Base>(m, "ChimeraClassicalGPU")
            .def(py::init<const graph::Spins&, const graph::Chimera<FloatType>&, int>(), "init_spin"_a, "init_interaction"_a, "device_num"_a=0)
            .def("reset_spins", [](ChimeraClassicalGPU& self, const graph::Spins& init_spin){self.reset_spins(init_spin);},"init_spin"_a);

        //make_chimera_transverse_gpu
        m.def("make_chimera_classical_gpu", [](const graph::Spins& init_spin, const graph::Chimera<FloatType>& init_interaction, int device_num){
                return system::make_chimera_classical_gpu<rows_per_block, cols_per_block>(init_spin, init_interaction, device_num);
                }, "init_spin"_a, "init_interaction"_a, "device_num"_a=0);
    }

#endif


//Algorithm
template<template<typename> class Updater, typename System, typename RandomNumberEngine>
inline void declare_Algorithm_run(py::module &m, const std::string& updater_str){
    auto str = std::string("Algorithm_")+updater_str+std::string("_run");
    using SystemType = typename system::get_system_type<System>::type;
    //with seed
    m.def(str.c_str(), [](System& system, std::size_t seed, const utility::ScheduleList<SystemType>& schedule_list,
                const std::function<void(const System&, const typename utility::UpdaterParameter<SystemType>::Tuple&)>& callback){
            py::gil_scoped_release release;

            using Callback = std::function<void(const System&, const utility::UpdaterParameter<SystemType>&)>;
            RandomNumberEngine rng(seed);
            algorithm::Algorithm<Updater>::run(system, rng, schedule_list,
                    callback ? [=](const System& system, const utility::UpdaterParameter<SystemType>& param){callback(system, param.get_tuple());} : Callback(nullptr));

            py::gil_scoped_acquire acquire;
            }, "system"_a, "seed"_a, "schedule_list"_a, "callback"_a = nullptr);

    //without seed
    m.def(str.c_str(), [](System& system, const utility::ScheduleList<SystemType>& schedule_list,
                const std::function<void(const System&, const typename utility::UpdaterParameter<SystemType>::Tuple&)>& callback){
            py::gil_scoped_release release;

            using Callback = std::function<void(const System&, const utility::UpdaterParameter<SystemType>&)>;
            RandomNumberEngine rng(std::random_device{}());
            algorithm::Algorithm<Updater>::run(system, rng, schedule_list,
                    callback ? [=](const System& system, const utility::UpdaterParameter<SystemType>& param){callback(system, param.get_tuple());} : Callback(nullptr));

            py::gil_scoped_acquire acquire;
            }, "system"_a, "schedule_list"_a, "callback"_a = nullptr);

    //schedule_list can be a list of tuples
    using TupleList = std::vector<std::pair<typename utility::UpdaterParameter<SystemType>::Tuple, std::size_t>>;
    
    //with seed
    m.def(str.c_str(), [](System& system, std::size_t seed, const TupleList& tuplelist,
                const std::function<void(const System&, const typename utility::UpdaterParameter<SystemType>::Tuple&)>& callback){
            py::gil_scoped_release release;

            using Callback = std::function<void(const System&, const utility::UpdaterParameter<SystemType>&)>;
            RandomNumberEngine rng(seed);
            algorithm::Algorithm<Updater>::run(system, rng, utility::make_schedule_list<SystemType>(tuplelist),
                    callback ? [=](const System& system, const utility::UpdaterParameter<SystemType>& param){callback(system, param.get_tuple());} : Callback(nullptr));

            py::gil_scoped_acquire acquire;
            }, "system"_a, "seed"_a, "tuplelist"_a, "callback"_a = nullptr);

    //without seed
    m.def(str.c_str(), [](System& system, const TupleList& tuplelist,
                const std::function<void(const System&, const typename utility::UpdaterParameter<SystemType>::Tuple&)>& callback){
            py::gil_scoped_release release;

            using Callback = std::function<void(const System&, const utility::UpdaterParameter<SystemType>&)>;
            RandomNumberEngine rng(std::random_device{}());
            algorithm::Algorithm<Updater>::run(system, rng, utility::make_schedule_list<SystemType>(tuplelist),
                    callback ? [=](const System& system, const utility::UpdaterParameter<SystemType>& param){callback(system, param.get_tuple());} : Callback(nullptr));

            py::gil_scoped_acquire acquire;
            }, "system"_a, "tuplelist"_a, "callback"_a = nullptr);

}

//utility
template<typename SystemType>
inline std::string repr_impl(const utility::UpdaterParameter<SystemType>&);

template<>
inline std::string repr_impl(const utility::UpdaterParameter<system::classical_system>& obj){
    return "(beta: " + std::to_string(obj.beta) + ")";
}

template<>
inline std::string repr_impl(const utility::UpdaterParameter<system::classical_constraint_system>& obj){
    return "(beta: " + std::to_string(obj.beta) + ", lambda: " + std::to_string(obj.lambda) + ")";
}

template<>
inline std::string repr_impl(const utility::UpdaterParameter<system::transverse_field_system>& obj){
    return "(beta: " + std::to_string(obj.beta) + ", s: " + std::to_string(obj.s) + ")";
}

template<typename SystemType>
inline void declare_Schedule(py::module &m, const std::string& systemtype_str){
    auto str = systemtype_str + "Schedule";
    py::class_<utility::Schedule<SystemType>>(m, str.c_str())
        .def(py::init<>())
        .def(py::init<const std::pair<const utility::UpdaterParameter<SystemType>&, std::size_t>&>(), "obj"_a)
        .def_readwrite("one_mc_step", &utility::Schedule<SystemType>::one_mc_step)
        .def_readwrite("updater_parameter", &utility::Schedule<SystemType>::updater_parameter)
        .def("__repr__", [](const utility::Schedule<SystemType>& self){
                return "(" + repr_impl(self.updater_parameter) + " mcs: " + std::to_string(self.one_mc_step) + ")";
                });

    //define make_schedule_list
    m.def("make_schedule_list", &utility::make_schedule_list<SystemType>, "tuplelist"_a);

}

//result
//get_solution
template<typename System>
inline void declare_get_solution(py::module &m){
    m.def("get_solution", [](const System& system){return result::get_solution(system);}, "system"_a);
}



#endif
