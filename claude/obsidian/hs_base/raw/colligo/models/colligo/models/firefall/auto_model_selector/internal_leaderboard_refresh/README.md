# Auto Model Selection

Auto Model Selection Component recommends the best model for a given reqirement instead of users explicitly figuring out and picking a model. This reduces friction and boosts the odds of success. Current implementation is based on approach described in the following wiki page:
https://wiki.corp.adobe.com/display/GenAI/Automatic+model+selection

## Leaderboard Model Recommendation
The scoring are derived from internal evaluation results based on t2i_challenger_616 evaluation set -  https://evaluation-hub.adobe.io/leaderboard?evalSet=t2i_challenger_616

Currently, ELO score and leaderboard APIs are not exposed in the public documentation -https://evaluation-hub.adobe.io/docs. So these files are manually downloaded and translated into yaml files for internal use in config. 
Evaluation Hub also supports merging defined categories and combining them into a single category for faster lookup. This is used for T2I experiment categories. The categories defined in t_616 evaluation set are combined into categories defined by Amogh.
```
  photorealism:
  - architecture_exteriors
  - architecture_interior
  - complex_scenes
  - crowds
  - cultural
  - detailed_animals
  - detailed_human_portraits
  - dynamic_animals
  - dynamic_people
  - fashion_beauty_portraits
  - food_drink
  - holidays_celebrations
  - intricate_detail
  - multiple objects
  - nature_landscapes
  - people_object_interactions
  - people_object_interactions_rewr
  - product_shot
  - relfections_shadows_light
  - short_prompts
  - texture_material
  - vehicles
  digital_art:
  - animation_styles
  - fantasy_characters
  - fantasy_scenes
  - whimsical_imaginary
  traditional_art:
  - art_media
  graphic_design:
  - abstract_artistic_backgrounds
  - graphic_design
  - text_rendering
```

ToDo -
1. EVal Hub ELO score API access and automate manual download and translation into yaml files for internal use in config.
2. Support use case specific studies, evaluation sets and ELO boards derived from use case specific evaluation sets and studies.

## - Mapping from Model names defined in Internal Leaderboard to model_id-> model_version in 3P
# https://pluto-prod-od1-kulai-eval-strategy-0-8000.od1.colligo.dev/elo_leaderboard?eval_set=t2i_challenger_616

This is a temporary solution till eval hub exposes leaderboard data API, we need to manually create a mapping from model names defined in Internal Leaderboard to model_id-> model_version in 3P.

1. Download the leaderboard data from eval hub API - https://pluto-prod-od1-kulai-eval-strategy-0-8000.od1.colligo.dev/elo_leaderboard?eval_set=t2i_challenger_616  
   2. Download the total model scores data from eval hub API - https://pluto-prod-od1-kulai-eval-strategy-0-8000.od1.colligo.dev/elo_leaderboard?eval_set=t2i_challenger_616&category=total
   3. Download the category data from eval hub API - https://pluto-prod-od1-kulai-eval-strategy-0-8000.od1.colligo.dev/elo_leaderboard?eval_set=t2i_challenger_616&category=category_name
   # Aspect ratio etc if its required
   4. Combine the total model scores data and category data to get the final model scores data across all categories in single yaml file
2. Parse the leaderboard data to get model names and model_id-> model_version in 3P
3. Create a mapping from model names to model_id-> model_version in 3P
4. Save the mapping to a yaml file
(Of course - just ask cursor to do conversions from csv to yaml)
Example mapping:
```

```