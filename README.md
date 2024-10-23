# Passive Acoustic Monitoring Datasets


<div align="center">

<img class="img-fluid" src="assets/dalle_botticelli.png" alt="img-verification" width="250" height="250">

<em>“DALLE-2 prompt: Botticelli painting of a a frog working in an oil company "</em>

</div>

Passive Acoustic Monitoring Datasets (pam_datasets) is an open-source Python package dedicated to preprocessing, transformation, verification, experimental protocols, and curation of passive acoustic monitoring recordings for training machine learning algorithms. This package was designed to (1) check the integrity and properties of the data collected in the field, (2) filter, preprocess, transform, and curate the data, and (3) split the dataset given some experimental protocol for training and test. This workflow opens the possibility to fastly scan large audio datasets and use good practices to improve powerful machine learning techniques.


## Example using Anuraset:


## Installation instruction and reproduction of baseline results

1. Install [Conda](http://conda.io/)

2. Clone this repository

```bash
git clone https://github.com/soundclim/anuraset/
```

3. Create an environment and install requirements

```bash
cd anuraset
conda create -n anuraset_env python=3.8 -y
conda activate anuraset_env
conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia
pip install -r requirements.txt
```

> **Notes**
> * The installation of dependencies where tested on Azure. If you want to run locally, you might have to change the way you install PyTorch. Check the [PyTorch official webpage](https://pytorch.org/get-started/locally/) for installation instruction on specific platforms.
> * For **macOS** you might need to install [chardet: The Universal Character Encoding Detector](https://pypi.org/project/chardet/) with pip.


4. Download the [dataset](https://github.com/soundclim/anuraset). The **Anuraset** is a labeled collection of 93k samples of 3-second-long passive acoustic monitoring recordings organized into 42 neotropical anurans species suitable for multi-label call classification. 

5. Follow the example notebooks

## TODO
- [x] Multi-label setting (AnuraSet-4)
- [ ] Mutli-class setting 
- [ ] Binary
- [ ] EDA raw
- [ ] EDA dataset
- [ ] Visualization
- [ ] Autocorrelation
- [ ] Split

## Similar projects

- http://opensoundscape.org/en/latest/
- https://github.com/shyamblast/Koogu

## Acknowledgments
The authors acknowledge financial support from the intergovernmental Group on Earth Observations (GEO) and Microsoft, under the GEO-Microsoft Planetary Computer Programme (October 2021).

## Contact

