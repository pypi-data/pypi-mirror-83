import numpy as np
import pandas as pd
import os
pd.set_option('precision', 3)

class MarkovChainBQ(object):

    '''
    Variables

    conversion_summary
    conversion_paths

    Transition Matrix
        trans_matrix
        trans_conversion_matrix
        perc_matrix

    Removal Effect

        removal_effect_attribution_final
        removal_effect_attribution

    Touch Conversion
        first_touch_converison_attribution
        last_touch_conversion_attribution
    '''


    def __init__(self, filename):
        '''

        :param filname:
            Source file name
        '''

        self.filename = filename

    def read_file(self):
        print ("Read File")
        columns = ['date', 'fullVisitorId', 'visitId', 'visitNumber', 'channelGrouping', 'hits_page_pagePath']
        self.data = pd.read_csv('data.csv', usecols = columns)
        # self.data = pd.read_csv(self.filename, usecols = columns)

        self.preprocess_data()
        self.preprocess()

    def preprocess_data(self):

        print ("Preprocess Data")
        data = self.data
        data.date = pd.to_datetime(data.date.map(str), format='%Y%m%d')
        data['unique_session'] = data.fullVisitorId.map(str) + '-' + data.visitId.map(str)

        data.sort_values(['fullVisitorId', 'date', 'visitId'], inplace=True)
        data['conversion'] = 0

        conversion_mask = data.hits_page_pagePath.str.contains(r'lpconfirm|/thank-you|/scheduler-thank-you')
        data.loc[conversion_mask, 'conversion'] = 1

        data.drop('hits_page_pagePath', inplace=True, axis='columns')

        data.drop_duplicates(inplace=True)

        data.sort_values(['unique_session', 'conversion'], inplace=True, ascending=[True, False])

        data['delete_row'] = data['unique_session'].shift()
        data = data[~(data['delete_row'] == data['unique_session'])]

        data.drop(['visitNumber', 'delete_row'], axis='columns', inplace=True)
        self.data = data

    def preprocess(self):
        data = self.data
        sorted_data = data.sort_values(['fullVisitorId', 'visitId'])

        df_conversion_count = sorted_data.copy()
        group_data = sorted_data.groupby(['fullVisitorId'], sort=True)
        df_conversion_count['path_no'] = group_data.agg({'conversion': {'path_no': 'shift'}}).fillna(1)[
            ('conversion', 'path_no')]
        df_conversion_count['path_no'] = df_conversion_count.groupby('fullVisitorId').agg({'path_no': 'cumsum'})

        del (group_data)
        df_navigation_paths_group = df_conversion_count.groupby(['fullVisitorId', 'path_no'])
        df_navigation_paths = df_navigation_paths_group.agg({'channelGrouping': {'path': lambda x: ' > '.join(x)},'conversion': {'conversion': 'sum'}})  ## Summming all the converison values

        df_navigation_paths.columns = df_navigation_paths.columns.droplevel(0)  ## Removing top group columns
        df_navigation_paths.reset_index(['fullVisitorId', 'path_no'], inplace=True)
        df_navigation_paths.columns = pd.Index(['fullVisitorId', 'path_no', 'path', 'conversion'])

        conversion_mask = df_navigation_paths['conversion'] == 1
        self.conversion_paths = df_navigation_paths[conversion_mask]

        self.conversion_summary = self.conversion_paths.groupby('path').agg({'conversion': 'sum'}).sort_values('conversion', ascending=False).reset_index()

        ## Full conversion Paths
        self.conversion_paths = self.conversion_paths.copy()
        self.conversion_paths['path'] = self.conversion_paths['path'].apply(lambda x: '(start) > ' + x + ' > (conversion)')

    def removal_effect(self):

        '''
        This function calculate the removal effect for every function
        :return:
        '''
        print ("Removal Effect")
        self.removal_effect_attribution = []
        inital = self.trans_matrix[['channel_from', 'channel_to']]

        for i in range(self.channel_list.shape[0]):
            channel = self.channel_list[i]
            reserve = self.res.copy()

            # Creating mask
            channel_from_mask = reserve.channel_from == channel
            reserve.loc[channel_from_mask, 'channel_from'] = None

            # Creating mask and assigning the '(null)' value
            channel_to_mask = reserve.channel_to == channel
            # reserve.channel_to[channel_to_mask] = '(null)'
            reserve.loc[channel_to_mask, 'channel_to'] = '(null)'
            reserve.dropna(axis='rows', inplace=True)

            # Calculating the Sum of all the values
            removal = reserve.groupby(['channel_from', 'channel_to']).agg({'n': 'sum'}).reset_index()
            removal['perc'] = removal.groupby('channel_from')['n'].apply(lambda x: x / x.sum())

            removal = pd.concat([removal, self.dummy], axis='rows')

            removal = pd.merge(inital, removal, on=['channel_from', 'channel_to'], how='left')
            removal.fillna(0, inplace=True)

            cast_matrix = pd.pivot_table(data=removal, index='channel_from', columns='channel_to', values='perc',
                                         aggfunc=np.sum).fillna(0)
            cast_matrix[channel] = 0
            cast_matrix.loc[channel] = 0

            inist_n1 = pd.pivot_table(removal, index='channel_from', columns='channel_to', values='n',
                                      aggfunc=np.sum).fillna(0)
            inist_n1[channel] = 0
            inist_n1.loc[channel] = 0
            inist_n1 = inist_n1.loc['(start)']

            res_num = np.matmul(inist_n1, (np.linalg.matrix_power(cast_matrix, 100000)))
            df_cache = pd.DataFrame([[channel, res_num[np.argmax(inist_n1.index == "(conversion)")]]])
            # df_cache = pd.DataFrame([[channel, res_num.loc['(conversion)']]])
            df_cache.columns = ['Channel_name', 'conversions']
            self.removal_effect_attribution.append(df_cache)

        self.removal_effect_attribution = pd.concat(self.removal_effect_attribution, axis='rows', ignore_index=True)

        self.removal_effect_attribution['tot_conversion'] = np.sum(self.conversion_paths['conversion'])
        self.removal_effect_attribution['removal_effect'] = (self.removal_effect_attribution.tot_conversion - self.removal_effect_attribution.conversions) / self.removal_effect_attribution.tot_conversion
        self.removal_effect_attribution['tot_impact'] = np.sum(self.removal_effect_attribution.removal_effect)
        self.removal_effect_attribution['weighted_impact'] = self.removal_effect_attribution.removal_effect / self.removal_effect_attribution.tot_impact
        self.removal_effect_attribution['attrib_model_conversions'] = np.int32(np.round(self.removal_effect_attribution.tot_conversion * self.removal_effect_attribution.weighted_impact))

        # self.removal_effect_attribution.to_csv('./self.removal_effect_attributionutes.csv', index=False)
        self.removal_effect_attribution = self.removal_effect_attribution.round(3)
        self.removal_effect_matrix = self.removal_effect_attribution[['Channel_name', 'removal_effect']]
        self.removal_effect_matrix['removal_conversion'] = np.int32(np.round(self.removal_effect_matrix.removal_effect * self.removal_effect_attribution.tot_conversion))
        # df_removal_effect.to_csv('./df_removal_effect.csv', index=False)

        self.removal_effect_attribution_final = self.removal_effect_attribution[['Channel_name', 'attrib_model_conversions']]
        self.removal_effect_attribution_final.channel_name = self.removal_effect_attribution_final.Channel_name.str.strip()
        # self.removal_effect_attribution_final.to_csv('./self.removal_effect_attributionutes_final.csv', index=False)

    def touch_conversion(self):
        '''
        This function will calculate the first and last touch conversion matrix
        :return:
        '''

        print ("Touch Conversion")
        df_ft_lt_channel = self.conversion_paths.copy()
        df_ft_lt_channel['path'] = df_ft_lt_channel['path'].apply(lambda x: x.replace('(start) > ', '')).apply(
            lambda x: x.replace('> (conversion)', ''))
        df_ft_lt_channel['channel_name_ft'] = df_ft_lt_channel['path'].str.replace(r'>.*', '').str.strip()
        df_ft_lt_channel['channel_name_lt'] = df_ft_lt_channel['path'].str.replace(r'.*>', '').str.strip()

        df_ft = df_ft_lt_channel.groupby('channel_name_ft').agg({'conversion': {'first_touch_': 'sum'}}).reset_index()
        df_ft.columns = ['{0}{1}'.format(l1, l0) for l0, l1 in df_ft.columns]

        df_lt = df_ft_lt_channel.groupby('channel_name_lt').agg({'conversion': {'last_touch_': 'sum'}}).reset_index()
        df_lt.columns = ['{0}{1}'.format(l1, l0) for l0, l1 in df_lt.columns]

        df_ft_and_lt = pd.merge(df_ft, df_lt, left_on='channel_name_ft', right_on='channel_name_lt')
        df_ft_and_lt.drop('channel_name_lt', axis='columns')
        df_ft_and_lt.rename(columns={'channel_name_ft': 'channel_name'}, inplace=True)

        df_ft_and_mc_attribution = pd.merge(df_ft, self.removal_effect_attribution_final, left_on='channel_name_ft',
                                            right_on='Channel_name')
        df_ft_and_mc_attribution.drop('Channel_name', axis='columns', inplace=True)
        df_ft_and_mc_attribution.rename(columns={'channel_name_ft': 'channel_name'}, inplace=True)
        df_ft_and_mc_attribution['percentage_change'] = (df_ft_and_mc_attribution.attrib_model_conversions - df_ft_and_mc_attribution.first_touch_conversion) / df_ft_and_mc_attribution.attrib_model_conversions
        # df_ft_and_mc_attribution.to_csv('./first_touch and markov attributes.csv')

        df_lt_and_mc_attribution = pd.merge(df_lt, self.removal_effect_attribution_final, left_on='channel_name_lt',
                                            right_on='Channel_name')
        df_lt_and_mc_attribution.drop('Channel_name', axis='columns', inplace=True)
        df_lt_and_mc_attribution.rename(columns={'channel_name_lt': 'channel_name'}, inplace=True)
        df_lt_and_mc_attribution['percentage_change'] = (df_lt_and_mc_attribution.attrib_model_conversions - df_lt_and_mc_attribution.last_touch_conversion) / df_lt_and_mc_attribution.attrib_model_conversions
        # df_lt_and_mc_attribution.to_csv('./last_touch and markov attributes.csv')
        self.first_touch_conversion_attribution = df_ft_and_mc_attribution.round(3)
        self.last_touch_conversion_attribution = df_lt_and_mc_attribution.round(3)

    def transition_matrix(self):
        '''
        Calculating Transition matrix for given data
        '''

        print ("Calculating Transition Matrix")
        path_df = self.conversion_paths.path.str.replace('(start) > ', '').str.replace(' > (conversion)', '').str.split(' > ', expand=True)
        path_df.columns = map(lambda x: 'ord_' + str(x), path_df.columns)
        res = []
        print ("Before loop")
        for i in range(path_df.shape[1] - 1):
            cache = path_df[list(map(lambda x: 'ord_' + str(x), np.arange(i, i + 2)))]
            cache.dropna(axis='rows', inplace=True)
            cache = cache.groupby(list(map(lambda x: 'ord_' + str(x), np.arange(i, i + 2)))).size().reset_index()
            cache.columns = ['channel_from', 'channel_to', 'n']
            res.append(cache)
        res = pd.concat(res, axis=0, ignore_index=True)
        self.res = res.groupby(['channel_from', 'channel_to']).agg({'n': 'sum'}).reset_index()
        print ("After Loop")
        ## Taking unique values of channel_list Need for removal effect
        self.channel_list = pd.unique(res.channel_from)
        self.channel_list = self.channel_list[self.channel_list != '(start)']
        
        trans_matrix = res.groupby(['channel_from', 'channel_to']).agg({'n': 'sum'}).reset_index()
        trans_matrix['perc'] = trans_matrix.groupby('channel_from')['n'].apply(lambda x: x / x.sum())
        print ("Calculated Transition Matrix")
        ## Creating Dummy Dataframe
        self.dummy = pd.DataFrame.from_dict({
            'channel_from': ['(start)', '(conversion)', '(null)'],
            'channel_to': ['(start)', '(conversion)', '(null)'],
            'n': [0, 0, 0],
            'perc': [0, 1, 1]
        })

        self.trans_matrix = pd.concat([trans_matrix, self.dummy], axis=0, ignore_index=True)
        self.perc_matrix = self.trans_matrix.pivot_table(values='perc', index='channel_from', columns='channel_to').fillna(0).round(3)
        self.trans_conversion_matrix = self.trans_matrix.pivot_table(values='n', index='channel_from', columns='channel_to').fillna(0).round(3)


    def init_markov(self):
        self.read_file()
        self.transition_matrix()
        self.removal_effect()
        self.touch_conversion()


# if __name__ == "__main__":
#     file = None
#     mk_chain = MarkovChainBQ(file)
#     mk_chain.init_markov()
