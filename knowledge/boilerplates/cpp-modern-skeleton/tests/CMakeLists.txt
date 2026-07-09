include(GoogleTest)
enable_testing()

add_executable(${PROJECT_NAME}_tests
  test_main.cpp
)

target_link_libraries(${PROJECT_NAME}_tests
  PRIVATE
    ${PROJECT_NAME}_lib
    GTest::gtest_main
    GTest::gmock_main
)

set_project_warnings(${PROJECT_NAME}_tests)

gtest_discover_tests(${PROJECT_NAME}_tests)
