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
def show (O0OO0OO00OO0OO0O0 ,O0O00OO0O0O0000OO =8 ):#line:26
    plt .figure (figsize =(O0O00OO0O0O0000OO ,O0O00OO0O0O0000OO ))#line:27
    if np .max (O0OO0OO00OO0OO0O0 )<=1 :#line:28
        plt .imshow (O0OO0OO00OO0OO0O0 ,vmin =0 ,vmax =1 )#line:29
    else :#line:30
        plt .imshow (O0OO0OO00OO0OO0O0 ,vmin =0 ,vmax =255 )#line:31
    plt .gray ()#line:32
    plt .show ()#line:33
    plt .close ()#line:34
    print ()#line:35
def str2bool (O00O000OO00O0O000 ):#line:37
    if O00O000OO00O0O000 .lower ()in ('yes','true','t','y','1'):#line:38
        return True #line:39
    elif O00O000OO00O0O000 .lower ()in ('no','false','f','n','0'):#line:40
        return False #line:41
    else :#line:42
        raise argparse .ArgumentTypeError ('Boolean value expected.')#line:43
def parse_args (O000OOOO00000OOO0 =None ,OOO000OOO000000O0 =None ,OO0O0O0O0O000O000 =None ,O0O0O0O00O0OOOO00 =None ):#line:45
    O0OO0O00O00O000O0 =argparse .ArgumentParser (description ='YOLACT COCO Evaluation')#line:47
    O0OO0O00O00O000O0 .add_argument ('--trained_model',default =O0O0O0O00O0OOOO00 ,type =str ,help ='Trained state_dict file path to open. If "interrupt", this will open the interrupt file.')#line:50
    O0OO0O00O00O000O0 .add_argument ('--top_k',default =10 ,type =int ,help ='Further restrict the number of predictions to parse')#line:52
    O0OO0O00O00O000O0 .add_argument ('--cuda',default =True ,type =str2bool ,help ='Use cuda to evaulate model')#line:54
    O0OO0O00O00O000O0 .add_argument ('--fast_nms',default =True ,type =str2bool ,help ='Whether to use a faster, but not entirely correct version of NMS.')#line:56
    O0OO0O00O00O000O0 .add_argument ('--display_masks',default =True ,type =str2bool ,help ='Whether or not to display masks over bounding boxes')#line:58
    O0OO0O00O00O000O0 .add_argument ('--display_bboxes',default =True ,type =str2bool ,help ='Whether or not to display bboxes around masks')#line:60
    O0OO0O00O00O000O0 .add_argument ('--display_text',default =True ,type =str2bool ,help ='Whether or not to display text (class [score])')#line:62
    O0OO0O00O00O000O0 .add_argument ('--display_scores',default =True ,type =str2bool ,help ='Whether or not to display scores in addition to classes')#line:64
    O0OO0O00O00O000O0 .add_argument ('--display',dest ='display',action ='store_true',help ='Display qualitative results instead of quantitative ones.')#line:66
    O0OO0O00O00O000O0 .add_argument ('--shuffle',dest ='shuffle',action ='store_true',help ='Shuffles the images when displaying them. Doesn\'t have much of an effect when display is off though.')#line:68
    O0OO0O00O00O000O0 .add_argument ('--ap_data_file',default ='results/ap_data.pkl',type =str ,help ='In quantitative mode, the file to save detections before calculating mAP.')#line:70
    O0OO0O00O00O000O0 .add_argument ('--resume',dest ='resume',action ='store_true',help ='If display not set, this resumes mAP calculations from the ap_data_file.')#line:72
    O0OO0O00O00O000O0 .add_argument ('--max_images',default =-1 ,type =int ,help ='The maximum number of images from the dataset to consider. Use -1 for all.')#line:74
    O0OO0O00O00O000O0 .add_argument ('--output_coco_json',dest ='output_coco_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this just dumps detections into the coco json file.')#line:76
    O0OO0O00O00O000O0 .add_argument ('--bbox_det_file',default ='results/bbox_detections.json',type =str ,help ='The output file for coco bbox results if --coco_results is set.')#line:78
    O0OO0O00O00O000O0 .add_argument ('--mask_det_file',default ='results/mask_detections.json',type =str ,help ='The output file for coco mask results if --coco_results is set.')#line:80
    O0OO0O00O00O000O0 .add_argument ('--config',default =None ,help ='The config object to use.')#line:82
    O0OO0O00O00O000O0 .add_argument ('--output_web_json',dest ='output_web_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this dumps detections for usage with the detections viewer web thingy.')#line:84
    O0OO0O00O00O000O0 .add_argument ('--web_det_path',default ='web/dets/',type =str ,help ='If output_web_json is set, this is the path to dump detections into.')#line:86
    O0OO0O00O00O000O0 .add_argument ('--no_bar',dest ='no_bar',action ='store_true',help ='Do not output the status bar. This is useful for when piping to a file.')#line:88
    O0OO0O00O00O000O0 .add_argument ('--display_lincomb',default =False ,type =str2bool ,help ='If the config uses lincomb masks, output a visualization of how those masks are created.')#line:90
    O0OO0O00O00O000O0 .add_argument ('--benchmark',default =False ,dest ='benchmark',action ='store_true',help ='Equivalent to running display mode but without displaying an image.')#line:92
    O0OO0O00O00O000O0 .add_argument ('--no_sort',default =False ,dest ='no_sort',action ='store_true',help ='Do not sort images by hashed image ID.')#line:94
    O0OO0O00O00O000O0 .add_argument ('--seed',default =None ,type =int ,help ='The seed to pass into random.seed. Note: this is only really for the shuffle and does not (I think) affect cuda stuff.')#line:96
    O0OO0O00O00O000O0 .add_argument ('--mask_proto_debug',default =False ,dest ='mask_proto_debug',action ='store_true',help ='Outputs stuff for scripts/compute_mask.py.')#line:98
    O0OO0O00O00O000O0 .add_argument ('--no_crop',default =False ,dest ='crop',action ='store_false',help ='Do not crop output masks with the predicted bounding box.')#line:100
    O0OO0O00O00O000O0 .add_argument ('--image',default ='{}:{}'.format (OOO000OOO000000O0 ,OO0O0O0O0O000O000 ),type =str ,help ='A path to an image to use for display.')#line:102
    O0OO0O00O00O000O0 .add_argument ('--images',default =None ,type =str ,help ='An input folder of images and output folder to save detected images. Should be in the format input->output.')#line:104
    O0OO0O00O00O000O0 .add_argument ('--video',default =None ,type =str ,help ='A path to a video to evaluate on. Passing in a number will use that index webcam.')#line:106
    O0OO0O00O00O000O0 .add_argument ('--video_multiframe',default =1 ,type =int ,help ='The number of frames to evaluate in parallel to make videos play at higher fps.')#line:108
    O0OO0O00O00O000O0 .add_argument ('--score_threshold',default =0.15 ,type =float ,help ='Detections with a score under this threshold will not be considered. This currently only works in display mode.')#line:110
    O0OO0O00O00O000O0 .add_argument ('--dataset',default =None ,type =str ,help ='If specified, override the dataset specified in the config with this one (example: coco2017_dataset).')#line:112
    O0OO0O00O00O000O0 .add_argument ('--detect',default =False ,dest ='detect',action ='store_true',help ='Don\'t evauluate the mask branch at all and only do object detection. This only works for --display and --benchmark.')#line:114
    O0OO0O00O00O000O0 .set_defaults (no_bar =False ,display =False ,resume =False ,output_coco_json =False ,output_web_json =False ,shuffle =False ,benchmark =False ,no_sort =False ,no_hash =False ,mask_proto_debug =False ,crop =True ,detect =False )#line:117
    global args #line:119
    args =O0OO0O00O00O000O0 .parse_args (O000OOOO00000OOO0 )#line:120
    if args .output_web_json :#line:122
        args .output_coco_json =True #line:123
    if args .seed is not None :#line:125
        random .seed (args .seed )#line:126
