#define LV_MEM_CUSTOM 1
#define LV_MEMCPY_MEMSET_STD 1
#define LV_ATTRIBUTE_FAST_MEM IRAM_ATTR


#include "waveshare_rgb_lcd_port.h"
#include "ui.h"
#include "eez-flow.h"

void app_main()
{
    /*  waveshare_rgb_lcd_port handles lvgl_port and initialization of the screen and touch. It also sets up the 
    *  IO expander. **note** This is where we will have to modifiy to work with other touch controllers and displays
    *  eventually selectable through the import script.
    *
    *  lvgl_port handles the lvgl initialization and the lvgl task setup. I have modified this to work with EEZ-Flow by 
    * adding calls tp ui_init() and ui_tick() in their respective places.
    * 
    *  also provided with waveshare_rgb_lcd_port.h is a function to turn the screen backlight on and off. To turn the 
    * backlight on and off, simply call the waveshare_rgb_lcd_bl_on() and waveshare_rgb_lcd_bl_off() functions.
    */

    waveshare_esp32_s3_rgb_lcd_init(); // Initializes the Waveshare ESP32-S3 RGB LCD & Touch Controller

    wavesahre_rgb_lcd_bl_on();  // Turn on the backlight through the IO Expander
    // wavesahre_rgb_lcd_bl_off(); // Turn off the backlight through the IO Expander
    
}

