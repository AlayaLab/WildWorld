<div align="center">

<h1 align="center">WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG</h1>

<p align="center">
  <a href="https://alaya-studio.github.io/wildworld-project/">
    <img src="https://img.shields.io/badge/Project-Page-2ea44f?style=flat&logo=googlechrome&logoColor=white" alt="Project Page">
  </a>
  <a href="https://arxiv.org/abs/2603.23497">
    <img src="https://img.shields.io/badge/arXiv-2603.23497-b31b1b?style=flat&logo=arxiv&logoColor=b31b1b" alt="arXiv">
  </a>
  <a href="https://github.com/AlayaLab/WildWorld">
    <img src="https://img.shields.io/badge/Code-Github-007ec6?style=flat&labelColor=555555&logo=github&logoColor=white" alt="GitHub Code">
  </a>
  <a href="https://huggingface.co/datasets/Lixsp11/WildWorld">
    <img src="https://img.shields.io/badge/Dataset-HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=yellow" alt="Hugging Face Dataset">
  </a>
  <a href="https://www.youtube.com/watch?v=9vcSg553r2g">
    <img src="https://img.shields.io/badge/YouTube-Video-FF0000?style=flat&logo=youtube&logoColor=red" alt="YouTube Video">
  </a>
</p>

</div>

This repo contains the dataset and benchmark code used in

