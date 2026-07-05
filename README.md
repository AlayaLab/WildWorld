<div align="center">

<h1 align="center">WildWorld: A Large-Scale Dataset for Dynamic World Modeling<br>with Actions and Explicit State toward Generative ARPG</h1>

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
> 
>
> Alaya Studio, Shanda AI Research Tokyo; Beijing Institute of Technology; Shanghai Innovation Institute

## 🔥Update

- [2026.07.06] WildWorld is now available on Hugging Face, starting with part 1. We are updating the README with more details.
- [2026.03.25] We have released our paper — discussions and feedback are warmly welcome!

## 🧠Introduction

![pipeline](./assets/framework-arxiv.png)

**TL;DR** We present **WildWorld**, a large-scale action-conditioned world modeling dataset with explicit state annotations, automatically collected from a photorealistic AAA action role-playing game. It features:

- 🎬 **108M+ frames** with **per-frame annotations**: character skeletons, actions & states (HP, animation, etc.), camera poses, and depth maps
- ⚔️ **450+ semantically meaningful actions** including movement, attacks, and skill casting
- 🐉 **Diverse content**: 29 monster species, 4 player characters, 4 weapon types, 5 distinct stages
- 🕒 **Long-horizon sequences**: clips spanning up to 30+ minutes of continuous gameplay
- 📝 **Hierarchical captions**: both action-level and sample-level natural language descriptions

## 📦TODO

- [ ] Release parts 1, 2, and 3 of the WildWorld dataset.
- [ ] Add detailed README and example code.
- [ ] Release code of WildBench benchmark.

## 📄License

See [LICENSE](./LICENSE).

## 📖Citation

If you find this project helpful, please consider citing:

```bibtex
@article{li2026wildworld,
  title={Wildworld: A large-scale dataset for dynamic world modeling with actions and explicit state toward generative arpg},
  author={Li, Zhen and Meng, Zian and Shi, Shuwei and Peng, Wenshuo and Wu, Yuwei and Zheng, Bo and Li, Chuanhao and Zhang, Kaipeng},
  journal={arXiv preprint arXiv:2603.23497},
  year={2026}
}
```
