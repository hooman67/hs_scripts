# This is putting the T5 adaptor into the checkpoint since colligo loads it from there
import torch
import sys


# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-alse-03/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-24T10-32-39/lightning_logs/version_0/checkpoints/global_step_64000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_5/checkpoints/global_step_98000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_6/checkpoints/global_step_116000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_7/checkpoints/global_step_122000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_19/checkpoints/global_step_180000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_25/checkpoints/global_step_3040000_G.ckpt"
# input_path = "/sensei-fs/projects/firefly/clio/runai_training/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-03-28T14-34-13/lightning_logs/version_27/checkpoints/global_step_450000_G.ckpt"
# input_path = "/sensei-fs/users/hshariati/training/dmd_train_2/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50/lightning_logs/version_0/checkpoints/global_step_70000_G.ckpt"
# input_path = "/sensei-fs/users/hshariati/training/dmd_train_2/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50/lightning_logs/version_1/checkpoints/global_step_90000_G.ckpt"
# input_path = "/sensei-fs/users/hshariati/training/dmd_train_2/dmd_dmd-v12-prod3-27-84k-01/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-18T14-48-50/lightning_logs/version_2/checkpoints/global_step_130000_G.ckpt"
# input_path = "/sensei-fs/users/hshariati/del/global_step_30000_G.ckpt"
input_path = "/sensei-fs/users/hshariati/training/dmd_train_2/dmd_dmd-v12-prod3-27-84_hs_exp2/logs/clio3_dmd_guide8_mp_v4_2024_03_22-2024-04-25T11-23-27/lightning_logs/version_0/checkpoints/global_step_10000_G.ckpt"

unet = torch.load(input_path, map_location="cpu")
keys = list(unet.keys())
for key in keys:
    if key.startswith("G.eps_model.D"):
        unet[key.replace("G.eps_model.D", "eps_model")] = unet.pop(key)
unet.pop("g_optimizer")
output_path = input_path.replace(".ckpt", "_slimmed.ckpt")
# torch.save(unet, output_path)
print(output_path)


teacher_path = "/sensei-fs/projects/firefly/clio/training/logs/haravi/c3prod3-27-128px-2680k-aesnorm-mar3/c3prod3-27-128px-2680k-aesnorm-mar3-2024-01-12T21-41-30/lightning_logs/version_0/checkpoints/epoch=0-step=65000.ckpt"
teacher_unet = torch.load(teacher_path, map_location="cpu")

for key in teacher_unet["state_dict"].keys():
    if key in unet:
        teacher_unet["state_dict"][key] = unet[key]

output_path = input_path.replace(".ckpt", "combined_slimmed.ckpt")
torch.save(teacher_unet, output_path)
print(output_path)
