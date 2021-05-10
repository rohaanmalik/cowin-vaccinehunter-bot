import http.client
import json
import datetime

conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
payload = ''
headers = {}

def get_next_N_dates(n: int):
    dates = []
    for i in range(n):
        day = datetime.datetime.now() + datetime.timedelta(i)
        dates.append(str(day.day) + "-" +  str(day.month) + "-" +  str(day.year))
    print(dates)
    return dates

def fetch_to_json(days: int, date: str, district_number: int):
    endpoint = "/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}%0A".format(date=date, district_id=district_number)
    conn.request("GET", endpoint, payload, headers)
    res = conn.getresponse()
    data = res.read()
    init_json_str = json.dumps(data.decode("utf-8"))
    temp = json.loads(init_json_str)
    final_dict = json.loads(temp)
    return final_dict

def vaccine_availibility(age: int, type: str, days: int, district_number: int):
    any = True
    if (type != "" or type is None):
        any = False
    dates = get_next_N_dates(days)
    for i in range(len(dates)):
        final_dict = fetch_to_json(days, dates[i], district_number)
        centers = final_dict["centers"]
        final_list = []
        for center in centers:
            center_name = center['name']
            current_session = center["sessions"]
            final_list.extend(get_info_from_session(current_session, age, center_name, any, type))
        return final_list


def get_info_from_session(current_session, age: int, center_name:str, any: bool, type: str):
    final_list = []
    for i in range(len(current_session)):
        vax_name = current_session[i]["vaccine"]
        age_session = current_session[i]["min_age_limit"]
        capacity = current_session[i]["available_capacity"]
        if (age_session < age and capacity > 0):
            if(any is True):
                final_list.append(center_name + " " + vax_name + " " + str(capacity))
            elif(vax_name == type):    # specified a vax type 
                final_list.append(center_name + " " + vax_name + " " + str(capacity))
    return final_list

if __name__ == "__main__":
    final = vaccine_availibility(age=44, type="COVISHIELD",days=2,district_number=365) # Nagpur 
    if len(final) > 0:
        print(final)