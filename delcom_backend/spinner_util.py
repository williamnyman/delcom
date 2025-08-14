# spinner.py
import itertools
import threading
import sys
import time

# Global variables to track the spinner
_stop_spinner = False
_spinner_thread = None

def _spinner_task(msg):
    for frame in itertools.cycle([
			"[    ]",
			"[=   ]",
			"[==  ]",
			"[=== ]",
			"[====]",
			"[ ===]",
			"[  ==]",
			"[   =]",
			"[    ]",
			"[   =]",
			"[  ==]",
			"[ ===]",
			"[====]",
			"[=== ]",
			"[==  ]",
			"[=   ]"]):
        if _stop_spinner:
            break
        sys.stdout.write(f'\r{msg} {frame}')
        sys.stdout.flush()
        time.sleep(0.1)

def spinner_start(msg="Loading"):
    """Start the spinner in the background with a message."""
    global _stop_spinner, _spinner_thread
    _stop_spinner = False
    _spinner_thread = threading.Thread(target=_spinner_task, args=(msg,), daemon=True)
    _spinner_thread.start()

def spinner_end(final_msg=None):
    """Stop the spinner and optionally print a final message."""
    global _stop_spinner, _spinner_thread
    _stop_spinner = True
    if _spinner_thread is not None:
        _spinner_thread.join()
    if final_msg:
        print(f'\r{final_msg}   ')
    else:
        print()  # just move to next line
