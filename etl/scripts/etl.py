# -*- coding: utf-8 -*-

import os

import pandas as pd

from ddf_utils.str import to_concept_id

# configure file path
source = '../source/gapdata004 v7.xlsx'
out_dir = '../../'


def extract_datapoints(data, col, col_id):
    """extract datapoints from source.

    :parameters:
    col: target column
    col_id: the concept id of target column
    """
    dp = data[['Area', 'Year', col]].copy()
    dp.columns = ['area', 'year', col_id]
    dp['area'] = dp['area'].map(to_concept_id)

    return dp


if __name__ == '__main__':
    data001 = pd.read_excel(source, sheet_name='Data & meta data')

    # entities
    area = data001['Area'].unique()
    area_id = list(map(to_concept_id, area))
    ent = pd.DataFrame([], columns=['area', 'name'])
    ent['area'] = area_id
    ent['name'] = area

    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    ent.to_csv(path, index=False)

    # datapoints
    dps_list = ['Life expectancy at birth', 'Life expectancy, with interpolations']
    dps = dict([(x, to_concept_id(x)) for x in dps_list])

    for col, col_id in dps.items():
        dp = extract_datapoints(data001, col, col_id)
        path = os.path.join(out_dir, 'ddf--datapoints--{}--by--area--year.csv'.format(col_id))

        dp.dropna().sort_values(by=['area', 'year']).to_csv(path, index=False)

    # data001_dp_1 = data001[['Area', 'Year', 'Total Fertility Rate (TFR), also called Children per Woman']].copy()
    # data001_dp_2 = data001[['Area', 'Year', 'TFR interpolated']].copy()

    # data001_dp_1.columns = ['area', 'year', 'total_fertility_rate']
    # data001_dp_2.columns = ['area', 'year', 'total_fertility_rate_interpolated']

    # data001_dp_1['area'] = data001_dp_1['area'].map(to_concept_id)
    # data001_dp_2['area'] = data001_dp_2['area'].map(to_concept_id)

    # path1 = os.path.join(out_dir, 'ddf--datapoints--total_fertility_rate--by--area--year.csv')
    # path2 = os.path.join(out_dir, 'ddf--datapoints--total_fertility_rate_interpolated--by--area--year.csv')

    # data001_dp_1.dropna().sort_values(by=['area', 'year']).to_csv(path1, index=False)
    # data001_dp_2.dropna().sort_values(by=['area', 'year']).to_csv(path2, index=False)

    # concept
    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])
    cdf['name'] = [*dps_list,
                   'Area', 'Year', 'Name']
    cdf['concept_type'] = [*['measure'] * len(dps_list),
                           'entity_domain', 'time', 'string']
    cdf['concept'] = cdf.name.map(dps)
    cdf['concept'] = cdf['concept'].fillna(cdf['name'].map(to_concept_id))

    path = os.path.join(out_dir, 'ddf--concepts.csv')
    cdf.to_csv(path, index=False)

    print('Done.')
