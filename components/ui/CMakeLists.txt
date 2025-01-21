idf_component_register(
    SRCS "ui.c"  # We'll replace this with dynamic source gathering
    INCLUDE_DIRS "."
    REQUIRES 
        "lvgl"  # Add any required dependencies
)

# Dynamically gather all source files
file(GLOB UI_SRCS "*.c" "*.cpp")
set_source_files_properties(${UI_SRCS} PROPERTIES COMPILE_FLAGS "-Wno-unused-function")
target_sources(${COMPONENT_LIB} PRIVATE ${UI_SRCS})