iou_thresholds =[OO00000OO0O000O00 /100 for OO00000OO0O000O00 in range (50 ,100 ,5 )]#line:128
coco_cats ={}#line:129
coco_cats_inv ={}#line:130
color_cache =defaultdict (lambda :{})#line:131
def prep_display (O0O00OO0O00O0OOO0 ,O0O000O0O0O00000O ,OO00O0O0OO00OO000 ,OOOO000O0OO0OOOO0 ,OOOO00OO0OOOO0000 ,OOOO0OOO0O0000O00 =True ,O00000OOO00OOO00O =False ,O00OOOO0O0OO0OOOO =0.45 ,O00O0O0OOO0OOO0OO =256 ,OOO0OOOOOO00O0OO0 =512 ):#line:133
    ""#line:136
    if OOOO0OOO0O0000O00 :#line:137
        OOO0OOOOOO0OO00OO =undo_image_transformation (OO00O0O0OO00OO000 ,OOOO00OO0OOOO0000 ,OOOO000O0OO0OOOO0 )#line:138
        OOOOO00OOOOO00OO0 =torch .Tensor (OOO0OOOOOO0OO00OO )#line:140
    else :#line:141
        OOOOO00OOOOO00OO0 =OO00O0O0OO00OO000 /255.0 #line:142
        OOOO000O0OO0OOOO0 ,OOOO00OO0OOOO0000 ,_OOO0O0000000OOOO0 =OO00O0O0OO00OO000 .shape #line:143
    with timer .env ('Postprocess'):#line:145
        O0O00OOOO0O0O00O0 =postprocess (O0O000O0O0O00000O ,OOOO00OO0OOOO0000 ,OOOO000O0OO0OOOO0 ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:148
    with timer .env ('Copy'):#line:152
        if cfg .eval_mask_branch :#line:153
            O0OO0OOO000000O00 =O0O00OOOO0O0O00O0 [3 ][:args .top_k ]#line:155
        O0O0OO00000O0O000 ,OOOOOOOOO0000OO00 ,O00OOO00OO0OOO000 =[O000OOO00O0OOOO00 [:args .top_k ].cpu ().numpy ()for O000OOO00O0OOOO00 in O0O00OOOO0O0O00O0 [:3 ]]#line:156
    OO0OOOO0OOO0O0000 =np .array (O0O0OO00000O0O000 ,str )#line:159
    OO0OOOO0OOO0O0000 [OO0OOOO0OOO0O0000 =='0']='person'#line:160
    OO0OOOO0OOO0O0000 [OO0OOOO0OOO0O0000 =='24']='backpack'#line:161
    OO0OOOO0OOO0O0000 [OO0OOOO0OOO0O0000 =='26']='handbag'#line:162
    OO0OOOO0OOO0O0000 [OO0OOOO0OOO0O0000 =='27']='tie'#line:163
    print ('detected: {}'.format (OO0OOOO0OOO0O0000 ))#line:164
    OOOO00O000O0000O0 =min (args .top_k ,O0O0OO00000O0O000 .shape [0 ])#line:168
    for O00O000O000OO0000 in range (OOOO00O000O0000O0 ):#line:169
        if OOOOOOOOO0000OO00 [O00O000O000OO0000 ]<args .score_threshold :#line:170
            OOOO00O000O0000O0 =O00O000O000OO0000 #line:171
            break #line:172
    if OOOO00O000O0000O0 ==0 :#line:179
        OO00O0OOO0OOOO0O0 =np .ones ((OOO0OOOOOO00O0OO0 ,O00O0O0OOO0OOO0OO ),'uint8')*255 #line:180
        return OO00O0OOO0OOOO0O0 #line:181
    def O0000OOOOOO0OO0O0 (O00O000OOO000O0OO ,OOO0OOO0OO00000O0 =None ):#line:185
        global color_cache #line:186
        O0OO0O0OO0OO0OO00 =(O0O0OO00000O0O000 [O00O000OOO000O0OO ]*5 if O00000OOO00OOO00O else O00O000OOO000O0OO *5 )%len (COLORS )#line:187
        if OOO0OOO0OO00000O0 is not None and O0OO0O0OO0OO0OO00 in color_cache [OOO0OOO0OO00000O0 ]:#line:189
            return color_cache [OOO0OOO0OO00000O0 ][O0OO0O0OO0OO0OO00 ]#line:190
        else :#line:191
            O0000O0OOO00OO0O0 =COLORS [O0OO0O0OO0OO0OO00 ]#line:192
            if not OOOO0OOO0O0000O00 :#line:193
                O0000O0OOO00OO0O0 =(O0000O0OOO00OO0O0 [2 ],O0000O0OOO00OO0O0 [1 ],O0000O0OOO00OO0O0 [0 ])#line:195
            if OOO0OOO0OO00000O0 is not None :#line:196
                O0000O0OOO00OO0O0 =torch .Tensor (O0000O0OOO00OO0O0 ).to (OOO0OOO0OO00000O0 ).float ()/255. #line:197
                color_cache [OOO0OOO0OO00000O0 ][O0OO0O0OO0OO0OO00 ]=O0000O0OOO00OO0O0 #line:198
            return O0000O0OOO00OO0O0 #line:202
    if args .display_masks and cfg .eval_mask_branch :#line:205
        O0OO0OOO000000O00 =O0OO0OOO000000O00 [:OOOO00O000O0000O0 ,:,:,None ]#line:207
        O0OO0OOO000000O00 =np .array (O0OO0OOO000000O00 )#line:210
        O0OO0OOO000000O00 =O0OO0OOO000000O00 .reshape (O0OO0OOO000000O00 .shape [:-1 ])#line:212
        O00O00O0000000OOO =[]#line:217
        OO0OO00OO0OOO0000 =len (O0O00OO0O00O0OOO0 )*len (O0O00OO0O00O0OOO0 [0 ])#line:219
        OO0000O00000O0OOO ,O0O000000OOO00000 =0 ,0 #line:221
        OOOOOO0O00O000O0O =None #line:222
        for O00OOOO0O0000000O in range (len (O0O0OO00000O0O000 )):#line:223
            if O0O0OO00000O0O000 [O00OOOO0O0000000O ]==0 and np .sum (O0OO0OOO000000O00 [O00OOOO0O0000000O ,:,:])>OO0OO00OO0OOO0000 *0.15 *0.5 :#line:224
                OO0000O00000O0OOO =np .sum (np .array (O0OO0OOO000000O00 [O00OOOO0O0000000O ]))#line:225
                if OO0000O00000O0OOO >O0O000000OOO00000 :#line:226
                    O0O000000OOO00000 =OO0000O00000O0OOO #line:227
                    OOOOOO0O00O000O0O =O00OOOO0O0000000O #line:228
        if OOOOOO0O00O000O0O is not None :#line:229
            O00O00O0000000OOO .append (OOOOOO0O00O000O0O )#line:230
        OO0000O00000O0OOO ,O0O000000OOO00000 =0 ,0 #line:232
        OOOOOO0O00O000O0O =None #line:233
        for O00OOOO0O0000000O in range (len (O0O0OO00000O0O000 )):#line:234
            if O0O0OO00000O0O000 [O00OOOO0O0000000O ]==24 and np .sum (O0OO0OOO000000O00 [O00OOOO0O0000000O ,:,:])>OO0OO00OO0OOO0000 *0.009 *0.5 :#line:235
                OO0000O00000O0OOO =np .sum (np .array (O0OO0OOO000000O00 [O00OOOO0O0000000O ]))#line:236
                if OO0000O00000O0OOO >O0O000000OOO00000 :#line:237
                    O0O000000OOO00000 =OO0000O00000O0OOO #line:238
                    OOOOOO0O00O000O0O =O00OOOO0O0000000O #line:239
        if OOOOOO0O00O000O0O is not None :#line:240
            O00O00O0000000OOO .append (OOOOOO0O00O000O0O )#line:241
        OO0000O00000O0OOO ,O0O000000OOO00000 =0 ,0 #line:243
        OOOOOO0O00O000O0O =None #line:244
        for O00OOOO0O0000000O in range (len (O0O0OO00000O0O000 )):#line:245
            if O0O0OO00000O0O000 [O00OOOO0O0000000O ]==26 and np .sum (O0OO0OOO000000O00 [O00OOOO0O0000000O ,:,:])>OO0OO00OO0OOO0000 *0.009 *0.5 :#line:246
                OO0000O00000O0OOO =np .sum (np .array (O0OO0OOO000000O00 [O00OOOO0O0000000O ]))#line:247
                if OO0000O00000O0OOO >O0O000000OOO00000 :#line:248
                    O0O000000OOO00000 =OO0000O00000O0OOO #line:249
                    OOOOOO0O00O000O0O =O00OOOO0O0000000O #line:250
        if OOOOOO0O00O000O0O is not None :#line:251
            O00O00O0000000OOO .append (OOOOOO0O00O000O0O )#line:252
        OO0000O00000O0OOO ,O0O000000OOO00000 =0 ,0 #line:254
        OOOOOO0O00O000O0O =None #line:255
        for O00OOOO0O0000000O in range (len (O0O0OO00000O0O000 )):#line:256
            if O0O0OO00000O0O000 [O00OOOO0O0000000O ]==27 and np .sum (O0OO0OOO000000O00 [O00OOOO0O0000000O ,:,:])>OO0OO00OO0OOO0000 *0.0025 *0.5 :#line:257
                OO0000O00000O0OOO =np .sum (np .array (O0OO0OOO000000O00 [O00OOOO0O0000000O ]))#line:258
                if OO0000O00000O0OOO >O0O000000OOO00000 :#line:259
                    O0O000000OOO00000 =OO0000O00000O0OOO #line:260
                    OOOOOO0O00O000O0O =O00OOOO0O0000000O #line:261
        if OOOOOO0O00O000O0O is not None :#line:262
            O00O00O0000000OOO .append (OOOOOO0O00O000O0O )#line:263
        print ('valid index: {}'.format (O00O00O0000000OOO ))#line:268
        if len (O00O00O0000000OOO )==0 :#line:271
            OO00O0OOO0OOOO0O0 =np .ones ((OOO0OOOOOO00O0OO0 ,O00O0O0OOO0OOO0OO ,3 ),'uint8')*255 #line:272
            return OO00O0OOO0OOOO0O0 #line:273
        O0OO0OOO000000O00 =O0OO0OOO000000O00 [O00O00O0000000OOO ]#line:279
        OO000OO0OO000O0O0 =np .max (O0OO0OOO000000O00 ,axis =0 )#line:283
        O00000OO000O0O00O =np .ones ((5 ,5 ),np .uint8 )#line:307
        O00O0O0OOOO000OO0 =cv2 .morphologyEx (OO000OO0OO000O0O0 ,cv2 .MORPH_CLOSE ,O00000OO000O0O00O )#line:308
        O00O0O0OOOO000OO0 =np .array (O00O0O0OOOO000OO0 ,'uint8')#line:310
        try :#line:313
            _OOO0O0000000OOOO0 ,O0O00OOO0OOOOOOOO ,_OOO0O0000000OOOO0 =cv2 .findContours (O00O0O0OOOO000OO0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:314
        except :#line:315
            O0O00OOO0OOOOOOOO ,_OOO0O0000000OOOO0 =cv2 .findContours (O00O0O0OOOO000OO0 ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:316
        OOOOO00000OO0OO0O =max (O0O00OOO0OOOOOOOO ,key =lambda O0O0O0O0OOOO00OOO :cv2 .contourArea (O0O0O0O0OOOO00OOO ))#line:319
        O00OO00O0OO000OO0 =np .zeros_like (O00O0O0OOOO000OO0 )#line:322
        O000000O00O00OOO0 =cv2 .drawContours (O00OO00O0OO000OO0 ,[OOOOO00000OO0OO0O ],-1 ,color =255 ,thickness =-1 )#line:323
        O0OOOO00OOOO0O000 =np .min (np .where (O000000O00O00OOO0 >0 )[0 ])#line:327
        OOO0O0O0O0O0OO000 =np .max (np .where (O000000O00O00OOO0 >0 )[0 ])#line:328
        OO0OOO00OOO0O0O00 =np .min (np .where (O000000O00O00OOO0 >0 )[1 ])#line:329
        O00OO0O00000000OO =np .max (np .where (O000000O00O00OOO0 >0 )[1 ])#line:330
        O0O00OO0O00O0OOO0 [:,:,0 ][O000000O00O00OOO0 ==0 ]=255 #line:334
        O0O00OO0O00O0OOO0 [:,:,1 ][O000000O00O00OOO0 ==0 ]=255 #line:335
        O0O00OO0O00O0OOO0 [:,:,2 ][O000000O00O00OOO0 ==0 ]=255 #line:336
        OO00O0O0OO00OO000 =cv2 .cvtColor (O0O00OO0O00O0OOO0 ,cv2 .COLOR_BGR2RGB )#line:340
        OO00O0O0OO00OO000 =Image .fromarray (OO00O0O0OO00OO000 )#line:341
        OO00O0O0OO00OO000 =OO00O0O0OO00OO000 .crop ((OO0OOO00OOO0O0O00 ,O0OOOO00OOOO0O000 ,O00OO0O00000000OO ,OOO0O0O0O0O0OO000 ))#line:348
        OOOO00OO0OOOO0000 ,OOOO000O0OO0OOOO0 =OO00O0O0OO00OO000 .size #line:349
        OOOOO00OO0O00000O =int (OOO0OOOOOO00O0OO0 *0.95 )#line:352
        OO00O0O0OO00OO000 =OO00O0O0OO00OO000 .resize ((int (OOOO00OO0OOOO0000 *OOOOO00OO0O00000O /OOOO000O0OO0OOOO0 ),OOOOO00OO0O00000O ),Image .BICUBIC )#line:353
        OOOO00OO0OOOO0000 ,OOOO000O0OO0OOOO0 =OO00O0O0OO00OO000 .size #line:354
        O00O00OOO00O0OOOO =Image .new ('RGB',(O00O0O0OOO0OOO0OO ,OOO0OOOOOO00O0OO0 ),(255 ,255 ,255 ))#line:358
        O00O00OOO00O0OOOO .paste (OO00O0O0OO00OO000 ,(O00O0O0OOO0OOO0OO //2 -OOOO00OO0OOOO0000 //2 ,int (OOO0OOOOOO00O0OO0 *0.03 )))#line:359
        return O00O00OOO00O0OOOO #line:365
    return OOO0OOOOOO0OO00OO #line:417
def evalimage (OOO0OO00O0O0OOOO0 ,OO0O0O00OO0OOO00O :Yolact ,OO000OO00OO0O0OOO :str ,OOO0OOOOOO000000O :str =None ,OO00OOO000O0OO000 =256 ,OOO000OO0O0OO000O =512 ):#line:421
    O0O000O0000O0O00O =torch .from_numpy (OOO0OO00O0O0OOOO0 ).float ()#line:423
    OOO0O0O0OOOO0O000 =FastBaseTransform ()(O0O000O0000O0O00O .unsqueeze (0 ))#line:424
    O0OOO0OO0O00OOOO0 =OO0O0O00OO0OOO00O (OOO0O0O0OOOO0O000 )#line:425
    OO00000OO0OO00OO0 =prep_display (OOO0OO00O0O0OOOO0 ,O0OOO0OO0O00OOOO0 ,O0O000O0000O0O00O ,None ,None ,undo_transform =False ,w_aim =OO00OOO000O0OO000 ,h_aim =OOO000OO0O0OO000O )#line:428
    return OO00000OO0OO00OO0 #line:434
def evaluate (OO000OO000O0O0000 :Yolact ,O00OOO0OO0OO000O0 ,O0O0O00OOO0O00O0O ,OOOOOOOO00OO000O0 =False ,O0OOO0OO0O0O0OO0O =256 ,O00O000OO00O00000 =512 ):#line:439
    OO000OO000O0O0000 .detect .use_fast_nms =args .fast_nms #line:440
    cfg .mask_proto_debug =args .mask_proto_debug #line:441
    OOO0O0OOOO00O00O0 ,O0OO0OO0O0O00OOO0 =args .image .split (':')#line:443
    OO00OOOO0O0OO0O0O =evalimage (O0O0O00OOO0O00O0O ,OO000OO000O0O0000 ,OOO0O0OOOO00O00O0 ,O0OO0OO0O0O00OOO0 ,w_aim =O0OOO0OO0O0O0OO0O ,h_aim =O00O000OO00O00000 )#line:444
    return OO00OOOO0O0OO0O0O #line:445
class tool_mask :#line:481
    def __init__ (OOO000OO0O0OOOOOO ,OO0O000OOO00OOO0O ):#line:482
        parse_args (model_path =OO0O000OOO00OOO0O )#line:485
        if args .config is None :#line:487
            OO0O000OOO00OOO0O =SavePath .from_str (args .trained_model )#line:488
            args .config =OO0O000OOO00OOO0O .model_name +'_config'#line:490
            set_cfg (args .config )#line:492
        with torch .no_grad ():#line:494
            print ('Loading mask model...',end ='')#line:498
            OOO000OO0O0OOOOOO .net =Yolact ()#line:499
            OOO000OO0O0OOOOOO .net .load_weights (args .trained_model )#line:500
            OOO000OO0O0OOOOOO .net .eval ()#line:502
            print ('Done.')#line:503
            if args .cuda :#line:505
                OOO000OO0O0OOOOOO .net =OOO000OO0O0OOOOOO .net #line:507
    def __del__ (O000O000OO0O0O0OO ):#line:511
        pass #line:512
    def do_mask (OOO00O00OO00000OO ,O0OO0O000OO00O00O ,O0O000OO0000OOOOO =256 ,OO00OOOO0OO0OOO00 =512 ):#line:515
        parse_args ()#line:517
        O0OO0O000OO00O00O =cv2 .cvtColor (O0OO0O000OO00O00O ,cv2 .COLOR_RGB2BGR )#line:520
        with torch .no_grad ():#line:522
            OO0OO0OO0000O00OO =None #line:524
            OOO0O0OOOO0OO00O0 =evaluate (OOO00O00OO00000OO .net ,OO0OO0OO0000O00OO ,O0OO0O000OO00O00O ,w_aim =O0O000OO0000OOOOO ,h_aim =OO00OOOO0OO0OOO00 )#line:526
        print ('mask end.')#line:530
        return np .array (OOO0O0OOOO0OO00O0 ,'uint8')#line:531
if __name__ =='__main__':#line:535
    pass #line:537
