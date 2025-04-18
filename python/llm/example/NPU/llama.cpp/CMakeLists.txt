cmake_minimum_required(VERSION 3.10)

project(LLM_NPU_EXAMPLE VERSION 1.0.0 LANGUAGES CXX)

set (CMAKE_CXX_STANDARD 17)
SET (CMAKE_CXX_STANDARD_REQUIRED True)

if(DEFINED ENV{CONDA_ENV_DIR})
    set(ENV_DIR $ENV{CONDA_ENV_DIR})
    set(LIBRARY_DIR ${ENV_DIR}/bigdl-core-npu)
    include_directories(${LIBRARY_DIR}/include/npu)
    include_directories(${LIBRARY_DIR}/include/llamacpp)
    set(DLL_DIR ${ENV_DIR}/intel_npu_acceleration_library/lib/Release)
else()
    set(LIBRARY_DIR ${CMAKE_CURRENT_SOURCE_DIR})
    include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
endif()

add_library(npu_llm STATIC IMPORTED)
set_target_properties(npu_llm PROPERTIES IMPORTED_LOCATION ${LIBRARY_DIR}/npu_llm.lib)

add_library(llama STATIC IMPORTED)
set_target_properties(llama PROPERTIES IMPORTED_LOCATION ${LIBRARY_DIR}/llama.lib)

add_library(common STATIC IMPORTED)
set_target_properties(common PROPERTIES IMPORTED_LOCATION ${LIBRARY_DIR}/common.lib)

add_library(ggml STATIC IMPORTED)
set_target_properties(ggml PROPERTIES IMPORTED_LOCATION ${LIBRARY_DIR}/ggml.lib)

set(TARGET simple)
add_executable(${TARGET} simple.cpp)
install(TARGETS ${TARGET} RUNTIME)
target_link_libraries(${TARGET} PRIVATE npu_llm common llama ggml ${CMAKE_THREAD_LIBS_INIT})
target_compile_features(${TARGET} PRIVATE cxx_std_17)

add_custom_command(TARGET simple POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        ${LIBRARY_DIR}/npu_llm.dll
        ${LIBRARY_DIR}/llama.dll
        ${LIBRARY_DIR}/ggml.dll
        ${CMAKE_BINARY_DIR}/Release/
    COMMENT "Copying npu_llm.dll llama.dll ggml.dll to build/Release\n"
)

add_custom_command(TARGET simple POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${DLL_DIR}/
        ${CMAKE_BINARY_DIR}/Release/
    COMMENT "Copying dependency to build/Release\n"
)