import datetime
import pandas as pd
import numpy as np
from crosspredict.iterator import Iterator
from crosspredict.crossval import CrossLightgbmModel
from crosspredict.report_binary import ReportBinary
from crosspredict.report_binary import CurveFabric
import matplotlib.pyplot as plt
import shap

from sklearn.metrics import roc_auc_score
from jinja2 import Template
import yaml
import json
import lightgbm as lgb
from hyperopt import fmin, tpe, Trials, space_eval
import logging
import yaml
import logging
import json
from sklearn.model_selection import train_test_split

def sci_init(df, params):
    '''
    :param df:
    :param params:
    :return:
    '''
    min_date = params['min_date']
    max_date = params['max_date']
    oot_split = params['oot_split']
    oos_frac = params['oos_frac']
    col_target = params['col_target']
    col_dt = params['col_dt']
    col_dt_mon = params['col_dt_mon']
    col_client = params['col_client']

    df[col_dt] = pd.to_datetime(df[col_dt])
    df[col_dt_mon] = df[col_dt].map(lambda x: x.replace(day=1))
    mask1 = df[col_dt]>=min_date
    mask2 = df[col_dt]<max_date
    df = df[mask1 & mask2]
    #
    df[col_client + '_ind'] = df[col_client]
    df[col_dt + '_ind'] = df[col_dt]

    oot = df[df['labling'] == 'OOT'].reset_index(drop=True)
    oos = df[df['labling'] == 'OOS'].reset_index(drop=True)
    train = df[df['labling'] == 'train'].reset_index(drop=True)
    rest = df[~df['labling'].isin(['train','OOS','OOT'])].reset_index(drop=True)

    train = train.set_index([col_client + '_ind', col_dt + '_ind'])
    oos = oos.set_index([col_client + '_ind', col_dt + '_ind'])
    oot = oot.set_index([col_client + '_ind', col_dt + '_ind'])
    return [train, oos, oot, rest]

def adversarial_make_target(train, params):
    col_target = params['col_target']
    adversarial_frac = params['adversarial_frac']
    target_ind = train.sort_values('act_date')[-int(train.shape[0] * adversarial_frac):].index
    train[col_target] = train.index.isin(target_ind).astype(int)

    report = {}
    report['adversarial_frac'] = adversarial_frac
    report['col_target'] = col_target
    report = json.dumps(report, indent=4, sort_keys=True)
    return [train, report]

def model_fit(df,params_model,lgb_params):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    n_repeats = params_model['n_repeats']
    n_splits = params_model['n_splits']
    num_boost = params_model['num_boost']
    col_target = params_model['col_target']
    col_client = params_model['col_client']
    cv_byclient = params_model['cv_byclient']
    cols_exclude = params_model['cols_exclude']
    feature_name = [col for col in df.columns if col not in cols_exclude]

    if type(lgb_params)==str:
        lgb_params = json.loads(lgb_params)["params"]
    params = lgb_params

    iter_df = Iterator(n_repeats=n_repeats,
                       n_splits=n_splits,
                       random_state=0,
                       col_target=col_target,
                       cv_byclient=cv_byclient,
                       col_client=col_client)

    model_class = CrossLightgbmModel(iterator=iter_df,
                                     feature_name=feature_name,
                                     params=params,
                                     num_boost_round=num_boost,
                                     early_stopping_rounds=50,
                                     valid=True,
                                     random_state=0,
                                     col_target=col_target,
                                     )

    result = model_class.fit(df)
    log.info(result)
    fig, shap_df = model_class.shap(df)

    report = {}
    report['col_target'] = col_target
    report['score_max'] = format(float(result['score_max']), '.5f')
    report['scores_all'] = [format(float(i), '.5f') for i in result['scores_all']]
    report['frac'] = [format(float(i), '.5f') for i in result['scores_all']]
    report['loss'] = format(float(result['loss']), '.5f')
    report['std'] = format(float(result['std']), '.5f')
    report['shap_df'] = shap_df[:15].to_markdown()
    report['feature_len'] = str(len(feature_name))
    report['num_boost'] = str(result['num_boost'])
    report = json.dumps(report, indent=4, sort_keys=True)
    plt.tight_layout(True)
    return [fig, shap_df, report, model_class]


