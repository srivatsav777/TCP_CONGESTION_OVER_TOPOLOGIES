import pandas as pd
from plotnine import *
from plotnine.data import *
import sys

dtypes = { 
    "ts" : "float",
    "sender" : "category", 
    "retr" : "float",
    "retr.total" : "float",
    "cwnd" : "float", 
    "ssthresh" : "float",
    "rtt" : "float"
}

col_names = [ "ts", "sender", "retr", "retr.total", "cwnd", "ssthresh" , "rtt"]

df = pd.read_csv(sys.argv[1] , names = col_names ,  dtype= dtypes )

df['sender_codes'] = df.sender.cat.codes

df["ts"] = df["ts"] - df["ts"].min()

lost = df.dropna()
lost = lost[(lost["retr"] > 0)]

pt = ggplot(df) + geom_line(aes(x="ts", y="cwnd" ))  

pt = pt + theme_bw() + geom_vline(aes(xintercept="ts" , color="sender") , data=lost , alpha=0.1 )

pt = pt + scale_y_continuous(breaks = list(range(0 , 50 ,10)) , name="CWND") + scale_x_continuous(breaks = list(range(0 , 40 , 2)) , name="Time (s)") + scale_colour_discrete()  

ggsave(plot = pt, filename = sys.argv[2] , path = "./")