> [**WildWorld: A Large-Scale Dataset for Dynamic World Modeling with Actions and Explicit State toward Generative ARPG**](https://arxiv.org/abs/2603.23497)
>
> Zhen Li, Zian Meng, Shuwei Shi, Wenshuo Peng, Yuwei Wu, Bo Zheng, Chuanhao Li, Kaipeng Zhang
>
> Alaya Studio, Shanda AI Research Tokyo; Beijing Institute of Technology; Shanghai Innovation Institute

## 🔥 Update

- [2026.07.06] WildWorld is now available on Hugging Face, starting with part 1 (574 hours)!
- [2026.03.25] We have released our paper — discussions and feedback are warmly welcome!

## 🧠 Introduction

![pipeline](./assets/framework-arxiv.png)

**TL;DR** We present **WildWorld**, a large-scale action-conditioned world modeling dataset with explicit state annotations, automatically collected from a photorealistic AAA action role-playing game. It features:

- 🎬 **108M+ frames** with **per-frame annotations**: character skeletons, actions & states (HP, animation, etc.), camera poses, and depth maps
- ⚔️ **450+ semantically meaningful actions** including movement, attacks, and skill casting
- 🐉 **Diverse content**: 29 monster species, 4 player characters, 4 weapon types, 5 distinct stages
- 🕒 **Long-horizon sequences**: clips spanning up to 30+ minutes of continuous gameplay
- 📝 **Hierarchical captions**: both action-level and sample-level natural language descriptions

## 🚀 Quick Start

The WildWorld dataset is hosted on [Hugging Face](https://huggingface.co/datasets/Lixsp11/WildWorld) and is planned to be released in three parts:

| Part   | Content                          | Duration    | `rgb.mp4` | `depth.mkv` | `state.csv` | `skeleton.npz` |
| ------ | -------------------------------- | ----------- | --------- | ----------- | ----------- | -------------- |
| part 1 | 1v1 | 574h | ~1.8 TB  | ~5.4 TB    | ~26 GB    | ~70 GB       |
| part 2 | TBD                              | -         | -       | -         | -         | -            |
| part 3 | TBD                              | -         | -       | -         | -         | -           |

### Directory Layout

One directory per sample, organized as:

```
data_part<x>/
├── <id>/
│   ├── rgb.mp4        # RGB frames at 720p@30 fps, no HUD/UI overlay
│   ├── depth.mkv      # 8-bit depth map encoded via lossless HEVC
│   ├── state.csv      # per-frame camera pose, player/monster state
│   └── skeleton.npz   # world-space 3-D joint positions per entity
└── skeleton_edges.json  # bone connectivity per skeleton type
```

## 📊 Data Format

### World State Records (`state.csv`)

State records fall into three categories: camera, player/NPC, and monster.

#### Camera

| Column       | Format             | Meaning                                                      |
| ------------ | ------------------ | ------------------------------------------------------------ |
| `camera.K`   | `(fx, fy, cx, cy)` | Camera intrinsics |
| `camera.pos` | `(x, y, z)`        | Camera position in world coordinates                         |
| `camera.rot` | `(x, y, z, w)`     | Camera-to-world rotation in the OpenGL camera frame |

#### Player/NPC

A frame may contain multiple players, indexed by `<index>`.

| Column                                       | Meaning                                                      |
| -------------------------------------------- | ------------------------------------------------------------ |
| `npc.count`                                  | Number of player characters           |
| `npc.tracking`                               | Which NPC the camera focuses on    |
| `npc.list.<index>.type_id`                         | NPC character type id         |
| `npc.list.<index>.member_id`                       | Party-member id (used by `npc.tracking`)       |
| `npc.list.<index>.weapon_id`                       | Weapon type id |
| `npc.list.<index>.pos`                             | `(x, y, z)` player position in world                         |
| `npc.list.<index>.rot`                             | `(x, y, z, w)` player world rotation       |
| `npc.list.<index>.motion_bank_id`                  | Animation bank id |
| `npc.list.<index>.motion_id`                       | Animation clip id |
| `npc.list.<index>.motion_frame`                    | Current playback frame within the clip |
| `npc.list.<index>.hp` / `max_hp` / `red_hp`                  | Current / maximum / recoverable health                                    |
| `npc.list.<index>.sp` / `max_sp`                   | Current / maximum stamina                                    |
| `npc.list.<index>.atk`                             | Total physical attack (gear + buffs)                         |
| `npc.list.<index>.wp_atk`                          | Weapon's own physical attack                                 |
| `npc.list.<index>.attr`                            | Total elemental attack value                                 |
| `npc.list.<index>.wp_attr`                         | Weapon's own elemental attack value                          |
| `npc.list.<index>.crit_rate`                       | Critical-hit rate, in `[-1, 1]` (negative = weakened hits)   |
| `npc.list.<index>.crit_atk_rate`                   | Critical damage multiplier (e.g. `1.25` = +25 %)             |
| `npc.list.<index>.def`                             | Physical defense (can change with temporary buffs)           |
| `npc.list.<index>.resist_{fire,water,ice,elec,dragon}` | Elemental resistances                                    |

#### Monster

A frame may contain multiple monsters, indexed by `<index>`.

| Column                          | Meaning                                                      |
| ------------------------------- | ------------------------------------------------------------ |
| `monster.count`                 | Number of monsters currently present           |
| `monster.list.<index>.type_id`        | Monster species type id; `nan` on frames where the monster is absent |
| `monster.list.<index>.pos`            | `(x, y, z)` monster position in world                        |
| `monster.list.<index>.rot`            | `(x, y, z, w)` monster world rotation (unit quaternion)      |
| `monster.list.<index>.motion_bank_id` | Animation bank id                                            |
| `monster.list.<index>.motion_id`      | Animation clip id                                            |
| `monster.list.<index>.motion_frame`   | Current playback frame within the clip                       |
| `monster.list.<index>.hp` / `max_hp`  | Current / maximum health                                     |
| `monster.list.<index>.cond`           | Active status conditions, `angry` / `stun` / `poison` / `sleep` / `paralyse` / `parry` / `tired` / `block_npc`, or `none` |

### Skeleton Joints (`skeleton.npz`)

Each sample's `skeleton.npz` holds one array per entity instance, keyed `<kind><index>_<type_id>`:

- **kind**: `m` = monster, `n` = player character, `w` = the player's weapon
- **index**: entity index number
- **type_id**: skeleton type id, i.e. monster species type id / player character type id / weapon type id (matches `type_id` / `weapon_id`)
- **value**: `(N, J, 3) float32`, world-space joint positions per frame

Example: `m1_21` (monster index 1, species 21).

#### Bone Connectivity (`skeleton_edges.json`)

The joint axis `J` has a **fixed, deterministic order per `type_id`**. Bone connectivity is shipped in `skeleton_edges.json`, one entry per skeleton type:

```json
{
  "em_21":  [[0, 3], [1, 5], ...],   // monsters:  key = "em_<type_id>"
  "npc":    [[0, 2], [0, 31], ...],  // player:    single shared skeleton
  "wp_4":   [[0, 1], ...],           // weapons:   key = "wp_<type_id>"
  ...
}
```

#### Visualization

The `scripts/` directory provides code for rendering skeletons into videos, as shown in the intro video:

```bash
python scripts/render_skeleton_video.py data_part<x>/<id> --edges skeleton_edges.json --overlay-rgb -o skeleton.mp4
```

## 📦 Checklist

- [x] Release part 1 of the WildWorld dataset.
- [ ] Release WildWorld dataset part 2 and part 3.
- [x] Add detailed README and example code.
- [ ] Release code of WildBench benchmark.

## 📄 License

See [LICENSE](./LICENSE).

## 📖 Citation

If you find this project helpful, please consider citing:

```bibtex
@article{li2026wildworld,
  title={Wildworld: A large-scale dataset for dynamic world modeling with actions and explicit state toward generative arpg},
  author={Li, Zhen and Meng, Zian and Shi, Shuwei and Peng, Wenshuo and Wu, Yuwei and Zheng, Bo and Li, Chuanhao and Zhang, Kaipeng},
  journal={arXiv preprint arXiv:2603.23497},
  year={2026}
}
```
