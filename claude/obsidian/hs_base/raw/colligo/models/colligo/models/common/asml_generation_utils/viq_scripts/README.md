# VIQ Scripts

This folder will have helpful scripts regularly used by the Video Inference Quality (VIQ) squad
All the scripts below assume that for each html there is an associated CSV file with the raw data (sensei paths, https paths, inputs, seeds etc.). This is a hard assumption. If your html was generated using colligo2html, you already have an associated csv

## HTML manipulation scripts

### Combining HTMLs
To combine HTMLs, use the `combine_csvs.py` script

```
python models/colligo/models/common/asml_generation_utils/viq_scripts/combine_csvs.py \
--input_csvs "<path_to_csv_1>,<path_to_csv_2>" \
--save_to "<save-to-location-to-store-combined-csv-and-html>" \
--caption_column "caption" \
--input_image_columns "image1,image2" \
--input_video_column "https_video0_ssr" \ 
--output_video_columns "<baseline, ablation>"
```

### Reencode HTMLs
To reencode (recompress) videos from a given HTML, use the `reencode_videos.py` script

```
python models/colligo/models/common/asml_generation_utils/viq_scripts/reencode_videos.py \
--input_csv "<path-to-csv>" \
--save_to "<save-to>" \
--crf <crf-value> \
--caption_column "caption" \
--image_columns "image0,image1" \
--video_columns "sensei_video0_ssr,sensei_video0_nossr"
```

### Standardize CSVs
Colligo2HTML expects the html to be of a very specific format. To convert a given csv (which contains a subset of columns from the standard format) to the standardized format, use `standardize_csv.py`

```
python models/colligo/models/common/asml_generation_utils/viq_scripts/standardize_csv.py \
--input_csv <path-to-nonstandard-csv> \
--output_csv <path-to-standardized-csv>
```

### CSV to HTML
Uploads videos from a CSV to S3 and creates an HTML out of it. Often used when you have the CSV but not the HTML file

```
python models/colligo/models/common/asml_generation_utils/viq_scripts/reencode_videos.py \
--input_csv "<path-to-csv>" \
--save_to "<save-to>" \
--crf <crf-value> \
--caption_column "caption" \
--image_columns "image0,image1" \
--video_columns "sensei_video0_ssr,sensei_video0_nossr"
```



