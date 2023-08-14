# CMake file for Resummino.
#
# Copyright 2008-2010 Jonathan Debove.
# Copyright 2011-2014 David R. Lamprea.
# Copyright 2011-2014 Marcel Rothering.
#
# Licensed under the terms of the EUPL version 1.1 or later.
# See the LICENCE file for more information.

cmake_minimum_required(VERSION 2.9)
project(resummino C CXX Fortran)

option(BUILD_LOOPTOOLS "Build LoopTools" ON)
option(BUILD_LHAPDF "Build LHAPDF " OFF)
option(BUILD_TESTING "Build Tests" OFF)

option(BUILD_TESTING "Enable test mode" OFF)
option(DODEBUG "Enable debug mode" OFF)
option(PROFILE "Enable profile mode" OFF)
option(COVERAGE "Enable coverage mode" OFF)

if(NOT CMAKE_BUILD_TYPE)
	set(CMAKE_BUILD_TYPE "Release")
endif()

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_SOURCE_DIR}/external/cmake)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
include_directories(${CMAKE_SOURCE_DIR}/external/include)
include_directories(${CMAKE_SOURCE_DIR}/external/include/Fastor)

include(ExternalProject)

# # compiles looptools 213 (configure script changed so that the folder is always calles lib)
if(BUILD_LOOPTOOLS)
	ExternalProject_Add(lt
		SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/external/lib/LoopTools-2.13
		CONFIGURE_COMMAND ${CMAKE_COMMAND} -E env FFLAGS=-std=legacy CCFLAGS=-fPIC CPPFLAGS=-fPIC ${CMAKE_CURRENT_SOURCE_DIR}/external/lib/LoopTools-2.13/configure --prefix=<INSTALL_DIR>
		BUILD_COMMAND ${MAKE})
	ExternalProject_Get_Property(lt install_dir)
	set(LT_DIR ${install_dir})
	include_directories(${LT_DIR}/include)
	set(LOOPTOOLS_LIBRARIES ${LT_DIR}/lib/libooptools.a)
else()
	find_package(LoopTools REQUIRED)
	include_directories(${LOOPTOOLS_INCLUDE_DIRS})
endif()

# LHAPDF
if(BUILD_LHAPDF)
	# This is needed since otherwise LHAPDF autoconf files get new timestamp and
	# this screws the compilation up.
	if(NOT EXISTS ${CMAKE_SOURCE_DIR}/external/lib/LHAPDF-6.2.3)
		execute_process(COMMAND tar xvfz
			${CMAKE_SOURCE_DIR}/external/lib/LHAPDF-6.2.3.tar.gz -C
			${CMAKE_SOURCE_DIR}/external/lib/)
	endif()

	ExternalProject_Add(lhapdf
		SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/external/lib/LHAPDF-6.2.3
		CONFIGURE_COMMAND
		${CMAKE_CURRENT_SOURCE_DIR}/external/lib/LHAPDF-6.2.3/configure
		--prefix=<INSTALL_DIR> --disable-python
		BUILD_COMMAND ${MAKE})
	ExternalProject_Get_Property(lhapdf install_dir)
	set(LHAPDF_DIR ${install_dir})
	include_directories(${LHAPDF_DIR}/include)
	set(LHAPDF_LIBRARIES ${LHAPDF_DIR}/lib/libLHAPDF.a)
else()
	find_package(LHAPDF REQUIRED)
	include_directories(${LHAPDF_INCLUDE_DIRS})
endif()

# set(LHAPDF ${CMAKE_CURRENT_SOURCE_DIR}/lhapdf-prefix)
# set(LHAPDF_LIBRARIES ${CMAKE_CURRENT_SOURCE_DIR}/lhapdf-prefix/lib/libLHAPDF)
# set(LHAPDF_INCLUDE_DIRS ${CMAKE_CURRENT_SOURCE_DIR}/lhapdf-prefix/include)

# Boost headers
# include(external/cmake/RequireBoostHeaders.cmake)
find_package(Boost 1.67.0 REQUIRED)

# link_directories(${LHAPDF_LIBRARIES})
# find_library(LHAPDF REQUIRED)
# add_library(LHAPDF)
# target_link_libraries(${LHAPDF_LIBRARIES})

# GSL
find_package(GSL REQUIRED)
include_directories(${GSL_INCLUDE_DIRS})

if(DODEBUG)
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g ")
	SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -g ")
	SET(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -g ")
endif()

if(PROFILE)
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pg ")
	SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pg ")
	SET(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -pg ")
endif()

if(COVERAGE)
	include(CodeCoverage)
	APPEND_COVERAGE_COMPILER_FLAGS()
endif()

add_subdirectory(src)

if(BUILD_TESTING)
	include(Catch)
	include_directories(${CMAKE_SOURCE_DIR}/external/include/catch/)

	include(CTest)
	include_directories(src)
	enable_testing()
	add_subdirectory(test)
endif()

if(COVERAGE)
	SETUP_TARGET_FOR_COVERAGE_LCOV(
		NAME coverage
		EXECUTABLE ctest --output-on-failure # -j ${n_cores} # Executable in PROJECT_BINARY_DIR
		DEPENDENCIES
		test_loops
		test_test
		EXCLUDE "/usr/*"
		EXCLUDE "${PROJECT_SOURCE_DIR}/external/*"
	)
endif()
