from file_extractor import image_to_text,pdf_to_jpg
from fuzzywuzzy import fuzz
import json
import pandas as pd

restructured_data = {}
item_list=["balance_sheet","profit_and_loss","cash_flow"]
pdf_file = "AMZN.pdf"  # Replace with your PDF file path
path_ocr = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Replace with your path
img = pdf_to_jpg(pdf_file)


def ratios(response):
    term_file = open('terminology.json')
    term_json = json.load(term_file)
    # print(term_json)
    my_json = {}
    restructured_data={}
    temp = []
    for res in response:
        for year in res.keys():
            summ = 0
            for lis in res[year]:
                for int_term in lis.keys():

                    #print("res=",res,"\n","year=",year,"\n","lis=",lis,"\n","int_term=",int_term,"\n","next")

                    ### For Total Net Sales
                    for term in term_json['Sales']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Sales' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Total Net Income
                    for term in term_json['Net Income']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Net Income' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Total Income Tax
                    for term in term_json['Income Tax Total']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Income Tax Total' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Interest Expense
                    for term in term_json['Interest Expense']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Interest Expense' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Interest Income
                    for term in term_json['Interest Income']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>90:
                            old_key = int_term
                            new_dic = {'Interest Income' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Depreciation and Amortization
                    for term in term_json['Depreciation and Amortization']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Dep and Amor' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Cost of Goods Sold
                    for term in term_json['Cost of Goods Sold']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'COGS' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Total Equity
                    for term in term_json['Total Equity']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Total Equity' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Long term Debt
                    for term in term_json['Long term Debt']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Long term Debt' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Total Assets
                    for term in term_json['Total Assets']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Total Assets' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Current Liabilities
                    for term in term_json['Total Current Liabilities']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Total Current Liabilities' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For PPNNet
                    for term in term_json['PPNNet']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'PPNNet' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Intangible
                    for term in term_json['Intangible']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Intangible' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Intangible
                    for term in term_json['Goodwill']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Goodwill' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Current Assets
                    for term in term_json['Total Current Assets']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Current Assets' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Inventories
                    for term in term_json['Inventories']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Inventories' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Receivables
                    for term in term_json['Receivables']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Receivables' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Cash
                    for term in term_json['Cash and Short-Term Investments']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Cash' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Operating Income
                    for term in term_json['Operating Income']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Operating Income' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Income before Tax
                    for term in term_json['Income before Tax']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Income before Tax' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Purchases
                    for term in term_json['Purchases']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Purchases' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Purchases
                    for term in term_json['Accounts Payable']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Accounts Payable' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Cash in ops activity
                    for term in term_json['Cash in ops activity']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Cash Ops' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Cash in Invest activity
                    for term in term_json['Cash in Invest activity']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Cash Invset' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Operating Expense
                    for term in term_json['Operating Expense']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Operating Expense' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Short term Debt
                    for term in term_json['Short term Debt']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Short term Debt' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})

                    ### For Dividends Paid
                    for term in term_json['Dividends Paid']:
                        term = term.replace(' ', '_').lower()
                        similarity_ratio = fuzz.ratio(int_term,term)
                        if similarity_ratio>80:
                            old_key = int_term
                            new_dic = {'Dividends Paid' if key == old_key else key: value for key, value in lis.items()}
                            temp.append({year:new_dic})
                    
                        
                        
        
    
    for item in temp:
        for yr, val in item.items():
            if yr not in restructured_data:
                restructured_data[yr] = {}
            restructured_data[yr].update(val)

    #print("\nstarts here",restructured_data)    
    return restructured_data
    
        
dataframe = pd.DataFrame(restructured_data).T
    #dataframe.to_csv('your_dataframe.csv', index=False)

def calculations():
    global dataframe

    ## Metrics calculation    

    try:
        dataframe['ebidta'] = dataframe['Income before Tax']+(dataframe['Interest Income']-dataframe['Interest Expense']) + dataframe['Dep and Amor']
    except:
        dataframe['ebidta'] = 0

    try:
        dataframe['ebit'] = dataframe['Income before Tax']+(dataframe['Interest Income']-dataframe['Interest Expense'])
    except:
        dataframe['ebit'] = 0
                                
    try:
        dataframe['ebt'] = dataframe['Income before Tax']
    except:
        dataframe['ebt'] = 0

    try:
        dataframe['capemployed'] = dataframe['Total Assets']-dataframe['Total Current Liabilities']
    except:
        dataframe['capemployed'] = 0

    try:
        dataframe['networkcap'] = dataframe['Current Assets']-dataframe['Total Current Liabilities']
    except:
        dataframe['networkcap'] = 0

    try:
        dataframe['fixassets'] = dataframe['PPNNet']+dataframe['Intangible']+dataframe['Goodwill']
    except:
        dataframe['fixassets'] = 0
                                
    ## Ratios Calculation
    dataframeratios = pd.DataFrame()
    try:
        dataframeratios['gross_margin'] = (dataframe['Sales']-dataframe['COGS'])/dataframe['Sales']
    except:
        dataframeratios['gross_margin'] = 0
    
    try:
        dataframeratios['netmargin'] = dataframe['Net Income']/dataframe['Sales']
    except:
        dataframeratios['netmargin'] = 0

    try:
        dataframeratios['ebit_ratio'] = dataframe['ebit']/dataframe['Sales']
    except:
        dataframeratios['ebit_ratio'] = 0

    try:
        dataframeratios['pbt_margin'] = dataframe['ebt']/dataframe['Sales']
    except:
        dataframeratios['pbt_margin'] = 0

    try:
        dataframeratios['roe'] = (dataframe['Net Income'])/dataframe['Total Equity'].mean()
    except:
        dataframeratios['roe'] = 0

    try:
        dataframeratios['return_ondebt'] = (dataframe['Net Income'])/(dataframe['Long term Debt']+dataframe['Short term Debt'])
    except:
        dataframeratios['return_ondebt'] = 0

    try:
        dataframeratios['roa'] = (dataframe['Net Income'])/dataframe['Total Assets'].mean()
    except:
        dataframeratios['roa'] = 0

    try:
        dataframeratios['roce'] = (dataframe['Net Income'] + dataframe['Interest Income'])/dataframe['capemployed'].mean()
    except:
        dataframeratios['roce'] = 0

    try:
        dataframeratios['roi'] = dataframe['ebit']/dataframe['capemployed'].mean()
    except:
        dataframeratios['roi'] = 0

    try:
        dataframeratios['rona'] = dataframe['Net Income']/(dataframe['fixassets']+dataframe['networkcap']).mean()
    except:
        dataframeratios['rona'] = 0

    try:
        dataframeratios['asset_turnratio'] = dataframe['Sales']/dataframe['Total Assets'].mean()
    except:
        dataframeratios['asset_turnratio'] = 0

    try:
        dataframeratios['fixedass_turnratio'] = dataframe['Sales']/(dataframe['fixassets']-dataframe['Intangible']).mean()
    except:
        dataframeratios['fixedass_turnratio'] = 0

    try:
        dataframeratios['plant_turnover'] = dataframe['Sales']/dataframe['PPNNet'].mean()
    except:
        dataframeratios['plant_turnover'] = 0

    try:
        dataframeratios['workcap_turnratio'] = dataframe['Sales']/dataframe['networkcap'].mean()
    except:
        dataframeratios['workcap_turnratio'] = 0

    try:
        dataframeratios['equity_turnover'] = dataframe['Sales']/dataframe['Total Equity'].mean()
    except:
        dataframeratios['equity_turnover'] = 0

    try:
        dataframeratios['inventory_turn_ratio'] = dataframe['COGS']/dataframe['Inventories'].mean()
    except:
        dataframeratios['inventory_turn_ratio'] = 0

    try:
        dataframeratios['receivables_turn_ratio'] = dataframe['Sales']/dataframe['Receivables'].mean()
    except:
        dataframeratios['receivables_turn_ratio'] = 0

    try:
        dataframeratios['ebit_byassets'] = dataframe['ebit']/dataframe['Total Assets'].mean()
    except:
        dataframeratios['ebit_byassets'] = 0

    try:
        dataframeratios['ebitda_byassets'] = dataframe['ebidta']/dataframe['Total Assets'].mean()
    except:
        dataframeratios['ebitda_byassets'] = 0

    try:
        dataframeratios['days_workcap'] = 365/dataframe['workcap_turnratio']
    except:
        dataframeratios['days_workcap'] = 0

    try:
        dataframeratios['cash_turnover'] = dataframe['Sales']/dataframe['Cash']
    except:
        dataframeratios['cash_turnover'] = 0

    try:
        dataframeratios['current_ratio'] = dataframe['Current Assets']/dataframe['Total Current Liabilities']
    except:
        dataframeratios['current_ratio'] = 0

    try:
        dataframeratios['quickratio_exinven'] = (dataframe['Current Assets']-dataframe['Inventories'])/dataframe['Total Current Liabilities']
    except:
        dataframeratios['quickratio_exinven'] = 0

    try:
        dataframeratios['cash_toassets'] = dataframe['Cash']/dataframe['Total Assets']
    except:
        dataframeratios['cash_toassets'] = 0

    try:
        dataframeratios['cash_toworkcap'] = dataframe['Cash']/(dataframe['Current Assets']-dataframe['Total Current Liabilities'])
    except:
        dataframeratios['cash_toworkcap'] = 0

    try:
        if "Purchases" not in dataframe.columns:
            dataframeratios['payables_turn_ratio'] = dataframe['COGS']/dataframe['Accounts Payable'].mean()
        else:
            dataframeratios['payables_turn_ratio'] = dataframe['Purchases']/dataframe['Accounts Payable'].mean()
    except:
        dataframeratios['payables_turn_ratio'] = 0

    try:
        dataframeratios['debtor_days'] = (dataframe['Receivables'].mean())*365
    except:
        dataframeratios['debtor_days'] = 0

    try:
        dataframeratios['inv_days'] = (dataframe['Inventories'].mean()/dataframe['COGS'])*365
    except:
        dataframeratios['inv_days'] = 0

    try:
        if "Purchases" not in dataframe.columns:
            dataframeratios['cred_days'] = (dataframe['Accounts Payable'].mean()/dataframe['COGS'])*365
        else:
            dataframeratios['cred_days'] = (dataframe['Accounts Payable'].mean()/dataframe['Purchases'])*365
    except:
        dataframeratios['cred_days'] = 0

    try:
        dataframeratios['cash_conv'] = dataframeratios['debtor_days']+dataframeratios['inv_days']+dataframeratios['cred_days']
    except:
        dataframeratios['cash_conv'] = 0

    try:
        dataframeratios['fcf_tosales'] = dataframe['Cash Ops']+dataframe["Cash Invest"]
    except:
        dataframeratios['fcf_tosales'] = 0

    try:
        dataframeratios['cash_ratio'] = (dataframe['PPNNet']+dataframe["Cash"])/dataframe['Total Current Liabilities']
    except:
        dataframeratios['cash_ratio'] = 0

    try:
        dataframeratios['defense_int_ratio'] = dataframe['Current Assets']/dataframe['Operating Expense']
    except:
        dataframeratios['defense_int_ratio'] = 0

    try:
        dataframeratios['interest_covratio'] = dataframe['ebit']/dataframe['Interest Income']
    except:
        dataframeratios['interest_covratio'] = 0

    try:
        dataframeratios['de_ratio'] = (dataframe['Long term Debt']+dataframe['Short term Debt'])/dataframe['Total Equity']
    except:
        dataframeratios['de_ratio'] = 0

    try:
        dataframeratios['equity_ratio'] = dataframe['Total Equity']/dataframe['capemployed']
    except:
        dataframeratios['equity_ratio'] = 0

    try:
        dataframeratios['debt_ratio'] = (dataframe['Long term Debt']+dataframe['Short term Debt'])/dataframe['capemployed']
    except:
        dataframeratios['debt_ratio'] = 0

    try:
        dataframeratios['liab_byasset'] = dataframe['Total Current Liabilities']/dataframe['Total Assets']
    except:
        dataframeratios['liab_byasset'] = 0

    try:
        dataframeratios['debt_assetratio'] = (dataframe['Long term Debt']+dataframe['Short term Debt'])/dataframe['Total Assets']
    except:
        dataframeratios['debt_assetratio'] = 0

    try:
        dataframeratios['debt_toebitda'] = (dataframe['Long term Debt']+dataframe['Short term Debt'])/dataframe['ebidta']
    except:
        dataframeratios['debt_toebitda'] = 0

    try:
        dataframeratios['netdebt_toebitda'] = ((dataframe['Long term Debt']+dataframe['Short term Debt'])-dataframe['Cash'])/dataframe['ebidta']
    except:
        dataframeratios['netdebt_toebitda'] = 0

    try:
        dataframeratios['workingcap_byassets'] = (dataframe['Current Assets']-dataframe['Total Current Liabilities'])/dataframe['Total Assets']
    except:
        dataframeratios['workingcap_byassets'] = 0

    try:
        dataframeratios['fixed_asset_by_long_term_debt'] = dataframe['fixassets']/(dataframe['Long term Debt']-dataframe['Short term Debt'])
    except:
        dataframeratios['fixed_asset_by_long_term_debt'] = 0

    try:
        dataframeratios['debt_by_tangible_net_worth'] = (dataframe['Long term Debt']+dataframe['Short term Debt'])/(dataframe['Total Assets']-dataframe['Intangible'])
    except:
        dataframeratios['debt_by_tangible_net_worth'] = 0

    try:
        dataframeratios['interest_coverage_npbt'] = dataframe['ebt']/dataframe['Interest Income']
    except:
        dataframeratios['interest_coverage_npbt'] = 0

    try:
        dataframeratios['interest_coverage_oc'] = dataframe['Cash Ops']/dataframe['Interest Income']
    except:
        dataframeratios['interest_coverage_oc'] = 0

    try:
        dataframeratios['sustainable_growth_rate'] = (1-(dataframe['Dividends Payed']/dataframe['Net Income']))*dataframeratios['roe']
    except:
        dataframeratios['sustainable_growth_rate'] = 0

    try:
        dataframeratios['debtserv_covratio'] = dataframe['Operating Income']/((dataframe['Income before Tax']+dataframe['Interest Expense'])/(dataframe['Interest Expense']+dataframe['Short term Debt']+dataframe['Long term Debt']))
    except:
        dataframeratios['debtserv_covratio'] = 0




    dataframeratios = dataframeratios.round(4)
    print("\nratos here",dataframeratios)                    
                    
    return dataframeratios
    

#for merging dictionaries
def merge_nested_dicts(dict1, dict2):
    """
    Merge two nested dictionaries.
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            merge_nested_dicts(dict1[key], value)
        else:
            # Update or add the key-value pair
            dict1[key] = value



def structure():
    merged_data={}
    for i in item_list:
        if i=="balance_sheet":
            print("\n\nfor balance sheet")
            pg1,pg2=38,39
            your_json = image_to_text(path_ocr,img,pg1=pg1,pg2=pg2)           
            bal_dict=ratios(your_json)
            #print("\n",bal_dict)

        if i=="profit_and_loss":
            print("\n\nfor profit and loss")
            pg1,pg2= 36,37
            your_json = image_to_text(path_ocr,img,pg1=pg1,pg2=pg2)           
            pl_dict=ratios(your_json)
            #print("\n",pl_dict)

        if i =="cash_flow":
            print("\n\nfor cash flow")
            pg1,pg2=35,36
            your_json = image_to_text(path_ocr,img,pg1=pg1,pg2=pg2)           
            cf_dict=ratios(your_json)
            #print("\n",cf_dict)

    merged_data={
    'balance_sheet': bal_dict,
    'profit_and_loss': pl_dict,
    'cash_flow': cf_dict
    }
    #formatting date wise
    combined_dict_2 = {}

    # Iterate through years
    for year, categories in merged_data['balance_sheet'].items():
        # Create a dictionary for the current year
        combined_dict_2[year] = {}

        # Add balance_sheet data for the current year
        combined_dict_2[year]['balance_sheet'] = categories

        # Add profit_and_loss data for the current year
        combined_dict_2[year]['profit_and_loss'] = merged_data['profit_and_loss'][year]

        # Add cash_flow data for the current year
        combined_dict_2[year]['cash_flow'] = merged_data['cash_flow'][year]

 
        print("\nfinally\n",combined_dict_2)

        



        
structure()



