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

#ifndef OPENJIJ_UTILITY_MEMORY_HPP__
#define OPENJIJ_UTILITY_MEMORY_HPP__

#include <memory>
#include <utility>

namespace openjij {
    namespace utility {

        /**
         * @brief make_unique function
         *
         * @tparam T
         * @tparam ...Args
         * @param ...args
         *
         * @return unique_ptr
         */
        template<typename T, typename ...Args>
            std::unique_ptr<T> make_unique( Args&& ...args )
            {
                return std::unique_ptr<T>( new T( std::forward<Args>(args)... ) );
            }
    } // namespace utility
} // namespace openjij

#endif
