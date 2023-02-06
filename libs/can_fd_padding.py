def can_fd_data(d):
    return ( d if d <=  8 else
        12 if 8 < d <= 12 else
        16 if 12 < d <= 16 else
        20 if 16 < d <= 20 else
        24 if 20 < d <= 24 else
        32 if 24 < d <= 32 else
        48 if 32 < d <= 48 else
        64)   
    