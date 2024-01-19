import quandl
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

quandl.ApiConfig.api_key = "SpxSuXCvQRpcCKz1vbSy"
quandl.ApiConfig.api_base = 'https://data.nasdaq.com/api/v3'


def grab_quandl(ticker, calendardate, dimension="MRQ"):
    data = quandl.get_table(
        'SHARADAR/SF1', ticker=ticker, calendardate=calendardate)
    # Annual statements with restatements and timespan is  dimension parameter
    data = data[data['dimension'] == dimension]
    data = data.fillna(0)

    def get_profit_and_loss(dataframe):
        dummy_df = pd.DataFrame()
        dummy_df['revenue'] = dataframe['revenue']  # Also known as Total Sales
        dummy_df['cogs'] = dataframe['cor']
        dummy_df['sgna'] = dataframe['sgna']
        dummy_df['depamor'] = dataframe['depamor']
        dummy_df['other_operating_expense'] = dataframe['opex']
        dummy_df['operating_income'] = dataframe['opinc']
        dummy_df['other_income_expense_net'] = (
                                                       dataframe['ebit'] + dataframe['netincnci'] + dataframe[
                                                   'netincdis']) - dataframe['opinc']
        dummy_df['interest_expense'] = dataframe['intexp']
        dummy_df['pretax_income'] = (
                                            dataframe['ebit'] + dataframe['netincnci'] + dataframe['netincdis']) - \
                                    dataframe['intexp']
        dummy_df['net_income'] = dataframe['netinc']
        dummy_df['tax_total'] = dataframe['taxexp']
        dummy_df['eps'] = dataframe['eps']
        dummy_df['ebitda'] = dataframe['ebitda']
        dummy_df['minority_interest'] = dataframe['assets'] - \
                                        (dataframe['liabilities'] + dataframe['equity'])
        dummy_df['exto_items_dis_op'] = dataframe['netincdis']
        dummy_df['dividend'] = dataframe['dps'] * dataframe['sharesbas']
        dummy_df['accrued'] = dataframe['netinc'] - dummy_df['dividend']

        return dummy_df

    def get_balance_sheet(dataframe, profit_and_loss_df):
        dummy_df = pd.DataFrame()
        dummy_df['cash_short_term_invstmnt'] = dataframe['cashneq']
        dummy_df['receivables'] = dataframe['receivables']
        dummy_df['inventories'] = dataframe['inventory']
        dummy_df['curr_invstmnt'] = dataframe['investmentsc']
        dummy_df['other_curr_assets'] = dataframe['assetsc']
        dummy_df['tot_curr_assets'] = dataframe['cashneq'] + dataframe['receivables'] + \
                                      dataframe['inventory'] + dataframe['investmentsc'] + \
                                      dataframe['assetsc']
        dummy_df['ppnenet'] = dataframe['ppnenet']
        dummy_df['invstmnt_advncs'] = dataframe['investmentsnc']
        dummy_df['intangibles'] = dataframe['intangibles']
        dummy_df['other_assets'] = dataframe['assetsnc']
        dummy_df['tot_noncurr_assets'] = dataframe['ppnenet'] + \
                                         dataframe['investmentsnc'] + \
                                         dataframe['intangibles'] + dataframe['assetsnc']
        dummy_df['total_assets'] = dataframe['assets']
        dummy_df['acc_payable'] = dataframe['payables']
        dummy_df['shortterm_debt'] = dataframe['debtc']
        dummy_df['total_curr_liabilities'] = dataframe['liabilitiesc']
        dummy_df['longterm_debt'] = dataframe['debtnc']
        dummy_df['tot_noncurr_liabilities'] = dataframe['liabilitiesnc']
        dummy_df['total_liabilities'] = dataframe['liabilities']
        dummy_df['retain_earnings'] = dataframe['retearn']
        dummy_df['tot_stockhldr_eq'] = dataframe['equity']
        dummy_df['convdebt_and_noncontrol_intrst'] = profit_and_loss_df['minority_interest']
        dummy_df['total_liabilities_equity'] = dataframe['liabilities'] + \
                                               dataframe['equity']

        return dummy_df

    def get_cash_flow(dataframe):
        dummy_df = pd.DataFrame()

        dummy_df['netcash_operating_expense'] = dataframe['ncfo']
        dummy_df['add_to_prop_equip'] = dataframe['capex']
        dummy_df['netcash_by_invst_act'] = dataframe['ncfi']
        dummy_df['netcash_by_fin_act'] = dataframe['ncff']
        dummy_df['eff_exchrate_on_cash_and_equi'] = dataframe['ncfx']

        return dummy_df

    def get_profitability_ratios(dataframe, dimension):
        ratio_df = pd.DataFrame()

        ###################### Profitability Ratios ########################################
        ratio_df['gross_margin'] = dataframe['grossmargin']
        ratio_df['ebitdamargin'] = dataframe['ebitdamargin']
        ratio_df['netmargin'] = dataframe['netmargin']
        ratio_df['ebit_ratio'] = dataframe['ebit'] / dataframe['revenue']
        ratio_df['pbt_margin'] = dataframe['ebt'] / dataframe['revenue']
        ratio_df['roe'] = dataframe['roe']
        ratio_df['roce'] = ((dataframe['netinc'] + dataframe['intexp']) /
                            (dataframe['assets'] - dataframe['liabilitiesc'])) * 100
        ratio_df['roi'] = dataframe['ebit'] / \
                          (dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['roa'] = dataframe['roa']
        ratio_df['rona'] = dataframe['netinc'] / \
                           ((dataframe['ppnenet'] + dataframe['intangibles']) +
                            dataframe['workingcapital'])
        ratio_df['return_ondebt'] = dataframe['netinc'] / \
                                    (dataframe['debtc'] + dataframe['debtnc'])

        return ratio_df

    def get_efficiency_performance_ratios(dataframe, dimension):
        ratio_df = pd.DataFrame()

        ratio_df['asset_turnratio'] = dataframe['revenue'] / \
                                      dataframe['assets'].mean()
        ratio_df['fixedass_turnratio'] = dataframe['revenue'] / \
                                         (dataframe['ppnenet']).mean()
        ratio_df['plant_turnover'] = dataframe['revenue'] / \
                                     (dataframe['ppnenet']).mean()
        ratio_df['workcap_turnratio'] = dataframe['revenue'] / \
                                        (dataframe['workingcapital']).mean()
        ratio_df['equity_turnover'] = dataframe['revenue'] / \
                                      (dataframe['equity']).mean()
        ratio_df['inventory_turn_ratio'] = dataframe['cor'] / \
                                           (dataframe['inventory']).mean()
        ratio_df['receivables_turn_ratio'] = dataframe['revenue'] / \
                                             (dataframe['receivables']).mean()
        ratio_df['payables_turn_ratio'] = dataframe['cor'] / \
                                          (dataframe['payables']).mean()
        if dimension == 'MRQ':
            ratio_df['debtor_days'] = (
                                              dataframe['receivables'].mean() / dataframe['revenue']) * 365 * (1 / 4)
            ratio_df['inv_days'] = (
                                           dataframe['inventory'].mean() / dataframe['cor']) * 365 * (1 / 4)
            ratio_df['cred_days'] = (
                                            dataframe['payables'].mean() / dataframe['cor']) * 365 * (1 / 4)
        else:
            ratio_df['debtor_days'] = (
                                              dataframe['receivables'].mean() / dataframe['revenue']) * 365
            ratio_df['inv_days'] = (
                                           dataframe['inventory'].mean() / dataframe['cor']) * 365
            ratio_df['cred_days'] = (
                                            dataframe['payables'].mean() / dataframe['cor']) * 365

        ratio_df['cash_conv'] = ratio_df['debtor_days'] + \
                                ratio_df['inv_days'] + ratio_df['cred_days']
        ratio_df['ebit_byassets'] = dataframe['ebit'] / \
                                    (dataframe['assets']).mean()
        ratio_df['ebitda_byassets'] = dataframe['ebitda'] / \
                                      (dataframe['assets'].mean())
        ratio_df['days_workcap'] = 365 / ratio_df['workcap_turnratio']
        ratio_df['cash_turnover'] = dataframe['revenue'] / dataframe['cashneq']

        return ratio_df

    def get_liquidity_ratios(dataframe, dimension):
        ratio_df = pd.DataFrame()

        ratio_df['current_ratio'] = dataframe['assetsc'] / \
                                    dataframe['liabilitiesc']
        ratio_df['quickratio_exinven'] = (
                                                 dataframe['assetsc'] - dataframe['inventory']) / dataframe[
                                             'liabilitiesc']
        ratio_df['cash_ratio'] = (
                                         dataframe['ppnenet'] + dataframe['cashneq']) / dataframe['liabilitiesc']
        ratio_df['cash_toassets'] = dataframe['cashneq'] / dataframe['assets']
        ratio_df['cash_toworkcap'] = dataframe['cashneq'] / \
                                     dataframe['workingcapital']
        ratio_df['defense_int_ratio'] = dataframe['assetsc'] / dataframe['opex']

        return ratio_df

    def get_leverage_ratios(dataframe, dimension):
        ratio_df = pd.DataFrame()

        ratio_df['debtserv_covratio'] = dataframe['opinc'] / ((dataframe['ebt'] + dataframe['intexp']) / (
                dataframe['intexp'] + dataframe['debtc'] + dataframe['debtnc']))
        ratio_df['interest_covratio'] = dataframe['ebit'] / dataframe['intexp']
        ratio_df['de_ratio'] = dataframe['de']
        ratio_df['equity_ratio'] = dataframe['equity'] / \
                                   (dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['debt_ratio'] = (
                                         dataframe['debtc'] + dataframe['debtnc']) / (
                                             dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['liab_byasset'] = dataframe['liabilities'] / dataframe['assets']
        ratio_df['debt_assetratio'] = (
                                              dataframe['debtc'] + dataframe['debtnc']) / dataframe['assets']
        ratio_df['debt_toebitda'] = (
                                            dataframe['debtc'] + dataframe['debtnc']) / dataframe['ebitda']
        ratio_df['netdebt_toebitda'] = (
                                               dataframe['debtc'] + dataframe['debtnc'] - dataframe['cashneq']) / \
                                       dataframe['ebitda']

        return ratio_df

    def get_other_ratios(dataframe, dimension):
        ratio_df = pd.DataFrame()
        ratio_df['workingcap_byassets'] = (
                                                  dataframe['assetsc'] - dataframe['liabilitiesc']) / dataframe[
                                              'assets']

        ratio_df['fixed_asset_by_long_term_debt'] = (
                                                            dataframe['ppnenet'] + dataframe['intangibles']) / (
                                                                dataframe['debtnc'] - dataframe['debtc'])
        ratio_df['debt_by_tangible_net_worth'] = (
                                                         dataframe['debtnc'] + dataframe['debtc']) / (
                                                             dataframe['assets'] - dataframe['intangibles'])
        ratio_df['interest_coverage_npbt'] = dataframe['ebt'] / \
                                             dataframe['intexp']
        ratio_df['sustainable_growth_rate'] = (
                                                      1 - ((dataframe['dps'] * dataframe['sharesbas']) / dataframe[
                                                  'netinc'])) * dataframe['roe']

        return ratio_df

    def return_financial_ratios(dataframe, span):

        ratio_df = pd.DataFrame()

        ###################### Profitability Ratios ########################################
        ratio_df['gross_margin'] = dataframe['grossmargin']
        ratio_df['ebitdamargin'] = dataframe['ebitdamargin']
        ratio_df['netmargin'] = dataframe['netmargin']
        ratio_df['ebit_ratio'] = dataframe['ebit'] / dataframe['revenue']
        ratio_df['pbt_margin'] = dataframe['ebt'] / dataframe['revenue']
        ratio_df['roe'] = dataframe['roe']
        ratio_df['roce'] = ((dataframe['netinc'] + dataframe['intexp']) /
                            (dataframe['assets'] - dataframe['liabilitiesc'])) * 100
        ratio_df['roi'] = dataframe['ebit'] / \
                          (dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['roa'] = dataframe['roa']
        ratio_df['rona'] = dataframe['netinc'] / \
                           ((dataframe['ppnenet'] + dataframe['intangibles']) +
                            dataframe['workingcapital'])
        ratio_df['return_ondebt'] = dataframe['netinc'] / \
                                    (dataframe['debtc'] + dataframe['debtnc'])

        ###################### Efficiency Performance ########################################
        ratio_df['asset_turnratio'] = dataframe['revenue'] / \
                                      dataframe['assets'].mean()
        ratio_df['fixedass_turnratio'] = dataframe['revenue'] / \
                                         (dataframe['ppnenet']).mean()
        ratio_df['plant_turnover'] = dataframe['revenue'] / \
                                     (dataframe['ppnenet']).mean()
        ratio_df['workcap_turnratio'] = dataframe['revenue'] / \
                                        (dataframe['workingcapital']).mean()
        ratio_df['equity_turnover'] = dataframe['revenue'] / \
                                      (dataframe['equity']).mean()
        ratio_df['inventory_turn_ratio'] = dataframe['cor'] / \
                                           (dataframe['inventory']).mean()
        ratio_df['receivables_turn_ratio'] = dataframe['revenue'] / \
                                             (dataframe['receivables']).mean()
        ratio_df['payables_turn_ratio'] = dataframe['cor'] / \
                                          (dataframe['payables']).mean()
        if span == 'MRQ':
            ratio_df['debtor_days'] = (
                                          dataframe['receivables']).mean() * 365 * (1 / 4)
            ratio_df['inv_days'] = (
                                           dataframe['inventory'].mean() / dataframe['cor']) * 365 * (1 / 4)
            ratio_df['cred_days'] = (
                                            dataframe['payables'].mean() / dataframe['cor']) * 365 * (1 / 4)
        else:
            ratio_df['debtor_days'] = (dataframe['receivables']).mean() * 365
            ratio_df['inv_days'] = (
                                           dataframe['inventory'].mean() / dataframe['cor']) * 365
            ratio_df['cred_days'] = (
                                            dataframe['payables'].mean() / dataframe['cor']) * 365

        ratio_df['cash_conv'] = ratio_df['debtor_days'] + \
                                ratio_df['inv_days'] + ratio_df['cred_days']
        ratio_df['ebit_byassets'] = dataframe['ebit'] / \
                                    (dataframe['assets']).mean()
        ratio_df['ebitda_byassets'] = dataframe['ebitda'] / \
                                      (dataframe['assets'].mean())
        ratio_df['days_workcap'] = 365 / ratio_df['workcap_turnratio']
        ratio_df['cash_turnover'] = dataframe['revenue'] / dataframe['cashneq']

        ###################### Liquidity ########################################
        ratio_df['current_ratio'] = dataframe['assetsc'] / \
                                    dataframe['liabilitiesc']
        ratio_df['quickratio_exinven'] = (
                                                 dataframe['assetsc'] - dataframe['inventory']) / dataframe[
                                             'liabilitiesc']
        ratio_df['cash_ratio'] = (
                                         dataframe['ppnenet'] + dataframe['cashneq']) / dataframe['liabilitiesc']
        ratio_df['cash_toassets'] = dataframe['cashneq'] / dataframe['assets']
        ratio_df['cash_toworkcap'] = dataframe['cashneq'] / \
                                     dataframe['workingcapital']
        ratio_df['defense_int_ratio'] = dataframe['assetsc'] / dataframe['opex']

        ###################### Leverage ########################################
        ratio_df['debtserv_covratio'] = dataframe['opinc'] / ((dataframe['ebt'] + dataframe['intexp']) / (
                dataframe['intexp'] + dataframe['debtc'] + dataframe['debtnc']))
        ratio_df['interest_covratio'] = dataframe['ebit'] / dataframe['intexp']
        ratio_df['de_ratio'] = dataframe['de']
        ratio_df['equity_ratio'] = dataframe['equity'] / \
                                   (dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['debt_ratio'] = (
                                         dataframe['debtc'] + dataframe['debtnc']) / (
                                             dataframe['assets'] - dataframe['liabilitiesc'])
        ratio_df['liab_byasset'] = dataframe['liabilities'] / dataframe['assets']
        ratio_df['debt_assetratio'] = (
                                              dataframe['debtc'] + dataframe['debtnc']) / dataframe['assets']
        ratio_df['debt_toebitda'] = (
                                            dataframe['debtc'] + dataframe['debtnc']) / dataframe['ebitda']
        ratio_df['netdebt_toebitda'] = (
                                               dataframe['debtc'] + dataframe['debtnc'] - dataframe['cashneq']) / \
                                       dataframe['ebitda']

        ###################### Other ########################################
        ratio_df['workingcap_byassets'] = (
                                                  dataframe['assetsc'] - dataframe['liabilitiesc']) / dataframe[
                                              'assets']

        ###################### Recently added ratios ########################################
        ratio_df['fixed_asset_by_long_term_debt'] = (
                                                            dataframe['ppnenet'] + dataframe['intangibles']) / (
                                                                dataframe['debtnc'] - dataframe['debtc'])
        ratio_df['debt_by_tangible_net_worth'] = (
                                                         dataframe['debtnc'] + dataframe['debtc']) / (
                                                             dataframe['assets'] - dataframe['intangibles'])
        ratio_df['interest_coverage_npbt'] = dataframe['ebt'] / \
                                             dataframe['intexp']
        ratio_df['sustainable_growth_rate'] = (
                                                      1 - ((dataframe['dps'] * dataframe['sharesbas']) / dataframe[
                                                  'netinc'])) * dataframe['roe']

        return ratio_df

    profit_and_loss_df = get_profit_and_loss(data)
    balance_sheet_df = get_balance_sheet(data, profit_and_loss_df)
    cash_flow_df = get_cash_flow(data)

    profitability_ratios_df = get_profitability_ratios(data, dimension)
    efficiency_performance_ratios_df = get_efficiency_performance_ratios(
        data, dimension)
    liquidity_ratios_df = get_liquidity_ratios(data, dimension)
    leverage_ratios_df = get_leverage_ratios(data, dimension)
    other_ratios_df = get_other_ratios(data, dimension)

    output = {"calendardate": calendardate,
              "dimension": dimension,
              "profit_and_loss": profit_and_loss_df.iloc[0].to_dict(),
              "balance_sheet": balance_sheet_df.iloc[0].to_dict(),
              "cash_flow": cash_flow_df.iloc[0].to_dict(),
              "profitability_ratios": profitability_ratios_df.iloc[0].to_dict(),
              "efficiency_performance_ratios": efficiency_performance_ratios_df.iloc[0].to_dict(),
              "liquidity_ratios": liquidity_ratios_df.iloc[0].to_dict(),
              "leverage_ratios": leverage_ratios_df.iloc[0].to_dict(),
              "other_ratios_df": other_ratios_df.iloc[0].to_dict()}

    return output