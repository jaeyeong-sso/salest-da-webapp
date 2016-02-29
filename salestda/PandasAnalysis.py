import pandas as pd
import pandas.io.sql as pd_sql
import MySQLdb
import ast

def agg_montly_sales_volumn(unit_numofproduct, unit_salesamount):
    
    conn = MySQLdb.connect(host='173.194.254.102', 
                port=3306,user='salest', passwd='salest', 
                db='salest_database')

    df_dailyTr = pd_sql.read_frame('select * from daily_tr_summary',conn)
    conn.close()
    
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
            if(key=='num_of_order'):
                value = value / unit_numofproduct
            if(key=='total_amount'):
                value = value / unit_salesamount
            dict_month_sales_volume[key] = value
        
        list_month_sales_volume.append(dict_month_sales_volume.copy())
        
    return list_month_sales_volume


def desc_total_sales_volumn():
    conn = MySQLdb.connect(host='173.194.254.102', 
                port=3306,user='salest', passwd='salest', 
                db='salest_database')

    df_dailyTr = pd_sql.read_frame('select * from daily_tr_summary',conn)
    conn.close()
    
    df_dailyTr["date"] = pd.to_datetime(df_dailyTr["date"])
    series_sum = df_dailyTr.sum()
    series_sum.name = 'sum'
    desc_dfs = df_dailyTr.describe().append(series_sum)

    desc_dfs = desc_dfs.drop(['id'],axis=1)
    desc_dfs['num_of_order'] = desc_dfs['num_of_order'].apply(lambda v: round(v))
    desc_dfs['total_amount'] = desc_dfs['total_amount'].apply(lambda v: round(v))

    return desc_dfs.to_dict()
    

#################################################################################################

def agg_montly_num_of_product_by_product_cate():

    conn = MySQLdb.connect(host='173.194.254.102', 
                    port=3306,user='salest', passwd='salest', 
                    db='salest_database')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    
    df_daily_product_tr = pd_sql.read_frame('select * from daily_product_tr_summary',conn)
        
    conn.close()
    
    df_daily_product_tr['date_mon'] = df_daily_product_tr['date'].apply(lambda date: date.strftime('%Y-%m'))
        
    def aggregation(row):
        num_of_product = row['num_of_product'].sum()
        return pd.Series([num_of_product], index=['num_of_product'])
    
    df_monthly_product_tr = df_daily_product_tr.groupby(['date_mon','product_cate']).apply(aggregation)

    
    def gen_dict_num_of_product(month_rows):
        mothlyDict = {}
        
        itemList = []
        for item in zip(month_rows.index.get_level_values('product_cate'),month_rows['num_of_product']):
            itemList.append({'item':item[0],'value':item[1]})
        mothlyDict['year_month'] = month_rows.index.get_level_values('date_mon')[0]
        mothlyDict['data'] = itemList
        return mothlyDict


    mothlyNumOfProductDictItems = df_monthly_product_tr.groupby(df_monthly_product_tr.index.get_level_values('date_mon')).apply(gen_dict_num_of_product)

    mothlyNumOfProductDict = {}
    mothlyNumOfProductList = []
    for item in mothlyNumOfProductDictItems:
        mothlyNumOfProductList.append(item)
    mothlyNumOfProductDict['num_of_product'] = mothlyNumOfProductList

    return mothlyNumOfProductDict;


def agg_montly_total_amount_by_product_cate():

    conn = MySQLdb.connect(host='173.194.254.102', 
                    port=3306,user='salest', passwd='salest', 
                    db='salest_database')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")
    
    df_daily_product_tr = pd_sql.read_frame('select * from daily_product_tr_summary',conn)
        
    conn.close()
    
    df_daily_product_tr['date_mon'] = df_daily_product_tr['date'].apply(lambda date: date.strftime('%Y-%m'))

    def aggregation(row):
        total_amount = row['total_amount'].sum()
        return pd.Series([total_amount], index=['total_amount'])
    
    df_monthly_product_tr = df_daily_product_tr.groupby(['date_mon','product_cate']).apply(aggregation)

    def gen_dict_total_amount(month_rows):
        monthlyDict = {}
        monthlyDictKey = month_rows.index.get_level_values('date_mon')[0]
        
        monthCateItemsStr = "{"
        for item in zip(month_rows.index.get_level_values('product_cate'),month_rows['total_amount']):
            monthCateItemsStr += "'{0}':{1},".format(item[0],item[1]);
        
        monthCateItemsStr = monthCateItemsStr[:-1]
        monthCateItemsStr += "}"
        
        monthlyDict = ast.literal_eval(monthCateItemsStr)
        monthlyDict['year_month'] = month_rows.index.get_level_values('date_mon')[0]

        return monthlyDict


    mothlyTotalAmountDictItems = df_monthly_product_tr.groupby(df_monthly_product_tr.index.get_level_values('date_mon')).apply(gen_dict_total_amount)

    mothlyTotalAmountDict = {}
    mothlyTotalAmountList = []
    for item in mothlyTotalAmountDictItems:
        mothlyTotalAmountList.append(item)
    mothlyTotalAmountDict['total_amount'] = mothlyTotalAmountList

    return mothlyTotalAmountDict;


