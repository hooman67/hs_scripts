# Inference Configurations

| Configuration | 86 iterations | 87 iterations | Drop Interval | Description                                                                                                                           |
| ------------- | ------------- | ------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 20230921_A    | 25            | 15            | null          | (DDIM, uniform) -> (Momentum DPM-Solver++, uniform, beta: 0.6). Content should be similar to trainer results. Simple guidance of 8.0. |
| 20230921_B    | 25            | 15            | null          | (Momentum SDE-DPMSOLVER++, logsnr, beta: 0.85) -> (Momentum DPM-Solver++, logsnr, beta: 0.6)                                          |
| 20230921_C    | 25            | 15            | null          | Same as 20230921_B, except some slight density added to induce variation.                                                             |
| 20230921_D    | 19            | 17            | null          | Simple DDIM.                                                                                                                          |
| 20230927_A    | 25            | 15            | (525, 0)      | Same as 20230921_A, except for drop interval.                                                                                         |
| 20230927_B    | 25            | 15            | (525, 0)      | Same as 20230921_B, except for drop interval.                                                                                         |
| 20230927_C    | 25            | 15            | (525, 0)      | Same as 20230921_C, except for drop interval. Second model momentum reduced to 0.6.                                                   |
| 20230927_D    | 20            | 10            | (525, 0)      | Base: 20230927_B. Changes: few iterations, guidance changes for more vibrant colors.                                                  |
| 20230927_E    | 20            | 10            | (525, 0)      | Base: 20230927_E. Changes: a little duller, but more high frequency features.                                                         |
| 20230927_F    | 20            | 10            | None          | (DDIM, uniform) -> (Momentum DPM-Solver++, uniform, beta: 0.6). Switches from 86 to 87 at 350 instead of 400.                         |
