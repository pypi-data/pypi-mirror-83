from .data import COLORS #line:1
from .yolact import Yolact #line:2
from .utils .augmentations import FastBaseTransform #line:3
from .utils import timer #line:4
from .utils .functions import SavePath #line:5
from .layers .output_utils import postprocess ,undo_image_transformation #line:6
from .data import cfg ,set_cfg #line:8
import numpy as np #line:10
import torch #line:11
import argparse #line:13
import random #line:14
from collections import defaultdict #line:15
from PIL import Image #line:16
import matplotlib .pyplot as plt #line:17
import cv2 #line:18
w_aim ,h_aim =256 ,512 #line:22
def show (O0000000000OO00OO ,size =8 ):#line:26
    plt .figure (figsize =(size ,size ))#line:27
    if np .max (O0000000000OO00OO )<=1 :#line:28
        plt .imshow (O0000000000OO00OO ,vmin =0 ,vmax =1 )#line:29
    else :#line:30
        plt .imshow (O0000000000OO00OO ,vmin =0 ,vmax =255 )#line:31
    plt .gray ()#line:32
    plt .show ()#line:33
    plt .close ()#line:34
    print ()#line:35
def str2bool (OO0OO00OO0OOO0OO0 ):#line:37
    if OO0OO00OO0OOO0OO0 .lower ()in ('yes','true','t','y','1'):#line:38
        return True #line:39
    elif OO0OO00OO0OOO0OO0 .lower ()in ('no','false','f','n','0'):#line:40
        return False #line:41
    else :#line:42
        raise argparse .ArgumentTypeError ('Boolean value expected.')#line:43
