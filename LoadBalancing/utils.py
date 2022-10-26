def get_top_perc(hist, perc=0.90):
    covered = 0
    for i in range(0, 100, 5):
        covered += hist[i]
        if covered >= perc:
            return (i + 2.5) / 100.0

    if covered == 0.0:
        # hist not filled ?
        return 0.0
    else:
        # 100% usage
        return 1.0



def get_mem_swap_hist(hist):
    mem_hist = {i : 0 for i in range(0, 100, 5)}
    swap_hist = {i : 0 for i in range(0, 100, 5)}

    total_mem_p = 0.0
    total_swap_p = 0.0

    for i in range(0, 5, 50):
        total_mem_p += hist[i]
        total_swap_p += hist[i + 50]

    for i in range(0, 5, 50):
        mem_hist[i * 2] = hist[i] / total_mem_p
        swap_hist[i * 2] = hist[i + 50] / total_swap_p

    return mem_hist, swap_hist



import socket


def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.settimeout(0)
  try:
    # doesn't even have to be reachable
    s.connect(('10.254.254.254', 1))
    IP = s.getsockname()[0]
  except Exception:
    IP = '127.0.0.1'
  finally:
    s.close()
  return IP