def merge_json(**dict_inp):
    result = {}
    for key, value in dict_inp.items():
        value = json.loads(value)
        result.update(value)
    result = json.dumps(result, indent=4, sort_keys=True)
    return result


def make_report(template, report):
    report = json.loads(report)
    t = Template(''.join(template))
    readme_rendered = t.render(**report)
    return readme_rendered


def exclude_features(df, shap_df, params):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    if type(params)==str:
        params = json.loads(params)
    feature_selection = int(params['feature_selection'])

    log.info(f'df shape {df.shape}')
    cols_exclude = shap_df['index'][feature_selection:].values.tolist()
    log.info(f'total features {shap_df.shape[0]}')
    log.info(f'exclude columns {len(cols_exclude)}')
    feature_name = [col for col in df.columns if col not in cols_exclude]
    log.info(f'filtered columns {len(feature_name)}')
    df = df[feature_name]
    log.info(f'df filtered shape {df.shape}')
    return df

def forward_selection(df, params_model):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    n_repeats = params_model['n_repeats']
    n_splits = params_model['n_splits']
    hyperopt_trials = params_model['hyperopt_trials']
    num_boost = params_model['num_boost']
    col_target = params_model['col_target']
    col_client = params_model['col_client']
    cv_byclient = params_model['cv_byclient']
    cols_exclude = params_model['cols_exclude']

    feature_name = [col for col in df.columns if col not in cols_exclude]
    categorical_feature = []

    iter_df = Iterator(n_repeats=n_repeats,
                       n_splits=n_splits,
                       random_state=0,
                       col_target=col_target,
                       cv_byclient=cv_byclient,
                       col_client=col_client)




    important_features = feature_name
    important_cat_features = []

    scores = []
    selected_features = []
    selected_cat_features = []

    print("Starting force feature selection ...")
    for _ in range(len(important_features)):

        top_feature = None
        top_score = 0

        for i, f in enumerate(set(important_features) - set(selected_features)):

            current_features = selected_features + [f]
            log.info(f'inner iteration {i}: {f}')
            current_cat_features = selected_cat_features
            if f in categorical_feature:
                current_cat_features = selected_cat_features + [f]

            model_class = CrossLightgbmModel(iterator=iter_df,
                                             feature_name=current_features,
                                             params={
                                                 'objective': 'binary',
                                                 'metric': 'auc',
                                                 'bagging_seed': 0,
                                                 'data_random_seed': 0,
                                                 'drop_seed': 0,
                                                 'feature_fraction_seed': 0,
                                                 'verbose': -1
                                             },
                                             num_boost_round=100,
                                             early_stopping_rounds=100,
                                             valid=True,
                                             random_state=0,
                                             col_target=col_target,
                                             )


            result = model_class.fit(df)
            score = result['score_max']
            if score > top_score:
                print(f'new top score: {score}, top_feature: {f}')
                top_score = score
                top_feature = f

        log.info("{} features left to select ...".format(len(set(important_features) - set(selected_features)) - 1))
        scores.append(top_score)
        selected_features.append(top_feature)
        if top_feature in categorical_feature:
            selected_cat_features.append(top_feature)
        #     display.clear_output(wait=True)

        log.info(f'feature added: {top_feature}')
        log.info(f'top score: {top_score}')
        log.info(f'selected features: {selected_features}')


    log.info(scores)
    log.info(selected_features)
    log.info(selected_cat_features)

    plt.plot(scores)
    plt.show()

    scores_df = pd.DataFrame(scores, columns=["score"])
    selected_features_df = pd.DataFrame(selected_features, columns=["feature_name"])

    X = pd.concat([selected_features_df, scores_df], axis=1)
    X['score2'] = X['score'].shift(1)
    X['score_diff'] = X['score'] - X['score2']
    X['score_diff_flag'] = X['score_diff'] < 0.00005
    top_features = X[X['score_diff_flag']].index[0]

    scores_df = pd.DataFrame(zip(selected_features, scores), columns=["index","score"])
    top_features = json.dumps({"feature_selection": str(top_features)}, indent=4, sort_keys=True)
    return [scores_df, top_features]



