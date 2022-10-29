import config
import speedtest



def setup():
    speed_test = speedtest.Speedtest()
    tot_bytes = speed_test.download()
    config.HOST_PEAK_NET_BIT_RATE = tot_bytes