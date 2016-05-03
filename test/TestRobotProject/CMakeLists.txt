cmake_minimum_required(VERSION 2.8)

include(FRCDeploy)

project(TestRobotProject)

set(CMAKE_CXX_FLAGS "-fpermissive")

file(GLOB_RECURSE SOURCE_CODE *.cpp)

find_package(WPILib)

include_directories(${WPILib_INCLUDE_DIRS})

add_executable(TestProject ${SOURCE_CODE})

target_link_libraries(TestProject ${WPILib_LIBRARY})

add_make_deploy(TestProject 10.30.81.2)
