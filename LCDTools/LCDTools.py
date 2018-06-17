'''
MIT License

Copyright (c) 2018 Kyle Kowalczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
--------------------------------------------------------------------------------

Author: Kyle Kowalczyk

'''

from RPLCD import CharLCD
import RPi.GPIO as GPIO
from time import sleep


class Driver:

    Newline = '\r\n'

    def __init__(self, rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin, boardNum=GPIO.BCM, rwPin=None, cols=16, rows=2,
                 warnings=False):

        if warnings is False:
            GPIO.setwarnings(False)

        self.cols = cols
        self.rows = rows

        self.firstRun = True

        self.lcd = CharLCD(cols=cols, rows=rows, pin_rw=rwPin, pin_rs=rsPin, pin_e=enPin,
                           pins_data=[d4Pin,d5Pin,d6Pin,d7Pin], numbering_mode=boardNum)

        self._warm_up_display()

        self.lcdmem = self._generate_lcd_memory()
        self.curpos = [0, 0]  # [row, column]

        sleep(1)
        self.lcd.clear()
        sleep(1)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        GPIO.cleanup()

    def _warm_up_display(self):
        '''
        Fills every section of the display with spaces so the display gets "warmed up"
        and doesnt output junk when we start sending real data to it.
        :return:
        '''

        characters = self.cols * self.rows

        for x in range(characters):
            self.append_to_screen(' ')

    def _generate_lcd_memory(self):

        mem = []

        for x in range(self.rows):
            row = []

            for y in range(self.cols):
                row.append('')

            mem.append(row)

        return mem

    def _update_cursor_position(self):
        pass


    def send_newline(self):

        '''Sends a newline character to the LCD screen.

        :return: None
        '''

        self.lcd.write_string(self.Newline)

        if self.rows - 1 == self.curpos[0]:
            self.curpos[0] = 0

        else:
            self.curpos[0] += 1

        self.curpos[1] = 0

    def center_text(self, text):

        '''Returns supplied text centered based on how many columns the LCD screen has

        :param text: Text to center
        :type text: str
        :return: Centered text
        :rtype: str
        '''

        if len(text) > self.cols:
            raise Exception('Cant Center Text greather than screen width')

        if len(text) == self.cols:
            return text

        return text.center(self.cols, ' ')

    def append_to_screen(self, text, delay=.2):
        '''Appends text to the screen where the cursor last ended.

        :param text: String to write to the LCD screen
        :type text: str
        :param delay: Time to wait before writing string to the screen
        :type delay: float
        :return: None
        '''

        def determine_cursor_row():

            if columnCounter > self.cols - 1:
                if self.curpos[1] == self.cols - 1:
                    self.curpos[1] = 0

                else:

                    self.curpos[1] += 1

        def update_cursor_column():
            self.curpos[1] = columnCounter

        #sleep(delay)
        columnCounter = self.curpos[1]

        for char in text:


            update_cursor_column()
            determine_cursor_row()

            # writes data to LCD
            self.lcd.write_string(char)
            # updates the memory of what is written to the LCD
            self.lcdmem[self.curpos[0]][self.curpos[1]] = char

            if columnCounter == self.cols - 1:
                columnCounter = 0
                update_cursor_column()
                self.curpos[0] += 1

                if self.curpos[0] > self.rows - 1:
                    self.curpos[0] = 0
            else:

                columnCounter += 1
                update_cursor_column()


    def refresh_screen(self, text, delay=.2):

        '''Clears the LCD and writes a string of text

        :param text: String to write to the LCD screen
        :type text: str
        :param delay: Time to wait before writing string to the screen
        :type delay: float
        :return: None
        '''

        self.lcd.clear()
        self.append_to_screen(text, delay)

    def clear_screen(self):

        '''Clears the LCD screen

        :return: None
        '''

        self.curpos = [0, 0]

        # blanks out the LCD memory
        self.lcdmem = self._generate_lcd_memory()

        self.lcd.clear()

    def show_whats_displayed(self):

        '''Tool to show on the command line what is currently displayed to the screen'''


        totalWidth = self.cols + 2
        print('Output Display'.center(totalWidth))


        print('-' * totalWidth)
        for row in self.lcdmem:
            lineText = ''.join(letter for letter in row)
            if len(lineText) < self.cols:
                padding = self.cols - len(lineText)
                print('|' + lineText + ' ' * padding + '|')
            else:
                print('|{}|'.format(lineText))

        print('-' * totalWidth)




if __name__ == '__main__':

    '''
    Example on how to use the class above
    '''

    from datetime import timedelta

    def getUptime():
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds=uptime_seconds))

        return uptime_string[:-4]


    rsPin = 21
    enPin = 20
    d4Pin = 25
    d5Pin = 24
    d6Pin = 23
    d7Pin = 18

    with LCDTools(rsPin, enPin, d4Pin, d5Pin, d6Pin, d7Pin) as lcd:
        lcd.clear_screen()
        while True:

            try:
                uptime = getUptime()[:-3]
                lcd.append_to_screen(lcd.center_text('Suh Dude!'))
                lcd.append_to_screen(lcd.center_text('Uptime: {}'.format(uptime)))

                #lcd.show_whats_displayed()
            except KeyboardInterrupt:
                '''
                sleep(1)
                lcd.clear_screen()
                '''
                sleep(1)
                break
        lcd.clear_screen()
