from os import getenv
from datetime import datetime,  timedelta
from requests import Session
from json import dumps

printjson = lambda x: print(dumps(x.json(), indent=4))
html_path = "../fastapi/templates/current.html"



base_url = "https://api.ouraring.com"
s = Session()
s.headers = {"Authorization": f"Bearer {getenv('TOKEN')}"}


# https://cloud.ouraring.com/v2/docs#tag/Daily-Sleep-Routes

keyword = "daily_readiness"
keyword = "daily_sleep"
keyword = "daily_activity"
keyword = "sleep"

res = s.get(
    url = f"{base_url}/v2/usercollection/{keyword}",
    params={
        "start_date": (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "end_date": (datetime.utcnow() - timedelta(days=0)).strftime("%Y-%m-%d"),
    }
    
)
j = res.json()["data"][0]


hrv_list, hr_list = [], []
_ = [hrv_list.extend(x["hrv"]["items"]) for x in res.json()["data"]]
_ = [hr_list.extend(x["heart_rate"]["items"]) for x in res.json()["data"]]

import plotly.express as px
import pandas as pd

data = pd.concat([
    pd.DataFrame(data={"value": hrv_list, "measurement": "HRV"}),
    pd.DataFrame(data={"value": hr_list, "measurement": "HR"})
])

plt = px.line(data, facet_col="measurement", color="measurement",facet_col_wrap=2)
plt.write_html(html_path)



x = s.get(
    url = f"{base_url}/v2/usercollection/heartrate",
    params={
        "start_datetime": "2023-05-01T00:00:00",
        "end_datetime": "2023-05-12T00:00:00"
    }
    
)

len(x.json()["data"])

printjson(x)