def hyperopt_fit(df,params_model):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)

    n_repeats = params_model['n_repeats']
    n_splits = params_model['n_splits']
    hyperopt_trials = params_model['hyperopt_trials']
    num_boost = params_model['num_boost']
    col_target = params_model['col_target']
    col_client = params_model['col_client']
    cv_byclient = params_model['cv_byclient']
    cols_exclude = params_model['cols_exclude']

    feature_name = [col for col in df.columns if col not in cols_exclude]

    space = CrossLightgbmModel(iterator=None,
                               feature_name=feature_name,
                               params=None,
                               num_boost_round=num_boost,
                               early_stopping_rounds=50,
                               valid=True,
                               random_state=0,
                               col_target=col_target).get_hyperopt_space()

    iter_df = Iterator(n_repeats=n_repeats,
                       n_splits=n_splits,
                       random_state=0,
                       col_target=col_target,
                       cv_byclient=cv_byclient,
                       col_client=col_client)

    def score(params):
        params['njobs'] = 8
        cv_score = CrossLightgbmModel(iterator=iter_df,
                                      feature_name=feature_name,
                                      params=params,
                                      num_boost_round=9999,
                                      early_stopping_rounds=50,
                                      valid=True,
                                      random_state=0,
                                      col_target=col_target)
        return cv_score.fit(df=df)

    trials = Trials()
    best = fmin(fn=score,
                space=space,
                algo=tpe.suggest,
                trials=trials,
                max_evals=hyperopt_trials
                )

    results = {"params": space_eval(space, best)}
    results["hyperopt_trials"] = hyperopt_trials

    results = json.dumps(results, indent=4, sort_keys=True)
    return results

def model_single_fit(df, params_model, results, params_hyperopt):
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(__name__)
    results = json.loads(results)
    num_boost = int(results['num_boost'])

    col_target = params_model['col_target']
    cols_cat = params_model['cols_cat']

    cols_exclude = params_model['cols_exclude']
    feature_name = [col for col in df.columns if col not in cols_exclude]

    if type(params_hyperopt)==str:
        params_hyperopt = json.loads(params_hyperopt)["params"]
    params = params_hyperopt

    dataset = lgb.Dataset(
        data=df[feature_name],
        label=df[col_target],
        categorical_feature=cols_cat)
    log.info(params)
    model = lgb.train(params,
                      dataset,
                      num_boost_round=num_boost)

    model_str = model.model_to_string()

    return model_str


def model_predict_class(df_train, df_oos, df_oot, df_rest, model_class):

    df_train['predict_class'] = model_class.transform(df_train)
    df_oos['predict_class'] = model_class.predict(df_oos)
    df_oot['predict_class'] = model_class.predict(df_oot)
    df_rest['predict_class'] = model_class.predict(df_rest)

    return [df_train, df_oos, df_oot, df_rest]


def model_predict(df_oos, df_oot, df_rest, model):
    model = lgb.Booster(model_str = model)
    df_oos['predict_final'] = model.predict(df_oos[model.feature_name()])
    df_oot['predict_final'] = model.predict(df_oot[model.feature_name()])
    df_rest['predict_final'] = model.predict(df_rest[model.feature_name()])

    df = pd.concat([df_oos, df_oot, df_rest])
    return [df_oos, df_oot, df_rest]


def merge(df_train, df_oos, df_oot, df_rest):
    df_train['mask'] = 'train'
    df_oos['mask'] = 'oos'
    df_oot['mask'] = 'oot'
    df_rest['mask'] = 'rest'
    return pd.concat([df_train, df_oos, df_oot, df_rest])


