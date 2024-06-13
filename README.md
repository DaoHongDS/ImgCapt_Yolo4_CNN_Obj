# ImgCapt_Yolo4_CNN_Obj
Image captioning models by combining Yolo4 CNN backbone (CSP Darknet) and its Object detection results.

# Ideas
Our model (called ImgCapt_Yolo4_CNN_Obj) is based on the **original model** on the paper [Image captioning model using attention and object features to mimic human image understanding](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-022-00571-w).
To solve the image captioning problems, this paper presents an attention-based, Encoder-Decoder deep architecture that makes use of convolutional features extracted from a CNN model pre-trained on ImageNet (Xception), together with object features extracted from the YOLOv4 model, pre-trained on MS COCO. 

\origin model Image

This paper also introduces a new positional encoding scheme for object features, the “Importance Factor”.

ImportanceFactor = ConfidenceRate × ObjectWidth × ObjectHeight

We made improvements by replacing CNN features (Xception) from the original model by Yolo4 CNN features (CSP Darknet53). So, we only use Yolo4 instead of both Xception and Yolo4 for the image captioning model. The CNN features is get from the end point of CSP Darknet53. At this point, we can optimize the size of features shape and the depth (the features are good enough and the size is not too big).

\image of CNN feature point

The details of processing is on the image belows

\image processing

# Results

The experiments is on COCO dataset (20M images)

Early, we expected to reduce the params number, therefore boots up the speed of model (and maybe with some trade off with the accuracy). And we almost have made it... The params number had fallen from 96M (original model) to 75M (only 3/4 remaining). But, surprisingly, the accuracy was increased. BLEU4 was increased 25% from 0.171 (original model) to 0.214 (our model). METEOR was increased 12% from 0.366 (original model) to 0.411 (our model).

We 
