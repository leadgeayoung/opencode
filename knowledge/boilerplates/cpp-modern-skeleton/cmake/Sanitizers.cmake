# AddressSanitizer + UndefinedBehaviorSanitizer
function(enable_sanitizers target)
  if(ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(${target} PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options(${target} PRIVATE -fsanitize=address,undefined)
  elseif(ENABLE_SANITIZERS AND MSVC)
    target_compile_options(${target} PRIVATE /fsanitize=address)
  endif()
endfunction()
