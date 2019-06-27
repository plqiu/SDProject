

def standard_power_curve(wind_input_list):
    power_output_list=[]
    for wind_input in wind_input_list:
        if 3 >= wind_input:
            power_output = 0
        elif (wind_input > 3 and 5 >= wind_input):
            power_output = 72.563 * (wind_input - 3) + 11.6
        elif wind_input > 5 and 6 >= wind_input:
            power_output = 130.12 * (wind_input - 5) + 156.726
        if wind_input > 6 and 7 >= wind_input :
            power_output = 187.277 * (wind_input - 6) + 286.848
        if wind_input > 7 and 8 >= wind_input :
            power_output = 253.344 * (wind_input - 7) + 474.123
        if wind_input > 8 and 9.1 >= wind_input :
            power_output = 307.253 * (wind_input - 8) + 727.467
        if wind_input > 9.1 and 10.5 >= wind_input :
            power_output = 309.086 * (wind_input - 9.1) + 1067.28
        if wind_input > 10.5 :
            power_output = 1550

        power_output_list.append(power_output)
    return power_output_list