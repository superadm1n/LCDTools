# LCDTools

This module is designed to be used as a Library to interact with
an LCD screen.

the LCDTools library will allow for 4 pin communication with the LCD
screen and it will keep track of where the cursor is locate on the LCD
screen and what text is displayed where so you can still get insight
as to what is being displayed without having to eat up a bunch of pins.


### Prerequisites

RPi.GPIO==0.6.3

RPLCD==1.1.0


### Installation
Issue the following commands to install this driver into your project

```
pip install git+https://github.com/superadm1n/LCDTools
```

### Using Library
Below is example code for using the driver to display text to the screen
Show an CLI reperesentation of what the LCD looks like and clear it
off after 5 seconds.

```
import LCDTools

with LCDTools(rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin) as lcd:
    lcd.clear_screen()
    lcd.append_to_screen(lcd.center_text('Hello!'))  # prints centered
    lcd.append_to_screen('Have Fun!')
    lcd.show_whats_displayed()
    time.sleep(5)
    lcd.clear_screen()

#EOF
```


## Author

* **Kyle Kowalczyk**  [SmallGuysIT](https://smallguysit.com)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

