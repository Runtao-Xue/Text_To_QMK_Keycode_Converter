import os
import sys
import time
# #
if sys.platform == "win32":
    import msvcrt  # Windows specific
else:
    import select  # Used for input timeout on macOS/Linux

class Text_To_QMK_Keycodes:
    """
    A cross-platform utility class for converting text input into QMK firmware keycode sequences with clipboard integration and timeout features.

    This tool handles alphanumeric and shifted symbol conversion, simulates keyboard modifier behavior with timing delays, 
    and provides platform-appropriate input handling (Windows/macOS/Linux). The class supports bilingual UI prompts 
    and automatic clipboard operations.

    Key Features:
    - Converts uppercase letters and symbols to QMK's shift-modified keycodes
    - Adds configurable delay intervals between key actions
    - Implements input timeout with OS-specific non-blocking input
    - Supports Chinese/English prompts based on language parameter
    - Auto-copies results to system clipboard

    Class Methods:
    __init__(language: str)
    Initializes converter with UI language preference ('CN' for Chinese). Sets default delay (15ms) 
    and timeout (300s).

    copy_to_clipboard(text: str) -> None
    OS-agnostic clipboard insertion using:
    - Windows: clip command
    - macOS: pbcopy
    - Linux: xclip

    convert_text_to_qmk_keycodes(input_text: str) -> str
    Transforms input string into QMK-compatible sequence:
    - Handles uppercase via KC_LSFT modifiers
    - Maps symbols to shifted equivalents (e.g., '!' becomes shifted '1')
    - Inserts delay wrappers between key events

    get_input_with_timeout() -> Optional[str]
    Captures input with activity timeout using:
    - Windows: msvcrt for real-time keypress detection
    - Unix-like: select module for input polling
    Returns None on timeout, handles backspace/enter keys

    main() -> None
    Primary interaction loop:
    1. Displays timeout-aware prompt
    2. Processes conversion
    3. Manages clipboard operations
    4. Handles KeyboardInterrupt for clean exit

    Usage Example:
    >>> ttqk = Text_To_QMK_Keycodes(language='EN')
    >>> ttqk.main()  # Starts interactive session with English prompts

    Platform Notes:
    - Requires xclip package on Linux systems
    - Tested with Python 3.8+ on major OS versions
    - Shift timing optimized for QMK's default debounce behavior
    """
    def __init__(self, language):
        self.delay = 15
        self.timeout = 300
        self.language = language

    def copy_to_clipboard(self, text):
        if sys.platform == "win32":
            os.system(f'echo {text.strip()} | clip')
        elif sys.platform == "darwin":  # macOS
            os.system(f'echo "{text.strip()}" | pbcopy')
        else:  # Linux
            os.system(f'echo "{text.strip()}" | xclip -selection clipboard')

    def convert_text_to_qmk_keycodes(self, input_text):
        symbol_dict = {'!':'1', '@':'2', '#':'3', '$':'4', '%':'5', '^':'6', '&':'7', '*':'8', '(':'9', ')':'0',
                    '_':'-', '+':'=', '{':'[', '}':']', '|':'{KC_BSLS}', ':':';', '"':"'", '<':',', '>':'.', '?':'/'}
        delay_time = self.delay
        delay_string = '{' + str(delay_time) + '}'
        input_lst = list(str(input_text))
        output_lst = []
        for elem in input_lst:
            if elem.isalpha() and elem.isupper():
                elem = '{+KC_LSFT}' + delay_string + elem.lower() + delay_string + '{-KC_LSFT}'
            elif elem in symbol_dict:
                elem = '{+KC_LSFT}' + delay_string + symbol_dict[elem] + delay_string + '{-KC_LSFT}'
            output_lst.append(elem)
        return delay_string.join(output_lst)

    def get_input_with_timeout(self):
        timeout = self.timeout
        if self.language=='CN':
            print(f"请输入字符串（回车 Enter 转换为 QMK Keycodes，Ctrl+C 退出。{timeout} 秒无操作自动退出）：")
        else:
            print(f"Please enter a string (Press Enter to convert to QMK Keycodes, Ctrl+C to exit. The program will exit automatically after {timeout} seconds of inactivity):")
        
        if sys.platform == "win32":  # Windows non-blocking input
            sys.stdout.write("> ")
            sys.stdout.flush()
            input_text = ""
            start_time = time.time()

            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char == "\r":  # Enter key
                        print()
                        return input_text
                    elif char == "\b":  # Backspace key
                        input_text = input_text[:-1]
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    else:
                        input_text += char
                        sys.stdout.write(char)
                        sys.stdout.flush()

                if time.time() - start_time > timeout:
                    if self.language=='CN':
                        print(f"\n{timeout} 秒无操作，程序自动退出。")
                    else:
                        print(f"\n{timeout} seconds of inactivity. The program exited automatically.")
                    return None

        else:  # macOS/Linux timeout input
            sys.stdout.write("> ")
            sys.stdout.flush()
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            
            if ready:  # If input is received within timeout
                return sys.stdin.readline().strip()
            else:  # Timeout exit
                if self.language=='CN':
                    print(f"\n{timeout} 秒无操作，程序自动退出。")
                else:
                    print(f"\n{timeout} seconds of inactivity. The program exited automatically.")
                return None

    def main(self):
        while True:
            try:
                user_input = self.get_input_with_timeout()
                if user_input is None:
                    break
                
                result = self.convert_text_to_qmk_keycodes(user_input)                
                if self.language=='CN':
                    print("转换结果：", result)
                else:
                    print("Conversion result:", result)
                self.copy_to_clipboard(result)
                if self.language=='CN':
                    print("已复制到剪贴板。")
                else:
                    print("Copied to clipboard.")
            except KeyboardInterrupt:
                if self.language=='CN':
                    print("\n程序已退出。")
                else:
                    print("\nProgram exited.")
                break

if __name__ == "__main__":
    ttqk_object = Text_To_QMK_Keycodes(language='EN')
    ttqk_object.main()
