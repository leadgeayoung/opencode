add_library(${PROJECT_NAME}_lib
  STATIC
    main.cpp
)

target_include_directories(${PROJECT_NAME}_lib
  PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

target_link_libraries(${PROJECT_NAME}_lib
  PRIVATE
    ProjectOptions::fmt  # placeholder for external deps
)

set_project_warnings(${PROJECT_NAME}_lib)
enable_sanitizers(${PROJECT_NAME}_lib)

add_executable(${PROJECT_NAME}
  main.cpp
)

target_link_libraries(${PROJECT_NAME}
  PRIVATE
    ${PROJECT_NAME}_lib
)

set_project_warnings(${PROJECT_NAME})
enable_sanitizers(${PROJECT_NAME})
