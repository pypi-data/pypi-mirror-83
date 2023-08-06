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

#ifndef OPENJIJ_GRAPH_HPP__
#define OPENJIJ_GRAPH_HPP__

#include <vector>
#include <cstddef>
#include <random>
#include <nlohmann/json.hpp>

namespace openjij {
    namespace graph {

        using Spin = int;
        using Spins = std::vector<Spin>;
        using Index = std::size_t;

        using Nodes = std::vector<Index>;

        /**
         * @brief Abstract graph class
         */
        class Graph{
            private:
                const std::size_t _num_spins; /**< total number of spins */
            public:

                /**
                 * @brief Graph constructor
                 *
                 * @param num_spins total number of spins
                 */
                explicit Graph(std::size_t num_spins)
                    :_num_spins(num_spins){}

                /**
                 * @brief generate spins randomly.
                 *
                 * @return generated spins
                 */
                // const Spins gen_spin() const{
                template<typename RandomNumberEngine>
                const Spins gen_spin(RandomNumberEngine& random_numder_engine) const{
                    //generate spin array
                    Spins ret_spin(_num_spins);

                    std::uniform_int_distribution<> uid(0, 1);
                    for(auto& elem : ret_spin){
                        elem = 2*uid(random_numder_engine)-1;
                    }

                    return ret_spin;
                }


                /**
                 * @brief get number of spins
                 * @deprecated please use size()
                 *
                 * @return number of spins
                 */
                std::size_t get_num_spins() const noexcept {
                    return _num_spins;
                }

                /**
                 * @brief get number of spins
                 *
                 * @return number of spins
                 */
                std::size_t size() const noexcept {
                    return _num_spins;
                }
        };
    } // namespace graph 
} // namespace openjij

#endif
