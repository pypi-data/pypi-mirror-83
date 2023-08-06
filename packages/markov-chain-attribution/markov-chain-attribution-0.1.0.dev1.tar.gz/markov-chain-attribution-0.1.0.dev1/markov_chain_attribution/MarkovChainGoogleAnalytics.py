import numpy as np
import pandas as pd
import os


class MarkovChainGA(object):

    def __init__(self, filename):
        '''
            Variables
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

        :param filname:
            Source file name
        '''
        self.filename = filename
        pass

    def read_file(self):

        # data = pd.read_csv(os.path.join(self.filename, os.listdir(self.filename)[0]), engine = "python", skiprows = 6)
        data = pd.read_csv('data.csv', engine = "python", skiprows = 6)
        if ('Conversion Value' in data.columns):
            data.drop(['Conversion Value'], axis='columns', inplace=True)
        data.columns = ['path', 'conversion']
        # data.rename(columns={'MCF Channel Grouping Path': 'path', 'Conversions': 'conversion'}, inplace=True)
        self.conversion_paths = data
        self.conversion_paths['path'] = self.conversion_paths['path'].apply(
            lambda x: '(start) > ' + x + ' > (conversion)')

    def removal_effect(self):

        '''
        This function calculate the removal effect for every function
        :return:
        '''
        self.removal_effect_attribution = []
        inital = self.trans_matrix[['channel_from', 'channel_to']]

        for i in range(self.channel_list.shape[0]):
            channel = self.channel_list[i]
            reserve = self.res.copy()

            # Creating mask
            channel_from_mask = reserve.channel_from == channel
            reserve.loc[channel_from_mask, 'channel_from'] = None
            # reserve.channel_from[channel_from_mask] = None


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
            df_cache.columns = ['Channel_name', 'conversions']
            self.removal_effect_attribution.append(df_cache)

        self.removal_effect_attribution = pd.concat(self.removal_effect_attribution, axis='rows', ignore_index=True)

        self.removal_effect_attribution['tot_conversion'] = np.sum(self.conversion_paths['conversion'])
        self.removal_effect_attribution['removal_effect'] = (self.removal_effect_attribution.tot_conversion - self.removal_effect_attribution.conversions) / self.removal_effect_attribution.tot_conversion
        self.removal_effect_attribution['tot_impact'] = np.sum(self.removal_effect_attribution.removal_effect)
        self.removal_effect_attribution['weighted_impact'] = self.removal_effect_attribution.removal_effect / self.removal_effect_attribution.tot_impact
        self.removal_effect_attribution['attribution_conversion'] = np.int32(np.round(self.removal_effect_attribution.tot_conversion * self.removal_effect_attribution.weighted_impact))

        # self.removal_effect_attribution.to_csv('./self.removal_effect_attributionutes.csv', index=False)
        self.removal_effect_attribution = self.removal_effect_attribution.round(3)
        self.removal_effect_matrix = self.removal_effect_attribution[['Channel_name', 'removal_effect']]
        self.removal_effect_matrix['removal_conversion'] = np.int32(np.round(self.removal_effect_matrix.removal_effect * self.removal_effect_attribution.tot_conversion))
        # df_removal_effect.to_csv('./df_removal_effect.csv', index=False)

        self.removal_effect_attribution_final = self.removal_effect_attribution[['Channel_name', 'attribution_conversion']]
        self.removal_effect_attribution_final.channel_name = self.removal_effect_attribution_final.Channel_name.str.strip()
        # self.removal_effect_attribution_final.to_csv('./self.removal_effect_attributionutes_final.csv', index=False)

    def touch_conversion(self):
        '''
        This function will calculate the first and last touch conversion matrix
        :return:
        '''
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
        df_ft_and_mc_attribution['percentage_change'] = (df_ft_and_mc_attribution.attribution_conversion - df_ft_and_mc_attribution.first_touch_conversion) / df_ft_and_mc_attribution.attribution_conversion
        # df_ft_and_mc_attribution.to_csv('./first_touch and markov attributes.csv')

        df_lt_and_mc_attribution = pd.merge(df_lt, self.removal_effect_attribution_final, left_on='channel_name_lt',
                                            right_on='Channel_name')
        df_lt_and_mc_attribution.drop('Channel_name', axis='columns', inplace=True)
        df_lt_and_mc_attribution.rename(columns={'channel_name_lt': 'channel_name'}, inplace=True)
        df_lt_and_mc_attribution['percentage_change'] = (df_lt_and_mc_attribution.attribution_conversion - df_lt_and_mc_attribution.last_touch_conversion) / df_lt_and_mc_attribution.attribution_conversion
        # df_lt_and_mc_attribution.to_csv('./last_touch and markov attributes.csv')
        self.first_touch_conversion_attribution = df_ft_and_mc_attribution.round(3)
        self.last_touch_conversion_attribution = df_lt_and_mc_attribution.round(3)

    def transition_matrix(self):
        '''
        Calculating Transition matrix for given data
        '''
        path_df = self.conversion_paths.path.str.split(' > ', expand=True)
        path_df.columns = map(lambda x: 'ord_' + str(x), path_df.columns)
        res = []

        for i in range(path_df.shape[1] - 1):
            cache = path_df[list(map(lambda x: 'ord_' + str(x), np.arange(i, i + 2)))]
            cache.dropna(axis='rows', inplace=True)
            cache['n'] = self.conversion_paths.loc[cache.index, 'conversion']
            cache = cache.groupby(list(map(lambda x: 'ord_' + str(x), np.arange(i, i + 2)))).agg(
                {'n': 'sum'}).reset_index()
            cache.columns = ['channel_from', 'channel_to', 'n']
            res.append(cache)
        self.res_1 = res
        res = pd.concat(res, axis=0, ignore_index=True)
        self.res = res.groupby(['channel_from', 'channel_to']).agg({'n': 'sum'}).reset_index()

        ## Taking unique values of channel_list Need for removal effect
        self.channel_list = pd.unique(res.channel_from)
        self.channel_list = self.channel_list[self.channel_list != '(start)']

        trans_matrix = res.groupby(['channel_from', 'channel_to']).agg({'n': 'sum'}).reset_index()
        trans_matrix['perc'] = trans_matrix.groupby('channel_from')['n'].apply(lambda x: x / x.sum())
        ## Creating Dummy Dataframe
        self.dummy = pd.DataFrame.from_dict({
            'channel_from': ['(start)', '(conversion)', '(null)'],
            'channel_to': ['(start)', '(conversion)', '(null)'],
            'n': [0, 0, 0],
            'perc': [0, 1, 1]
        })

        self.trans_matrix = pd.concat([trans_matrix, self.dummy], axis=0, ignore_index=True)
        self.perc_matrix = self.trans_matrix.pivot_table(values='perc', index='channel_from',
                                                         columns='channel_to').fillna(0).round(3)
        self.trans_conversion_matrix = self.trans_matrix.pivot_table(values='n', index='channel_from',
                                                                     columns='channel_to').fillna(0)

