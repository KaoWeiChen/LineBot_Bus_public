import bus
from find_place import find_place
'''
可用指令:
    1. 公車站 [出發公車站名]到[到達公車站名]
    2. 地點 [出發地點]到[到達地點]
    3. command
'''

def cmd(cmd , tdx_token, line_client_id=None):
    if cmd == "command":
        return "1. 公車站 [出發公車站名]到[到達公車站名]\n2. 地點 [出發地點]到[到達地點]"
    if cmd[:3] == "公車站":
        if " " in cmd:
            startToend = cmd.split(" ")[1]
            if "到" in startToend:
                start_stop = startToend.split("到")[0]
                end_stop = startToend.split("到")[1]
                return bus.find_bus(start_stop, end_stop, tdx_token)
            else:
                return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    if cmd[:2] == "地點":
        if " " in cmd:
            startToend = cmd.split(" ")[1]
            if "到" in startToend:
                start_place = startToend.split("到")[0]
                end_place = startToend.split("到")[1]
                return bus.find_bus_position(start_place, end_place, tdx_token, line_client_id)
            else:
                return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    

def main():
    tdx_token = bus.get_token()
    command = input("指令格式:\n1. 公車站 [出發公車站名]到[到達公車站名]\n2. 地點 [出發地點]到[到達地點]\n請輸入指令: ")
    print(cmd(command, tdx_token))


if __name__ == "__main__":
    main()
