#pragma once

#include <memory>
#include <string>
#include <string_view>
#include <system_error>
#include <vector>

namespace project {

// Result type for operations that can fail
template <typename T>
using Result = std::pair<T, std::error_code>;

class Context {
 public:
  explicit Context(std::string_view name);
  ~Context();

  Context(const Context&) = delete;
  Context& operator=(const Context&) = delete;
  Context(Context&&) noexcept = default;
  Context& operator=(Context&&) noexcept = default;

  [[nodiscard]] std::string_view name() const noexcept { return name_; }
  [[nodiscard]] bool is_valid() const noexcept { return valid_; }

 private:
  std::string name_;
  bool valid_ = false;
};

class Engine {
 public:
  Engine();
  ~Engine();

  Engine(const Engine&) = delete;
  Engine& operator=(const Engine&) = delete;
  Engine(Engine&&) noexcept = default;
  Engine& operator=(Engine&&) noexcept = default;

  [[nodiscard]] Result<int> initialize();
  [[nodiscard]] Result<int> process(const std::vector<std::string>& input);
  void shutdown() noexcept;

 private:
  class Impl;
  std::unique_ptr<Impl> impl_;
};

}  // namespace project