def parse_args (argv =None ,inpass =None ,outpass =None ,model_path =None ):#line:45
    OO000O000O0OO0OOO =argparse .ArgumentParser (description ='YOLACT COCO Evaluation')#line:47
    OO000O000O0OO0OOO .add_argument ('--trained_model',default =model_path ,type =str ,help ='Trained state_dict file path to open. If "interrupt", this will open the interrupt file.')#line:50
    OO000O000O0OO0OOO .add_argument ('--top_k',default =10 ,type =int ,help ='Further restrict the number of predictions to parse')#line:52
    OO000O000O0OO0OOO .add_argument ('--cuda',default =True ,type =str2bool ,help ='Use cuda to evaulate model')#line:54
    OO000O000O0OO0OOO .add_argument ('--fast_nms',default =True ,type =str2bool ,help ='Whether to use a faster, but not entirely correct version of NMS.')#line:56
    OO000O000O0OO0OOO .add_argument ('--display_masks',default =True ,type =str2bool ,help ='Whether or not to display masks over bounding boxes')#line:58
    OO000O000O0OO0OOO .add_argument ('--display_bboxes',default =True ,type =str2bool ,help ='Whether or not to display bboxes around masks')#line:60
    OO000O000O0OO0OOO .add_argument ('--display_text',default =True ,type =str2bool ,help ='Whether or not to display text (class [score])')#line:62
    OO000O000O0OO0OOO .add_argument ('--display_scores',default =True ,type =str2bool ,help ='Whether or not to display scores in addition to classes')#line:64
    OO000O000O0OO0OOO .add_argument ('--display',dest ='display',action ='store_true',help ='Display qualitative results instead of quantitative ones.')#line:66
    OO000O000O0OO0OOO .add_argument ('--shuffle',dest ='shuffle',action ='store_true',help ='Shuffles the images when displaying them. Doesn\'t have much of an effect when display is off though.')#line:68
    OO000O000O0OO0OOO .add_argument ('--ap_data_file',default ='results/ap_data.pkl',type =str ,help ='In quantitative mode, the file to save detections before calculating mAP.')#line:70
    OO000O000O0OO0OOO .add_argument ('--resume',dest ='resume',action ='store_true',help ='If display not set, this resumes mAP calculations from the ap_data_file.')#line:72
    OO000O000O0OO0OOO .add_argument ('--max_images',default =-1 ,type =int ,help ='The maximum number of images from the dataset to consider. Use -1 for all.')#line:74
    OO000O000O0OO0OOO .add_argument ('--output_coco_json',dest ='output_coco_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this just dumps detections into the coco json file.')#line:76
    OO000O000O0OO0OOO .add_argument ('--bbox_det_file',default ='results/bbox_detections.json',type =str ,help ='The output file for coco bbox results if --coco_results is set.')#line:78
    OO000O000O0OO0OOO .add_argument ('--mask_det_file',default ='results/mask_detections.json',type =str ,help ='The output file for coco mask results if --coco_results is set.')#line:80
    OO000O000O0OO0OOO .add_argument ('--config',default =None ,help ='The config object to use.')#line:82
    OO000O000O0OO0OOO .add_argument ('--output_web_json',dest ='output_web_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this dumps detections for usage with the detections viewer web thingy.')#line:84
    OO000O000O0OO0OOO .add_argument ('--web_det_path',default ='web/dets/',type =str ,help ='If output_web_json is set, this is the path to dump detections into.')#line:86
    OO000O000O0OO0OOO .add_argument ('--no_bar',dest ='no_bar',action ='store_true',help ='Do not output the status bar. This is useful for when piping to a file.')#line:88
    OO000O000O0OO0OOO .add_argument ('--display_lincomb',default =False ,type =str2bool ,help ='If the config uses lincomb masks, output a visualization of how those masks are created.')#line:90
    OO000O000O0OO0OOO .add_argument ('--benchmark',default =False ,dest ='benchmark',action ='store_true',help ='Equivalent to running display mode but without displaying an image.')#line:92
    OO000O000O0OO0OOO .add_argument ('--no_sort',default =False ,dest ='no_sort',action ='store_true',help ='Do not sort images by hashed image ID.')#line:94
    OO000O000O0OO0OOO .add_argument ('--seed',default =None ,type =int ,help ='The seed to pass into random.seed. Note: this is only really for the shuffle and does not (I think) affect cuda stuff.')#line:96
    OO000O000O0OO0OOO .add_argument ('--mask_proto_debug',default =False ,dest ='mask_proto_debug',action ='store_true',help ='Outputs stuff for scripts/compute_mask.py.')#line:98
    OO000O000O0OO0OOO .add_argument ('--no_crop',default =False ,dest ='crop',action ='store_false',help ='Do not crop output masks with the predicted bounding box.')#line:100
    OO000O000O0OO0OOO .add_argument ('--image',default ='{}:{}'.format (inpass ,outpass ),type =str ,help ='A path to an image to use for display.')#line:102
    OO000O000O0OO0OOO .add_argument ('--images',default =None ,type =str ,help ='An input folder of images and output folder to save detected images. Should be in the format input->output.')#line:104
    OO000O000O0OO0OOO .add_argument ('--video',default =None ,type =str ,help ='A path to a video to evaluate on. Passing in a number will use that index webcam.')#line:106
    OO000O000O0OO0OOO .add_argument ('--video_multiframe',default =1 ,type =int ,help ='The number of frames to evaluate in parallel to make videos play at higher fps.')#line:108
    OO000O000O0OO0OOO .add_argument ('--score_threshold',default =0.15 ,type =float ,help ='Detections with a score under this threshold will not be considered. This currently only works in display mode.')#line:110
    OO000O000O0OO0OOO .add_argument ('--dataset',default =None ,type =str ,help ='If specified, override the dataset specified in the config with this one (example: coco2017_dataset).')#line:112
    OO000O000O0OO0OOO .add_argument ('--detect',default =False ,dest ='detect',action ='store_true',help ='Don\'t evauluate the mask branch at all and only do object detection. This only works for --display and --benchmark.')#line:114
    OO000O000O0OO0OOO .set_defaults (no_bar =False ,display =False ,resume =False ,output_coco_json =False ,output_web_json =False ,shuffle =False ,benchmark =False ,no_sort =False ,no_hash =False ,mask_proto_debug =False ,crop =True ,detect =False )#line:117
    global args #line:119
    args =OO000O000O0OO0OOO .parse_args (argv )#line:120
    if args .output_web_json :#line:122
        args .output_coco_json =True #line:123
    if args .seed is not None :#line:125
        random .seed (args .seed )#line:126
