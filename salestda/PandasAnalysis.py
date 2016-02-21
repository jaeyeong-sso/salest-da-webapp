import pandas as pd
import pandas.io.sql as pd_sql
import MySQLdb

def agg_montly_sales_volumn():
    
    con = MySQLdb.connect(host='173.194.254.102', 
                port=3306,user='salest', passwd='salest', 
                db='salest_database')

    df_dailyTr = pd_sql.read_frame('select * from daily_tr_summary',con)
    df_dailyTr["date"] = pd.to_datetime(df_dailyTr["date"])
    df_dailyTr['date_mon'] = df_dailyTr['date'].apply(lambda date: date.strftime('%Y-%m'))

    monthly_df = df_dailyTr[['num_of_order','total_amount']].groupby(df_dailyTr['date_mon']).sum()
    df_list = list(monthly_df.itertuples(index=True))

    df_column_name_list = list(monthly_df.columns.values)
    df_column_name_list.insert(0,'year_mon')
    
    list_month_sales_volume = []
    dict_month_sales_volume = {}

    for row in df_list:
        dict_month_sales_volume = {}
        
        for key,value in zip(df_column_name_list, row):
            dict_month_sales_volume[key] = value
        
        list_month_sales_volume.append(dict_month_sales_volume.copy())
        
    return list_month_sales_volume