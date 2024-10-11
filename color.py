def wavelength_to_rgb(wavelength):
    r = g = b = 0

    if 380 <= wavelength < 440:
        r = -(wavelength - 440) / (440 - 380)
        g = 0
        b = 1
    elif 440 <= wavelength < 490:
        r = 0
        g = (wavelength - 440) / (490 - 440)
        b = 1
    elif 490 <= wavelength < 510:
        r = 0
        g = 1
        b = -(wavelength - 510) / (510 - 490)
    elif 510 <= wavelength < 580:
        r = (wavelength - 510) / (580 - 510)
        g = 1
        b = 0
    elif 580 <= wavelength < 645:
        r = 1
        g = -(wavelength - 645) / (645 - 580)
        b = 0
    elif 645 <= wavelength <= 780:
        r = 1
        g = 0
        b = 0

    else:
        print("超出范围！")

    # 确保 RGB 值在 0 到 1 之间
    r = int(max(0, min(1, r)) * 255)
    g = int(max(0, min(1, g)) * 255)
    b = int(max(0, min(1, b)) * 255)

    return r, g, b