def report(df_data, params):
    col_generation_deals = params['col_generation_deals']
    cols_score = params['cols_score']
    cols_target = params['cols_target']

    a = ReportBinary(col_generation_deals=col_generation_deals,
                     cols_score=cols_score,
                     cols_target=cols_target)
    a.fit(df_data)
    b = a.plot_report(report_shape=(4, 2),
                      report={'roc-auc': {'loc': (0, 0)},
                              'precision-recall': {'loc': (0, 1)},
                              'mean-prob': [{'loc': (1, 0)}, {'loc': (1, 1)}],
                              'gen-gini': [{'loc': (2, 0), 'colspan': 2}],
                              'distribution': [{'loc': (3, 0)}, {'loc': (3, 1)}],
                              })
    fig = b.fig
    plt.tight_layout(True)
    return fig

def report_shap(df_data, model):
    fig = plt.figure()
    log = logging.getLogger(__name__)

    shap_df_fin = pd.DataFrame(columns=['feature'])
    model = lgb.Booster(model_str=model)
    model.params['objective']='binary'
    # Подготовка данных в нужном формате
    explainer = shap.TreeExplainer(model)
    df_sample = df_data[model.feature_name()].sample(
        n=2000, random_state=0, replace=True).astype(float)
    shap_values = explainer.shap_values(df_sample)[1]
    shap_df = pd.DataFrame(zip(model.feature_name(), np.mean(
        np.abs(shap_values), axis=0)), columns=['feature', 'shap_'])
    shap_df_fin = pd.merge(shap_df_fin, shap_df, how='outer', on='feature')

    shap.summary_plot(shap_values, df_sample, show=False, )
    plt.tight_layout(True)
    return [fig, shap_df_fin]

def report_count(df_data, params, params_prefix):
    log = logging.getLogger(__name__)
    prefix = params_prefix['name']
    col_dt = params['col_dt']
    col_target = params['col_target']
    first_dt = df_data[col_dt].min().strftime('%Y-%m-%d')
    last_dt = df_data[col_dt].max().strftime('%Y-%m-%d')
    count = str(df_data.shape[0])
    sum_target = str(df_data[col_target].sum())
    mean_target = format(df_data[col_target].mean() * 100, '.2f')
    report = {
        prefix+"first_dt": first_dt,
        prefix+"last_dt": last_dt,
        prefix+"count": count,
        prefix+"sum_target": sum_target,
        prefix+"mean_target": mean_target,
    }
    report = json.dumps(report, indent=4, sort_keys=True)
    return report

def report_mean_target_by_mon(df_data, params):
    col_dt_mon = params['col_dt_mon']
    col_target = params['col_target']

    df_grouped_render = df_data.groupby(col_dt_mon)[col_target].agg(['count', 'sum'])
    df_grouped_render['percentage'] = df_grouped_render['sum'] / df_grouped_render['count']


    df_grouped_render['percentage'] = df_grouped_render['percentage'].map(
        lambda x: f'{x * 100:,.2f}%'.replace(",", " "))
    df_grouped_render['sum'] = df_grouped_render['sum'].map(lambda x: f'{x:,}'.replace(",", " "))
    df_grouped_render['count'] = df_grouped_render['count'].map(lambda x: f'{x:,}'.replace(",", " "))
    df_grouped_render.index = df_grouped_render.index.map(lambda x: x.strftime('%Y-%m-%d'))
    report = {'mean_target_by_mon': df_grouped_render.to_markdown()}
    report = json.dumps(report, indent=4, sort_keys=True)
    return report

def report_merge_md(**dict_inp):
    result = ''
    for key, value in dict_inp.items():
        result += value
    return result