#################################################################################################

def agg_montly_total_amount_by_product(product_cate):
    df_category = make_product_cate_detail_df(product_cate)
    
    monthlyDictItems = df_category.apply(gen_dict_total_amount,axis=1)
    
    mothlyTotalAmountDict = {}
    mothlyTotalAmountList = []
    for item in monthlyDictItems:
        mothlyTotalAmountList.append(item)
    mothlyTotalAmountDict['total_amount'] = mothlyTotalAmountList
    
    return mothlyTotalAmountDict


def make_product_cate_detail_df(product_cate):
    
    conn = MySQLdb.connect(host='173.194.254.102', 
                        port=3306,user='salest', passwd='salest', 
                        db='salest_database')
    conn.query("set character_set_connection=utf8;")
    conn.query("set character_set_server=utf8;")
    conn.query("set character_set_client=utf8;")
    conn.query("set character_set_results=utf8;")
    conn.query("set character_set_database=utf8;")

    df_daily_product_tr = pd_sql.read_frame('select * from daily_product_tr_summary',conn)

    conn.close()

    # Agg Total amoun per Month/Product combination

    df_daily_product_tr['date_mon'] = df_daily_product_tr['date'].apply(lambda date: date.strftime('%Y-%m'))
    df_daily_product_tr = df_daily_product_tr[df_daily_product_tr.product_cate == product_cate.encode('utf8')]

    column_func_tuple = [('total_amount','sum')]
    
    df_monthly_product_tr = df_daily_product_tr.groupby(['date_mon','product_name'])['total_amount'].agg(column_func_tuple)
    
    # Overall Top 10 menu items in category 
    
    df_topten_products_by_total_amount = df_daily_product_tr.groupby(['product_name']).sum().sort_values(by='total_amount', ascending=False)[:10]
    df_topten_products_by_total_amount.drop(['id','num_of_product'],axis=1, inplace=True)
    df_topten_products_by_total_amount.rename(columns={'total_amount':'overall_total_amount'},inplace=True)
    
    # Merge the above two dataframes
    df_new = df_monthly_product_tr.reset_index(level=0)
    df_merged = pd.merge(df_new, df_topten_products_by_total_amount, left_index=True, right_index=True, how='left').sort_values(by='date_mon', ascending=True)
        
    def agg_monthly_items_summary(row):
        sr_columns = row[row['overall_total_amount'].notnull()].index
        sr_values = row[row['overall_total_amount'].notnull()]['total_amount']

        etcSum = row[row['overall_total_amount'].isnull()]['total_amount'].sum()

        sr_columns = sr_columns.insert(sr_columns.size,'ETC')
        sr_etc = pd.Series([etcSum], index=['ETC'])
        sr_values = sr_values.append(sr_etc)

        return pd.Series(sr_values, index=sr_columns)
    
    df_merged_new = df_merged.reset_index(level=0)
    df_merged_new.groupby(['date_mon'])

    df_agg_monthly_summary = df_merged.groupby(['date_mon']).apply(agg_monthly_items_summary).unstack()
    df_agg_monthly_summary.fillna(0,inplace=True)
 
    return df_agg_monthly_summary


def gen_dict_total_amount(row):
    
    monthlyDict = {}
    monthlyDictStr = "{"
    for key,value in zip(row.index, row): 
        monthlyDictStr += "'{0}':{1},".format(key,value)
    
    monthlyDictStr = monthlyDictStr[:-1]
    monthlyDictStr += "}"
    
    monthlyDict = ast.literal_eval(monthlyDictStr)
    monthlyDict['year_month'] = row.name
 
    return monthlyDict


# day_of_week : W-MON, W-TUE, W-WED, W-THU, W-FRI, W-SAT, W-SUN
def analysis_timebase_sales_amount(day_of_week):
    
    conn = MySQLdb.connect(host='173.194.254.102', 
                        port=3306,user='salest', passwd='salest', 
                        db='salest_database')

    df_db_table = pd_sql.read_sql(('select * from daily_timebase_agg'),conn, index_col=['date'], parse_dates=['date'])
    conn.close()

    df_db_table.drop(['id'],axis=1, inplace=True)
    
    if(day_of_week=='All'):
        return df_db_table.apply(lambda row: round(row.mean())).to_dict()
    else:
        first_date = df_db_table.index[0].strftime('%m/%d/%Y')
        last_date = df_db_table.index[-1].strftime('%m/%d/%Y')
        target_date_idx = pd.date_range(first_date,last_date, freq=day_of_week)
        df_selected_by_day = df_db_table.ix[target_date_idx]
        df_selected_by_day.dropna(how='all',inplace='True')
        return df_selected_by_day.apply(lambda row: round(row.mean())).to_dict()
    