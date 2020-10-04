from halo import Halo
import time
SPINERSOMETHING = 'something'
_spinner = Halo(text='trying to live', spinner='dots' )
_spinner.start()
_spinner.succeed(text='doing things')
time.sleep(1)
_spinner.fail(text=SPINERSOMETHING)
time.sleep(5)
_spinner.stop()

