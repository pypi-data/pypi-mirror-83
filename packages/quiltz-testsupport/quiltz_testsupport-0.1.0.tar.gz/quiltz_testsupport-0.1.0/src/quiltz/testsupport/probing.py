from time import sleep

def probe_that(f, timeout=1000):
    t = 0
    success = False
    while(not success):
        try:
            f()
            success = True
        except AssertionError as e:
            sleep(50.0/1000.0)
            t += 50
            if (t>=timeout):
                raise e
