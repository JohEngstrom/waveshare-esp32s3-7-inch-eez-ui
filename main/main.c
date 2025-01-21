/*
 * SPDX-FileCopyrightText: 2023-2024 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#define LV_MEM_CUSTOM 1
#define LV_MEMCPY_MEMSET_STD 1
#define LV_ATTRIBUTE_FAST_MEM IRAM_ATTR

#include "waveshare_rgb_lcd_port.h"
#include "ui.h"

void app_main()
{
    // waveshare_rgb_lcd_port handles lvgl porting and initialization. It also handles the display and touch driver for this board
    waveshare_esp32_s3_rgb_lcd_init(); // Initialize the Waveshare ESP32-S3 RGB LCD 
    wavesahre_rgb_lcd_bl_on();  //Turn on the screen backlight 
    // wavesahre_rgb_lcd_bl_off(); //Turn off the screen backlight 
    
    ESP_LOGI(TAG, "Display LVGL demos");
    // Lock the mutex due to the LVGL APIs are not thread-safe
    if (lvgl_port_lock(-1)) {
        // lv_demo_stress();
        // lv_demo_benchmark();
        // lv_demo_music();
        // lv_demo_widgets();
        // example_lvgl_demo_ui();

        ui_init(); // This will initialize the EEZ UI copied into the component/ui folder

        // Release the mutex
        lvgl_port_unlock();
    }


    // The following is the bare minimum required to run your UI with flow support
    if (lvgl_port_lock(-1)) {
        ui_tick();
        lvgl_port_unlock();
    }
}

