# Auto Model Selection

Auto Model Selection Component recommends the best model for a given reqirement instead of users explicitly figuring out and picking a model. This reduces friction and boosts the odds of success. Current implementation is based on approach described in the following wiki page:
https://wiki.corp.adobe.com/display/GenAI/Automatic+model+selection

## Internal Leaderboard Model Recommendation
 
This approach uses Internal Leaderboard Model Recommendation to provide model recommendations based on model ranking and recommendations derived from internal evaluation results - https://evaluation-hub.adobe.io/leaderboard?evalSet=t2i_challenger_616

Currently its only enabled for text to image, image editing. In future it can be easily extedned for other categories. More details are in the README.md file.

1. Reads leaderboard data from internal evaluation hub
2. Leaderboard data is filtered to 3P Gateway supported models and cached in configurations
3. Leaderboard data is augmented with credit costs for the models, and inference times projected/calculated
4. Provides model recommendations based on -

- Workflow intent (edit, generate), categories determined from prompt and input request features
- Ranking methods selected (elo_only, robust_score, weighted_linear) for model ranking, including bias for own model
- Model rankings across these categories as determined from Leaderboard Data and model features like cost and latency
- Includes support including/falling back to own model

These model recommendations are used to automatically generate based on best model recommendations to the user.

## Cost and Latency Data

1. Avg. Latency numbers can be fetched from Splunk/New Relic - https://splunk-us.corp.adobe.com/en-US/app/app_neural_filters_platform/firefall_gen_3p

2. Avg. Credit cost numbers can be fetched from BKS - https://wiki.corp.adobe.com/display/GenAI/Cost+Calculations%3A+Image+Models