def report_onefactor(df, df_shap, params):

    n_groups = 5
    col_dt_mon = params['col_dt_mon']
    col_target = params['col_target']

    report_text = ''

    for row in df_shap.iterrows():
        col_name = row[1]['index']
        text = f'Feature name = {row[1]["index"]}  \n'
        text += f'Shap Value = {row[1]["mean"]}  \n'
        text += f'Shap STD = {row[1]["std"]}  \n'
        text += f'![onefactor](data/04_feature/{col_name}.png)  \n'
        report_text = report_text + text
        print(text)

        splits = np.arange(0, n_groups + 1) / (n_groups)
        if df[col_name].nunique() > n_groups:
            a = pd.qcut(df[col_name], splits, duplicates='drop')
        else:
            a = df[col_name].astype('category')
        a.cat.add_categories(['missing'], inplace=True)
        a = a.fillna('missing')

        fig, _ = plt.subplots()
        #     gcf()
        fig.set_size_inches(1 * 8, 2 * 5)
        plt.subplots_adjust(left=0.125,
                            right=0.9,
                            bottom=0.1,
                            top=0.95,
                            wspace=0.1,
                            hspace=0.3
                            )

        b = df.groupby([col_dt_mon, a]).size().unstack(level=1)
        b = b.div(b.sum(axis=1), axis=0)
        c = df.groupby([col_dt_mon]).size()

        ax1 = plt.subplot2grid((2, 1), loc=(0, 0))
        ax2 = ax1.twinx()
        for col in b.columns:
            CurveFabric._draw_series_to_line_plot(_, b[col], ax=ax2, label=col, legend=True)
        CurveFabric._draw_series_to_bar_plot(_, c, ax=ax1)
        ax2.set_ylabel('Count, %')

        b = df.groupby([col_dt_mon, a])[col_target].mean().unstack(level=1)
        c = df.groupby([col_dt_mon]).size()

        ax3 = plt.subplot2grid((2, 1), loc=(1, 0))
        ax4 = ax3.twinx()
        for col in b.columns:
            CurveFabric._draw_series_to_line_plot(_, b[col], ax=ax4, label=col, legend=True)
        CurveFabric._draw_series_to_bar_plot(_, c, ax=ax3)
        ax4.set_ylabel('Mean Target')

        ax2.set_title(col_name, fontsize=14, fontweight='bold')
        plt.tight_layout(True)
        fig.savefig(f'data/04_feature/{col_name}.png')

    return report_text

def report_segments(df, params_sci):
    col_target = params_sci['col_target']
    # test masks
    mask_OOT = (df['labling'] == 'OOT')
    mask_sample = df['labling'] == 'sample'
    mask_sprut = (df['segment'] == "S") & mask_OOT
    mask_cb = (df['segment'] == "CB") & mask_OOT
    mask_ev_OOS = (df['segment'] == "EV") & mask_sample
    mask_good_OOS = (df['segment'] == 'G') & mask_sample

    def GiniMeanTargCalc(df):
        return [2 * roc_auc_score(df[col_target], df['predict_final']) - 1, df[col_target].mean(), df.shape[0]]

    GiniMeanTg = [['S'] + GiniMeanTargCalc(df[mask_sprut])] + \
                 [['SCB'] + GiniMeanTargCalc(df[mask_cb | mask_sprut])] + \
                 [['SCBEV'] + GiniMeanTargCalc(df[mask_cb | mask_sprut | mask_ev_OOS])] + \
                 [['SCBG'] + GiniMeanTargCalc(df[mask_cb | mask_sprut | mask_good_OOS])]

    GiniMeanTg_pandas = pd.DataFrame(GiniMeanTg, columns=['segment', 'Gini', 'meanTrg', 'count']).set_index('segment').T

    GiniMeanTg_pandas = GiniMeanTg_pandas.T
    for col in ['Gini', 'meanTrg']:
        GiniMeanTg_pandas[col] = GiniMeanTg_pandas[col].map(lambda x: f'{x*100:,.2f}%'.replace(","," "))
    GiniMeanTg_pandas['count'] = GiniMeanTg_pandas['count'].map(lambda x: f'{x:,}'.replace(","," "))

    return GiniMeanTg_pandas.to_markdown()