idf_component_register(
    SRCS "main.c" "waveshare_rgb_lcd_port.c" "./waveshare_rgb_lcd_port.c" "./main.c" "./lvgl_port.c"
    INCLUDE_DIRS "."
    REQUIRES
        "lvgl"
        "ui"
        "esp_common")

idf_component_get_property(lvgl_lib lvgl__lvgl COMPONENT_LIB)
target_compile_options(${lvgl_lib} PRIVATE -Wno-format)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unused-variable")


#add_definitions(-DEEZ_FOR_LVGL)