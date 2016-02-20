import pandas as pd
import pandas.io.sql as pd_sql
import MySQLdb

def aggregateMonthlyTrSummary():
    
    con = MySQLdb.connect(host='173.194.254.102', 
                port=3306,user='salest', passwd='salest', 
                db='salest_database')

    df_dailyTr = pd_sql.read_frame('select * from daily_tr_summary',con)
    df_dailyTr["date"] = pd.to_datetime(df_dailyTr["date"])
    df_dailyTr['date_mon'] = df_dailyTr['date'].apply(lambda date: date.strftime('%Y-%m'))

    monthly_df = df_dailyTr[['num_of_order','total_amount']].groupby(df_dailyTr['date_mon']).sum()
    return list(monthly_df.itertuples(index=True))