## Adversarial model
На всей [выборке](#выборка) {{adversarial_frac}}% самых свежих данных (по полю дата активации) размечаются как "1" остальные как "0" - это наше целевое событие ("{{col_target}}")  
[Кроссвалидация](#кроссвалидация) на всей [выборке](#выборка) - RepeatedStratifiedKFold by column group "{{col_target}}"  
Цель Adversarial validation попытаться предсказать, что событие было совершено в будущем.  
Чем выше качество модели -тем больше признаков изменили свое распределение во времени.  
Чем выше значимость фичи - тем больше смещение стабильности  
  
roc-auc {{score_max}} +- {{std}}  
roc-auc на каждом фолде {{scores_all}}  
  
Значимость признаков по shap:  
![adversarial_shap](data/03_primary/adversarial_fig.png)  
  
[adversarial_shap](data/03_primary/adversarial_shap.csv)   
  
{{shap_df}}  
  