#include "project/project.hpp"

#include <gtest/gtest.h>

#include <string>
#include <vector>

// --- Context tests ---

TEST(ContextTest, ValidConstruction) {
  project::Context ctx("test-context");
  EXPECT_TRUE(ctx.is_valid());
  EXPECT_EQ(ctx.name(), "test-context");
}

TEST(ContextTest, MoveSemantics) {
  project::Context ctx("source");
  project::Context moved = std::move(ctx);
  EXPECT_EQ(moved.name(), "source");
}

// --- Engine tests ---

TEST(EngineTest, InitializeAndShutdown) {
  project::Engine engine;
  auto [ec] = engine.initialize();
  EXPECT_FALSE(ec);
  engine.shutdown();
}

TEST(EngineTest, ProcessEmptyInput) {
  project::Engine engine;
  engine.initialize();
  auto [result, ec] = engine.process({});
  EXPECT_FALSE(ec);
  engine.shutdown();
}

TEST(EngineTest, ProcessWithInput) {
  project::Engine engine;
  engine.initialize();
  auto [result, ec] = engine.process({"hello", "world"});
  EXPECT_FALSE(ec);
  engine.shutdown();
}
