#include "project/project.hpp"

#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>

auto main(int argc, char* argv[]) -> int {
  try {
    std::vector<std::string> args(argv + 1, argv + argc);

    project::Engine engine;
    auto init_result = engine.initialize();
    if (!init_result.second) {
      std::cerr << "Failed to initialize: " << init_result.second.message() << "\n";
      return EXIT_FAILURE;
    }

    auto proc_result = engine.process(args);
    if (!proc_result.second) {
      std::cerr << "Processing failed: " << proc_result.second.message() << "\n";
      return EXIT_FAILURE;
    }

    engine.shutdown();
    return EXIT_SUCCESS;

  } catch (const std::exception& ex) {
    std::cerr << "Unhandled exception: " << ex.what() << "\n";
    return EXIT_FAILURE;
  }
}
