import bus
from find_place import find_place


def cmd(cmd , tdx_token, client_id):
    if cmd == "command":
        return "1. 公車站 [起始公車站名]到[終點公車站名]\n2. 地名 [起始地點]到[終點]"
    if cmd[:3] == "公車站":
        if " " in cmd:
            startToend = cmd.split(" ")[1]
            if "到" in startToend:
                start_stop = startToend.split("到")[0]
                end_stop = startToend.split("到")[1]
                return bus.find_bus(start_stop, end_stop, tdx_token)
            else:
                return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    if cmd[:2] == "地名":
        if " " in cmd:
            startToend = cmd.split(" ")[1]
            if "到" in startToend:
                start_place = startToend.split("到")[0]
                end_place = startToend.split("到")[1]
                return bus.find_bus_position(start_place, end_place, tdx_token, client_id)
            else:
                return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    return "指令輸入錯誤，請重新輸入指令。\n如果要查詢指令使用方式，請輸入command"
    



if __name__ == "__main__":
    tdx_token = bus.get_token()
    print(cmd("command", tdx_token, "123"))
    print(cmd("公車站 師大分部到臺大", tdx_token, "123"))
    print(cmd("地名 新光三越到統一阪急", tdx_token, "123"))
    print(cmd(str(11223), tdx_token, "123"))