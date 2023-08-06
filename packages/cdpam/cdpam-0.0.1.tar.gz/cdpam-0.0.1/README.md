# Contrastive learning-based Deep Perceptual Audio Metric (CDPAM) [[Paper]]() [[Webpage]](https://percepaudio.cs.princeton.edu/Manocha20_CDPAM/)

**Contrastive Learning For Perceptual Audio Similarity**

[Pranay Manocha](https://www.cs.princeton.edu/~pmanocha/), [Zeyu Jin](https://research.adobe.com/person/zeyu-jin/), [Richard Zhang](http://richzhang.github.io/), [Adam Finkelstein](https://www.cs.princeton.edu/~af/)   
Arxiv 2020()

<img src='https://richzhang.github.io/index_files/audio_teaser.jpg' width=500>

This is a Pytorch implementation of our new and improved audio perceptual metric. It contains (0) minimal code to run our perceptual metric (CDPAM), (1) code to train the perceptual metric on our JND dataset, (2) example of using our loss function for MelGAN waveform synthesis and (3) another example of using our loss function on DEMUCS real time speech denoiser. All the models also have their pretrained models. All results are available in our paper [here]().

## Things to note:
1) At the moment, this algorithm requires using **16-bit PCM** audio files to perform correctly. You can use sox to convert your file.
2) The current pretrained models support **sr=22050Hz**. Please make sure to resample your files first before using the metric.
For ease, you can load your audio clip using librosa.load(filename,sr=22050) and then rescale to [-32768 to 32768] using np.round(audio_file.astype(np.float)*32768)
3) Tested on Nvidia GeForce RTX 2080 GPU with Cuda (>=9.2) and CuDNN (>=7.3.0). CPU mode should also work with minor changes.

## (0) Usage as a loss function

### Minimal basic usage as a distance metric

Running the command below takes two audio files as input and gives the perceptual distance between the files. It should return (approx)**distance = 0.1696**. Some GPU's are non-deterministic, and so the distance could vary in the lsb.

```
cd metric
python simple-metric-use.py --e0 ../sample_audio/ref.wav --e1 ../sample_audio/2.wav
```

For loading large number of files, batch processing is more efficient. Refer to at [metric/simple-metric-use.py](metric/simple-metric-use.py) for more information.

## (1) Training the metric
For training the metric, the current codebase uses sampling rate=16000Hz. You can change the sampling rate to work for your dataset and task. The current pretrained model works on sampling rate=22050Hz and on 16-bit PCM audio files.

### Download the dataset
Follow the instructions in ''dataset'' subfolder of this repo. You can download all dataset to reproduce the results of the paper. The files in the dataset are all sampled at 16000Hz.

### Use the contrastive-learning based pretrained model
After you download the dataset, you can also train our model. Simply run 
```
cd metric
python train-contrastive.py --output_folder <folder_name>
```
This trains the contrastive learning pretraining model and stores the model in 'summaries' subfolder under 'metric'.
### Train on JND Data
After you train the pretraining model, you can train our lossnetwork. Simply run 
```
cd metric
python train-JND.py --output_folder <folder_name> --file_load <path to trained contrastive model>
```
This trains the JND model and stores the model in 'summaries' subfolder under 'metric'. Make sure to read the arguments in the train-JND.py file. 

### Finetune on Triplet pairwise comparison dataset
After you train the loss-network using JND Data, you can train further finetune our loss-network. Simply run 
```
cd metric
python train-finetune.py --output_folder <folder_name> --load_checkpoint 1 --file_load <path of JND trained model>
```
This trains the finetuned triplet model and stores the model in 'summaries' subfolder under 'metric'. Make sure to read the arguments in the train-finetune.py file.

## (2) MelGAN waveform synthesis

### Single Speaker Model
We make use of our metric as a loss function for training a waveform synthesis model. We use the codebase from [here](https://github.com/descriptinc/melgan-neurips). We just augment CDPAM to their loss for training. For training, please download the LJ Dataset and place it in the right locations. Please follow all other training instructions on the original repo. 
#### Inference:
After you train model, you can use the same trained model to check performance. Simply run 
```
python scripts/generate_from_folder.py --save_path <path_to_save_files> --load_path <model_path> --folder <input files to synthesize>
```
For example: for using our pre-trained model, please replace the load_path to 
```pre-model/MELGAN_trained/single_speaker```

### Cross Speaker Model
For training, please download the VCTK Dataset and place it in the right location. Please follow all other training instructions on the original repo. 
#### Inference:
After you train model, you can use the same trained model to check performance. To check cross-speaker performance, we download the DAPS dataset and check cross-speaker performance for each unseen speaker in DAPS dataset. Download the DAPS dataset (resample it to 22050Hz to match training), and run the inference script.

Simply run 
```
python scripts/generate_from_folder.py --save_path <path_to_save_files> --load_path <model_path> --folder <input files to synthesize>
```
For example: for using our pre-trained model, please replace the load_path to 
```pre-model/MELGAN_trained/cross_speaker```

## (3) Real-time waveform denoising

### Training the SE Model
We make use of our metric as a loss function for training an SE model. We use the codebase from [here](https://github.com/facebookresearch/denoiser). We just augment CDPAM to their loss for training. For training, please download both datasets (VCTK and DNS following the repo above) and place them in the right locations.

### Inferring the SE Model
After you train a SE model, you can use the same trained model to denoise audio files. Simply run 
```
python -m denoiser.enhance --model_path <path to the model> --noisy_dir <path to the dir with the noisy files> --out_dir <path to store enhanced files>
```
For example: for using our pre-trained model, please replace the model_path to 
```pre-model/DEMUCS_trained/best.th```

### License
The source code is published under the [MIT license](https://choosealicense.com/licenses/mit/). See LICENSE for details. In general, you can use the code for any purpose with proper attribution. If you do something interesting with the code, we'll be happy to know. Feel free to contact us. The primary contact is Pranay Manocha.<br/>
