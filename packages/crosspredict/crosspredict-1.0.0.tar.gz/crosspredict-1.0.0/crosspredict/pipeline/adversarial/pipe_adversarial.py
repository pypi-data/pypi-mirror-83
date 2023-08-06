

from kedro.pipeline import Pipeline, node
from crosspredict.pipeline.nodes import model_fit, adversarial_make_target, \
    make_report, merge_json


def adv_pipeline(**kwargs):
    '''
    :param train: pd.DataFrame Input DataFrame
    :param template_adversarial: text with Report template
    :param params: config with `adversarial` and `adversarial_params_default` top-level keys
    :return report_adversarial_json: json.dumps with calculated metrics for report
    :return report_adversarial: text with adversarial report
    :return adversarial_fig: matplotlib.pyplot.figure with feature importance. Should be saved in (data/03_primary/adversarial_fig.png)
    :return adversarial_shap: pd.DataFrame with feature importance. Should be saved in (data/03_primary/adversarial_shap.csv)
    '''
    return Pipeline([
        node(
            func=adversarial_make_target,
            inputs=["train", "params:adversarial"],
            outputs=["train_adv", "report_1"]
        ),
        node(
            func=model_fit,
            inputs=["train_adv", "params:adversarial", "params:adversarial_params_default"],
            outputs=["adversarial_fig", "adversarial_shap", "report_2", "tmp1"],
            name="modelling_adversarial",
        ),
        node(merge_json,
             dict(report_1 = "report_1",
                report_2 = "report_2"),
             "report_adversarial_json"
        ),
        node(
            func=make_report,
            inputs=["template_adversarial", "report_adversarial_json"],
            outputs="report_adversarial"
        )
        ]
    )
