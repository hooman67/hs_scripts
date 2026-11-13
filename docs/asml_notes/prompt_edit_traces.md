# Goal
Trying to fix the motion of the dog and the leash that gets hullucinated 
by modifying the prompt


# With the student model

## original prompt
    "prompt": "A dog, tied securely with a red cloth, plays around and jumps excitedly, its tail wagging furiously.",

## rewritten prompt with no issues
"prompt": "The dog plays around and jumps excitedly, its tail wagging furiously.",
93504c62-ee42-4f48-abbf-77cd395729bf.mp4


## Original prompt
    "prompt": "A tennis player serves a tennis ball with a racket in his hand, his body coiled with energy and focus as he prepares to launch the ball into the air.",
    edd16f3d-760c-4207-a852-6e3ba3522642.mp4

## rewritten prompt with no issues
    "prompt": "A tennis player serves a tennis ball with a racket in his hand.",


# with teacher model
## Input:
https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP5_spg-bur5_spgEnhancedOn_spgBadModelOff_05-30-25_2/d3f9e145-275e-4826-ab9c-e4437b1985f1.jpg
A dog, with a red cloth tied around his neck, plays around and jumps excitedly, its tail wagging furiously.

Output:
2b25da1d-c3c3-4c68-8ce2-bd974d3ef541.mp4



## Input:
prompt : A dog, tied securely with a red cloth, plays around and jumps excitedly, its tail wagging furiously.

Output:
2b25da1d-c3c3-4c68-8ce2-bd974d3ef541.mp4
https://clio.corp.adobe.com/model_evaluation/sensei-fs/users/hshariati/del/clineto/html/v1p9_l2_new_student__1394k_i2v_fast_motion_l2Teacher_spg-scheduleAtP8OnlyFirst10_spg-bur5_spgEnhancedOff_spgBadModelOff_05-30-25_1/97e4f76b-a566-4b70-820b-7d0893c15da5.mp4



## Input:
    "prompt": " A dog, with a red cloth necktie tied around his neck, plays around and jumps excitedly, its tail wagging furiously.",
01d5d3a7-0706-4387-8b5f-9d7e543482a4.mp4