iou_thresholds =[OO00000O0O0O0OO00 /100 for OO00000O0O0O0OO00 in range (50 ,100 ,5 )]#line:128
coco_cats ={}#line:129
coco_cats_inv ={}#line:130
color_cache =defaultdict (lambda :{})#line:131
def prep_display (O00O0O000OO00O0O0 ,OO00OOO0O0OOOO000 ,O00O0O0O00OO0000O ,OO00OO0O000O00O00 ,OOO0O000OO0000000 ,undo_transform =True ,class_color =False ,mask_alpha =0.45 ,w_aim =256 ,h_aim =512 ):#line:133
    ""#line:136
    if undo_transform :#line:137
        O0000O0000O0O0OOO =undo_image_transformation (O00O0O0O00OO0000O ,OOO0O000OO0000000 ,OO00OO0O000O00O00 )#line:138
        O00OOO0OOO000O0O0 =torch .Tensor (O0000O0000O0O0OOO )#line:140
    else :#line:141
        O00OOO0OOO000O0O0 =O00O0O0O00OO0000O /255.0 #line:142
        OO00OO0O000O00O00 ,OOO0O000OO0000000 ,_OOOO00O000O00OO0O =O00O0O0O00OO0000O .shape #line:143
    with timer .env ('Postprocess'):#line:145
        OO00OOOOO0OO00OOO =postprocess (OO00OOO0O0OOOO000 ,OOO0O000OO0000000 ,OO00OO0O000O00O00 ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:148
    with timer .env ('Copy'):#line:152
        if cfg .eval_mask_branch :#line:153
            OO0OO0O0OOOO0OOOO =OO00OOOOO0OO00OOO [3 ][:args .top_k ]#line:155
        O0O00000O00O0OOOO ,OO0O000O0OOO000OO ,O00OO0OO000O00O00 =[OO000O000000OO000 [:args .top_k ].cpu ().numpy ()for OO000O000000OO000 in OO00OOOOO0OO00OOO [:3 ]]#line:156
    O00O0OOO0OO0O00O0 =np .array (O0O00000O00O0OOOO ,str )#line:159
    O00O0OOO0OO0O00O0 [O00O0OOO0OO0O00O0 =='0']='person'#line:160
    O00O0OOO0OO0O00O0 [O00O0OOO0OO0O00O0 =='24']='backpack'#line:161
    O00O0OOO0OO0O00O0 [O00O0OOO0OO0O00O0 =='26']='handbag'#line:162
    O00O0OOO0OO0O00O0 [O00O0OOO0OO0O00O0 =='27']='tie'#line:163
    print ('detected: {}'.format (O00O0OOO0OO0O00O0 ))#line:164
    OO00OOOO0OOO000OO =min (args .top_k ,O0O00000O00O0OOOO .shape [0 ])#line:168
    for OO0000O0OO000OOO0 in range (OO00OOOO0OOO000OO ):#line:169
        if OO0O000O0OOO000OO [OO0000O0OO000OOO0 ]<args .score_threshold :#line:170
            OO00OOOO0OOO000OO =OO0000O0OO000OOO0 #line:171
            break #line:172
    if OO00OOOO0OOO000OO ==0 :#line:179
        O0OO000000OO0OO00 =np .ones ((h_aim ,w_aim ),'uint8')*255 #line:180
        return O0OO000000OO0OO00 #line:181
    def O0O00O0OO00000000 (OO0O0OO0OOOO00OOO ,on_gpu =None ):#line:185
        global color_cache #line:186
        O0O0OO0O0000O0OO0 =(O0O00000O00O0OOOO [OO0O0OO0OOOO00OOO ]*5 if class_color else OO0O0OO0OOOO00OOO *5 )%len (COLORS )#line:187
        if on_gpu is not None and O0O0OO0O0000O0OO0 in color_cache [on_gpu ]:#line:189
            return color_cache [on_gpu ][O0O0OO0O0000O0OO0 ]#line:190
        else :#line:191
            O0O0OOOOO0OO000OO =COLORS [O0O0OO0O0000O0OO0 ]#line:192
            if not undo_transform :#line:193
                O0O0OOOOO0OO000OO =(O0O0OOOOO0OO000OO [2 ],O0O0OOOOO0OO000OO [1 ],O0O0OOOOO0OO000OO [0 ])#line:195
            if on_gpu is not None :#line:196
                O0O0OOOOO0OO000OO =torch .Tensor (O0O0OOOOO0OO000OO ).to (on_gpu ).float ()/255. #line:197
                color_cache [on_gpu ][O0O0OO0O0000O0OO0 ]=O0O0OOOOO0OO000OO #line:198
            return O0O0OOOOO0OO000OO #line:202
    if args .display_masks and cfg .eval_mask_branch :#line:205
        OO0OO0O0OOOO0OOOO =OO0OO0O0OOOO0OOOO [:OO00OOOO0OOO000OO ,:,:,None ]#line:207
        OO0OO0O0OOOO0OOOO =np .array (OO0OO0O0OOOO0OOOO )#line:210
        OO0OO0O0OOOO0OOOO =OO0OO0O0OOOO0OOOO .reshape (OO0OO0O0OOOO0OOOO .shape [:-1 ])#line:212
        O0O00O00O000O0OO0 =[]#line:217
        OOO000000OO00O00O =len (O00O0O000OO00O0O0 )*len (O00O0O000OO00O0O0 [0 ])#line:219
        O00O0OOO00OOO0O00 ,OOOO0O000O00OO000 =0 ,0 #line:221
        OOOOOOOO0O0O00OO0 =None #line:222
        for OO0OO000O000O00OO in range (len (O0O00000O00O0OOOO )):#line:223
            if O0O00000O00O0OOOO [OO0OO000O000O00OO ]==0 and np .sum (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ,:,:])>OOO000000OO00O00O *0.15 *0.5 :#line:224
                O00O0OOO00OOO0O00 =np .sum (np .array (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ]))#line:225
                if O00O0OOO00OOO0O00 >OOOO0O000O00OO000 :#line:226
                    OOOO0O000O00OO000 =O00O0OOO00OOO0O00 #line:227
                    OOOOOOOO0O0O00OO0 =OO0OO000O000O00OO #line:228
        if OOOOOOOO0O0O00OO0 is not None :#line:229
            O0O00O00O000O0OO0 .append (OOOOOOOO0O0O00OO0 )#line:230
        O00O0OOO00OOO0O00 ,OOOO0O000O00OO000 =0 ,0 #line:232
        OOOOOOOO0O0O00OO0 =None #line:233
        for OO0OO000O000O00OO in range (len (O0O00000O00O0OOOO )):#line:234
            if O0O00000O00O0OOOO [OO0OO000O000O00OO ]==24 and np .sum (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ,:,:])>OOO000000OO00O00O *0.009 *0.5 :#line:235
                O00O0OOO00OOO0O00 =np .sum (np .array (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ]))#line:236
                if O00O0OOO00OOO0O00 >OOOO0O000O00OO000 :#line:237
                    OOOO0O000O00OO000 =O00O0OOO00OOO0O00 #line:238
                    OOOOOOOO0O0O00OO0 =OO0OO000O000O00OO #line:239
        if OOOOOOOO0O0O00OO0 is not None :#line:240
            O0O00O00O000O0OO0 .append (OOOOOOOO0O0O00OO0 )#line:241
        O00O0OOO00OOO0O00 ,OOOO0O000O00OO000 =0 ,0 #line:243
        OOOOOOOO0O0O00OO0 =None #line:244
        for OO0OO000O000O00OO in range (len (O0O00000O00O0OOOO )):#line:245
            if O0O00000O00O0OOOO [OO0OO000O000O00OO ]==26 and np .sum (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ,:,:])>OOO000000OO00O00O *0.009 *0.5 :#line:246
                O00O0OOO00OOO0O00 =np .sum (np .array (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ]))#line:247
                if O00O0OOO00OOO0O00 >OOOO0O000O00OO000 :#line:248
                    OOOO0O000O00OO000 =O00O0OOO00OOO0O00 #line:249
                    OOOOOOOO0O0O00OO0 =OO0OO000O000O00OO #line:250
        if OOOOOOOO0O0O00OO0 is not None :#line:251
            O0O00O00O000O0OO0 .append (OOOOOOOO0O0O00OO0 )#line:252
        O00O0OOO00OOO0O00 ,OOOO0O000O00OO000 =0 ,0 #line:254
        OOOOOOOO0O0O00OO0 =None #line:255
        for OO0OO000O000O00OO in range (len (O0O00000O00O0OOOO )):#line:256
            if O0O00000O00O0OOOO [OO0OO000O000O00OO ]==27 and np .sum (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ,:,:])>OOO000000OO00O00O *0.0025 *0.5 :#line:257
                O00O0OOO00OOO0O00 =np .sum (np .array (OO0OO0O0OOOO0OOOO [OO0OO000O000O00OO ]))#line:258
                if O00O0OOO00OOO0O00 >OOOO0O000O00OO000 :#line:259
                    OOOO0O000O00OO000 =O00O0OOO00OOO0O00 #line:260
                    OOOOOOOO0O0O00OO0 =OO0OO000O000O00OO #line:261
        if OOOOOOOO0O0O00OO0 is not None :#line:262
            O0O00O00O000O0OO0 .append (OOOOOOOO0O0O00OO0 )#line:263
        print ('valid index: {}'.format (O0O00O00O000O0OO0 ))#line:268
        if len (O0O00O00O000O0OO0 )==0 :#line:271
            O0OO000000OO0OO00 =np .ones ((h_aim ,w_aim ,3 ),'uint8')*255 #line:272
            return O0OO000000OO0OO00 #line:273
        OO0OO0O0OOOO0OOOO =OO0OO0O0OOOO0OOOO [O0O00O00O000O0OO0 ]#line:279
        O0O0OO00OO000000O =np .max (OO0OO0O0OOOO0OOOO ,axis =0 )#line:283
        O0OO00O0OOOO0OO00 =np .ones ((5 ,5 ),np .uint8 )#line:307
        OOO00000O00OOO0O0 =cv2 .morphologyEx (O0O0OO00OO000000O ,cv2 .MORPH_CLOSE ,O0OO00O0OOOO0OO00 )#line:308
        OOO00000O00OOO0O0 =np .array (OOO00000O00OOO0O0 ,'uint8')#line:310
        try :#line:313
            _OOOO00O000O00OO0O ,OO00OOOOO0000OOOO ,_OOOO00O000O00OO0O =cv2 .findContours (OOO00000O00OOO0O0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:314
        except :#line:315
            OO00OOOOO0000OOOO ,_OOOO00O000O00OO0O =cv2 .findContours (OOO00000O00OOO0O0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:316
        O000O0O00OO000000 =max (OO00OOOOO0000OOOO ,key =lambda OOOO0OOOOOO00OOO0 :cv2 .contourArea (OOOO0OOOOOO00OOO0 ))#line:319
        OOO000O0O00OOOO0O =np .zeros_like (OOO00000O00OOO0O0 )#line:322
        O0O0000OOOOOOOOO0 =cv2 .drawContours (OOO000O0O00OOOO0O ,[O000O0O00OO000000 ],-1 ,color =255 ,thickness =-1 )#line:323
        O0OOOO0000O0O0O00 =np .min (np .where (O0O0000OOOOOOOOO0 >0 )[0 ])#line:327
        OO0O00O00O0OOO0O0 =np .max (np .where (O0O0000OOOOOOOOO0 >0 )[0 ])#line:328
        OO00O0OO00O0OOOOO =np .min (np .where (O0O0000OOOOOOOOO0 >0 )[1 ])#line:329
        O00O00000OOO0OOOO =np .max (np .where (O0O0000OOOOOOOOO0 >0 )[1 ])#line:330
        O00O0O000OO00O0O0 [:,:,0 ][O0O0000OOOOOOOOO0 ==0 ]=255 #line:334
        O00O0O000OO00O0O0 [:,:,1 ][O0O0000OOOOOOOOO0 ==0 ]=255 #line:335
        O00O0O000OO00O0O0 [:,:,2 ][O0O0000OOOOOOOOO0 ==0 ]=255 #line:336
        O00O0O0O00OO0000O =cv2 .cvtColor (O00O0O000OO00O0O0 ,cv2 .COLOR_BGR2RGB )#line:340
        O00O0O0O00OO0000O =Image .fromarray (O00O0O0O00OO0000O )#line:341
        O00O0O0O00OO0000O =O00O0O0O00OO0000O .crop ((OO00O0OO00O0OOOOO ,O0OOOO0000O0O0O00 ,O00O00000OOO0OOOO ,OO0O00O00O0OOO0O0 ))#line:348
        OOO0O000OO0000000 ,OO00OO0O000O00O00 =O00O0O0O00OO0000O .size #line:349
        OO0000O0OOOOOOO00 =int (h_aim *0.95 )#line:352
        O00O0O0O00OO0000O =O00O0O0O00OO0000O .resize ((int (OOO0O000OO0000000 *OO0000O0OOOOOOO00 /OO00OO0O000O00O00 ),OO0000O0OOOOOOO00 ),Image .BICUBIC )#line:353
        OOO0O000OO0000000 ,OO00OO0O000O00O00 =O00O0O0O00OO0000O .size #line:354
        O00O000OOOO0OOOO0 =Image .new ('RGB',(w_aim ,h_aim ),(255 ,255 ,255 ))#line:358
        O00O000OOOO0OOOO0 .paste (O00O0O0O00OO0000O ,(w_aim //2 -OOO0O000OO0000000 //2 ,int (h_aim *0.03 )))#line:359
        return O00O000OOOO0OOOO0 #line:365
    return O0000O0000O0O0OOO #line:417
def evalimage (OO0OO0OOO00O0OO00 ,O0OOO00O0OO00OOOO :Yolact ,O0000OOO000OOOO0O :str ,save_path :str =None ,w_aim =256 ,h_aim =512 ):#line:421
    OO0OOOO000OOOOO00 =torch .from_numpy (OO0OO0OOO00O0OO00 ).float ()#line:423
    OO000000O0O0O000O =FastBaseTransform ()(OO0OOOO000OOOOO00 .unsqueeze (0 ))#line:424
    O00O0OOO0OOOOO000 =O0OOO00O0OO00OOOO (OO000000O0O0O000O )#line:425
    OO000OO0O0O00O00O =prep_display (OO0OO0OOO00O0OO00 ,O00O0OOO0OOOOO000 ,OO0OOOO000OOOOO00 ,None ,None ,undo_transform =False ,w_aim =w_aim ,h_aim =h_aim )#line:428
    return OO000OO0O0O00O00O #line:434
def evaluate (O0O0OOOO0000O0O0O :Yolact ,OOO0O0OO0O00000O0 ,OOOO0000OOOO0OO0O ,train_mode =False ,w_aim =256 ,h_aim =512 ):#line:439
    O0O0OOOO0000O0O0O .detect .use_fast_nms =args .fast_nms #line:440
    cfg .mask_proto_debug =args .mask_proto_debug #line:441
    OOOO00O0OOO0000OO ,O0000OOO0OOOOO0O0 =args .image .split (':')#line:443
    O0O000O0OOO0O000O =evalimage (OOOO0000OOOO0OO0O ,O0O0OOOO0000O0O0O ,OOOO00O0OOO0000OO ,O0000OOO0OOOOO0O0 ,w_aim =w_aim ,h_aim =h_aim )#line:444
    return O0O000O0OOO0O000O #line:445
class tool_mask :#line:481
    def __init__ (O00OO00O0O00O0O00 ,O0000OO0OO0OOOOOO ):#line:482
        parse_args (model_path =O0000OO0OO0OOOOOO )#line:485
        if args .config is None :#line:487
            O0000OO0OO0OOOOOO =SavePath .from_str (args .trained_model )#line:488
            args .config =O0000OO0OO0OOOOOO .model_name +'_config'#line:490
            set_cfg (args .config )#line:492
        with torch .no_grad ():#line:494
            print ('Loading mask model...',end ='')#line:498
            O00OO00O0O00O0O00 .net =Yolact ()#line:499
            O00OO00O0O00O0O00 .net .load_weights (args .trained_model )#line:500
            O00OO00O0O00O0O00 .net .eval ()#line:502
            print ('Done.')#line:503
            if args .cuda :#line:505
                O00OO00O0O00O0O00 .net =O00OO00O0O00O0O00 .net #line:507
    def __del__ (O0O00OOO000OO0O0O ):#line:511
        pass #line:512
    def do_mask (O000O00OO00000000 ,O000O0O00O000O00O ,w_aim =256 ,h_aim =512 ):#line:515
        parse_args ()#line:517
        O000O0O00O000O00O =cv2 .cvtColor (O000O0O00O000O00O ,cv2 .COLOR_RGB2BGR )#line:520
        with torch .no_grad ():#line:522
            OO00000O000O00000 =None #line:524
            OOOO0O0OOOO0OOOO0 =evaluate (O000O00OO00000000 .net ,OO00000O000O00000 ,O000O0O00O000O00O ,w_aim =w_aim ,h_aim =h_aim )#line:526
        print ('mask end.')#line:530
        return np .array (OOOO0O0OOOO0OOOO0 ,'uint8')#line:531
if __name__ =='__main__':#line:535
    pass #line:537
