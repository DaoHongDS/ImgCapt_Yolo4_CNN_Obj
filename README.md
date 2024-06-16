# ImgCapt_Yolo4_CNN_Obj
Image captioning models with features extracted from Yolo4 CNN backbone (CSP Darknet) and its Object detection results.

# Ideas
Our model (called ImgCapt_Yolo4_CNN_Obj) is based on the **original model** on the paper [Image captioning model using attention and object features to mimic human image understanding](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-022-00571-w).
To solve the image captioning problems, this paper presents an attention-based, Encoder-Decoder deep architecture that makes use of convolutional features extracted from a CNN model pre-trained on ImageNet (Xception), together with object features extracted from the YOLOv4 model, pre-trained on MS COCO. 

![image](https://drive.google.com/uc?export=view&id=1sLFwmG_VfTTDPK8Op4TblAau1pNwNFfc "Original model that Encoder uses convolutional features extracted from a CNN model pre-trained on ImageNet (Xception), together with object features extracted from the YOLOv4 model. LSTM is used for Decoder")

This paper also introduces a new positional encoding scheme for object features, the “Importance Factor”.

ImportanceFactor = ConfidenceRate × ObjectWidth × ObjectHeight

**We made improvements** by replacing CNN features (Xception) from the original model by Yolo4 CNN features (CSP Darknet53). So, we only use Yolo4 instead of both Xception and Yolo4 for the image captioning model. The CNN features is get from the end point of CSP Darknet53 (as figure below). At this point, we can optimize the size of features shape and the depth (the features are good enough and the size is not too big).

![image](https://drive.google.com/uc?export=view&id=1Bu6hOxMWKNTAEWigMR7_8ikX4zz_BSc2 "The CNN features is extracted from the end point of CSP Darknet53")

The details of processing is on the image belows:

![image](https://drive.google.com/uc?export=view&id=1HxsF5MUV2aCpgDyWx4hfMZ0RXTW_otjQ "Processing to extract combined features for image captioning model")

# Experiments

The experiments is on COCO dataset (train2014). We use 20k images (18k for training and 2k for testing (and calcalating BLEU, METEOR scores).

Models' architecture is Encoder-Decoder:
1. Encoder is combination of features (gets from a CNN models) and object detection results (get from Yolo4 output). We tried some CNN models like: Xception, Yolo4 backbone (CSP Darknet53), ViT, Swin...
2. Decoder is LSTM or Transformer.

For evaluations, we calculated BLEU and METEOR scores on the test dataset (2k COCO images). On the otherhand, we considered the params number of models and its speed of training and predicting.

# Results

At first, we expected to reduce the params number, therefore boots up the speed of model (and maybe with some trade off with the accuracy). And we almost have made it... The params number had fallen from 96M (original model) to 75M (only 3/4 remaining). But, surprisingly, the accuracy was increased. BLEU4 was increased 25% from 0.171 (original model) to 0.214 (our model). METEOR was increased 12% from 0.366 (original model) to 0.411 (our model).

Besides, we made some comparison when using features from SOTA CNN models like ViT (Visual Transformer), Swin Transformer (instead of using CNN backbone of Yolo4). The results point out the accuracy of our model is better than model uses ViT but it is not good as model uses Swin. About computation efficiency, the params number of our model is much less than models use ViT and Swin. Details is in the tables below.

![image](https://drive.google.com/uc?export=view&id=1Q8ZYaiJQeczcMzd4uQ8HGlIB1ABx7dRm "Comparison between models use LSTM for Decoder")

![image](https://drive.google.com/uc?export=view&id=1KEzgCWKWY9dqvb1QWB-QY-vf-OBWyDvp "Comparison between models use Transformer for Decoder")

In conclusion, experiments proved that our model is much better than original model about both accuracy and computation efficiency. It is also better than model that uses CNN features from ViT. When compare with model uses Swin, it is as good
as this SOTA methods in terms of the trade-off between accuracy and computational resources required for training and inference. I hope that our ImgCapt_Yolo4_CNN_Obj model is a good choice if you have limited resources, for examples in cases of no GPU or weak GPU.

# Source code

1. Clone the project
2. Extract file pycocotools.rar (library that supports the COCO dataset)
3. [Download](https://drive.google.com/file/d/1c1ddEkk4-EKT9mbyg0RGSIMVuB32zXHB/view?usp=sharing) and add file yolov4.weights to the project folder.
4. Add some subfolders to each model folder to store feature files, model files, checkpoints... as below:
```bash
├── 2_Swin_LSTM
│   ├── checkpoint
│   ├── model_swin_lstm
│   ├── Swin_npy
│   ├── Swin_LSTM_att.ipynb
├── 2_ViT_LSTM
│   ├── checkpoint
│   ├── model_trained_Vit_LSTM_att
│   ├── ViT_npy_preprocess
│   ├── ViT_LSTM_att.ipynb
├── 3_Yolo4_RNN
│   ├── checkpoint
│   ├── trained_model_Yolo_RNN_conv116
│   ├── Yolo4_conv116_npy_512_169
│   ├── Yolo4_conv116_npy_512_169.ipynb
├── 3_Yolo4_Xception_RNN
│   ├── checkpoint
│   ├── xception_npy
│   ├── trained_model_xception
│   ├── YoloCV2_Xception_LSTM.ipynb
├── 4_Swin_Trans
│   ├── model_swin_trans
│   ├── Swin_npy
│   ├── Swin_Trans.ipynb
├── 4_ViT_Trans
│   ├── model_ViT_Trans
│   ├── ViT_npy
│   ├── ViT_Trans.ipynb
├── 5_Yolo4_Trans
│   ├── model_Yolo4_Trans_conv116
│   ├── Yolo4_conv116_npy
│   ├── Yolo4_Trans_conv116.ipynb
├── 5_Yolo4_Xception_Trans
│   ├── model_Yolo4_Xception_Trans
│   ├── Yolo4_Xception_npy
│   ├── Yolo4_Xception_Trans.ipynb
```
6. Run ipynb files for each model's experiments.
