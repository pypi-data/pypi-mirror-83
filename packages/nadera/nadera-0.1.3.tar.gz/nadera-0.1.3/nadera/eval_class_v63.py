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
def show (O00O0OO000OOOO00O ,size =8 ):#line:26
    plt .figure (figsize =(size ,size ))#line:27
    if np .max (O00O0OO000OOOO00O )<=1 :#line:28
        plt .imshow (O00O0OO000OOOO00O ,vmin =0 ,vmax =1 )#line:29
    else :#line:30
        plt .imshow (O00O0OO000OOOO00O ,vmin =0 ,vmax =255 )#line:31
    plt .gray ()#line:32
    plt .show ()#line:33
    plt .close ()#line:34
    print ()#line:35
def str2bool (O0OOOOO0OO00O00O0 ):#line:37
    if O0OOOOO0OO00O00O0 .lower ()in ('yes','true','t','y','1'):#line:38
        return True #line:39
    elif O0OOOOO0OO00O00O0 .lower ()in ('no','false','f','n','0'):#line:40
        return False #line:41
    else :#line:42
        raise argparse .ArgumentTypeError ('Boolean value expected.')#line:43
def parse_args (argv =None ,inpass =None ,outpass =None ,model_path =None ):#line:45
    O0000O00OO00O0OO0 =argparse .ArgumentParser (description ='YOLACT COCO Evaluation')#line:47
    O0000O00OO00O0OO0 .add_argument ('--trained_model',default =model_path ,type =str ,help ='Trained state_dict file path to open. If "interrupt", this will open the interrupt file.')#line:50
    O0000O00OO00O0OO0 .add_argument ('--top_k',default =10 ,type =int ,help ='Further restrict the number of predictions to parse')#line:52
    O0000O00OO00O0OO0 .add_argument ('--cuda',default =True ,type =str2bool ,help ='Use cuda to evaulate model')#line:54
    O0000O00OO00O0OO0 .add_argument ('--fast_nms',default =True ,type =str2bool ,help ='Whether to use a faster, but not entirely correct version of NMS.')#line:56
    O0000O00OO00O0OO0 .add_argument ('--display_masks',default =True ,type =str2bool ,help ='Whether or not to display masks over bounding boxes')#line:58
    O0000O00OO00O0OO0 .add_argument ('--display_bboxes',default =True ,type =str2bool ,help ='Whether or not to display bboxes around masks')#line:60
    O0000O00OO00O0OO0 .add_argument ('--display_text',default =True ,type =str2bool ,help ='Whether or not to display text (class [score])')#line:62
    O0000O00OO00O0OO0 .add_argument ('--display_scores',default =True ,type =str2bool ,help ='Whether or not to display scores in addition to classes')#line:64
    O0000O00OO00O0OO0 .add_argument ('--display',dest ='display',action ='store_true',help ='Display qualitative results instead of quantitative ones.')#line:66
    O0000O00OO00O0OO0 .add_argument ('--shuffle',dest ='shuffle',action ='store_true',help ='Shuffles the images when displaying them. Doesn\'t have much of an effect when display is off though.')#line:68
    O0000O00OO00O0OO0 .add_argument ('--ap_data_file',default ='results/ap_data.pkl',type =str ,help ='In quantitative mode, the file to save detections before calculating mAP.')#line:70
    O0000O00OO00O0OO0 .add_argument ('--resume',dest ='resume',action ='store_true',help ='If display not set, this resumes mAP calculations from the ap_data_file.')#line:72
    O0000O00OO00O0OO0 .add_argument ('--max_images',default =-1 ,type =int ,help ='The maximum number of images from the dataset to consider. Use -1 for all.')#line:74
    O0000O00OO00O0OO0 .add_argument ('--output_coco_json',dest ='output_coco_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this just dumps detections into the coco json file.')#line:76
    O0000O00OO00O0OO0 .add_argument ('--bbox_det_file',default ='results/bbox_detections.json',type =str ,help ='The output file for coco bbox results if --coco_results is set.')#line:78
    O0000O00OO00O0OO0 .add_argument ('--mask_det_file',default ='results/mask_detections.json',type =str ,help ='The output file for coco mask results if --coco_results is set.')#line:80
    O0000O00OO00O0OO0 .add_argument ('--config',default =None ,help ='The config object to use.')#line:82
    O0000O00OO00O0OO0 .add_argument ('--output_web_json',dest ='output_web_json',action ='store_true',help ='If display is not set, instead of processing IoU values, this dumps detections for usage with the detections viewer web thingy.')#line:84
    O0000O00OO00O0OO0 .add_argument ('--web_det_path',default ='web/dets/',type =str ,help ='If output_web_json is set, this is the path to dump detections into.')#line:86
    O0000O00OO00O0OO0 .add_argument ('--no_bar',dest ='no_bar',action ='store_true',help ='Do not output the status bar. This is useful for when piping to a file.')#line:88
    O0000O00OO00O0OO0 .add_argument ('--display_lincomb',default =False ,type =str2bool ,help ='If the config uses lincomb masks, output a visualization of how those masks are created.')#line:90
    O0000O00OO00O0OO0 .add_argument ('--benchmark',default =False ,dest ='benchmark',action ='store_true',help ='Equivalent to running display mode but without displaying an image.')#line:92
    O0000O00OO00O0OO0 .add_argument ('--no_sort',default =False ,dest ='no_sort',action ='store_true',help ='Do not sort images by hashed image ID.')#line:94
    O0000O00OO00O0OO0 .add_argument ('--seed',default =None ,type =int ,help ='The seed to pass into random.seed. Note: this is only really for the shuffle and does not (I think) affect cuda stuff.')#line:96
    O0000O00OO00O0OO0 .add_argument ('--mask_proto_debug',default =False ,dest ='mask_proto_debug',action ='store_true',help ='Outputs stuff for scripts/compute_mask.py.')#line:98
    O0000O00OO00O0OO0 .add_argument ('--no_crop',default =False ,dest ='crop',action ='store_false',help ='Do not crop output masks with the predicted bounding box.')#line:100
    O0000O00OO00O0OO0 .add_argument ('--image',default ='{}:{}'.format (inpass ,outpass ),type =str ,help ='A path to an image to use for display.')#line:102
    O0000O00OO00O0OO0 .add_argument ('--images',default =None ,type =str ,help ='An input folder of images and output folder to save detected images. Should be in the format input->output.')#line:104
    O0000O00OO00O0OO0 .add_argument ('--video',default =None ,type =str ,help ='A path to a video to evaluate on. Passing in a number will use that index webcam.')#line:106
    O0000O00OO00O0OO0 .add_argument ('--video_multiframe',default =1 ,type =int ,help ='The number of frames to evaluate in parallel to make videos play at higher fps.')#line:108
    O0000O00OO00O0OO0 .add_argument ('--score_threshold',default =0.15 ,type =float ,help ='Detections with a score under this threshold will not be considered. This currently only works in display mode.')#line:110
    O0000O00OO00O0OO0 .add_argument ('--dataset',default =None ,type =str ,help ='If specified, override the dataset specified in the config with this one (example: coco2017_dataset).')#line:112
    O0000O00OO00O0OO0 .add_argument ('--detect',default =False ,dest ='detect',action ='store_true',help ='Don\'t evauluate the mask branch at all and only do object detection. This only works for --display and --benchmark.')#line:114
    O0000O00OO00O0OO0 .set_defaults (no_bar =False ,display =False ,resume =False ,output_coco_json =False ,output_web_json =False ,shuffle =False ,benchmark =False ,no_sort =False ,no_hash =False ,mask_proto_debug =False ,crop =True ,detect =False )#line:117
    global args #line:119
    args =O0000O00OO00O0OO0 .parse_args (argv )#line:120
    if args .output_web_json :#line:122
        args .output_coco_json =True #line:123
    if args .seed is not None :#line:125
        random .seed (args .seed )#line:126
iou_thresholds =[OO0000OO0O00OOOOO /100 for OO0000OO0O00OOOOO in range (50 ,100 ,5 )]#line:128
coco_cats ={}#line:129
coco_cats_inv ={}#line:130
color_cache =defaultdict (lambda :{})#line:131
def prep_display (OOOOOOO000O0O0O00 ,OOO00000O0OO00OO0 ,OO00OO0OO000OO000 ,OO0OOOO0O000O0O00 ,O00O0O0OOOO0OO000 ,undo_transform =True ,class_color =False ,mask_alpha =0.45 ,w_aim =256 ,h_aim =512 ):#line:133
    ""#line:136
    if undo_transform :#line:137
        OOOO00OO0O0OOOO0O =undo_image_transformation (OO00OO0OO000OO000 ,O00O0O0OOOO0OO000 ,OO0OOOO0O000O0O00 )#line:138
        O0OO00O00OO00OO00 =torch .Tensor (OOOO00OO0O0OOOO0O )#line:140
    else :#line:141
        O0OO00O00OO00OO00 =OO00OO0OO000OO000 /255.0 #line:142
        OO0OOOO0O000O0O00 ,O00O0O0OOOO0OO000 ,_O0OOO00OO00OOO00O =OO00OO0OO000OO000 .shape #line:143
    with timer .env ('Postprocess'):#line:145
        OO00O0OO0O00OO0O0 =postprocess (OOO00000O0OO00OO0 ,O00O0O0OOOO0OO000 ,OO0OOOO0O000O0O00 ,visualize_lincomb =args .display_lincomb ,crop_masks =args .crop ,score_threshold =args .score_threshold )#line:148
    with timer .env ('Copy'):#line:152
        if cfg .eval_mask_branch :#line:153
            O0OOOOOO00O0OOOO0 =OO00O0OO0O00OO0O0 [3 ][:args .top_k ]#line:155
        O00O00OOOOO00O0O0 ,OOO00OOOO0O0O000O ,O000O0O00OO0OO000 =[O0OO0OOO0O0O0O0OO [:args .top_k ].cpu ().numpy ()for O0OO0OOO0O0O0O0OO in OO00O0OO0O00OO0O0 [:3 ]]#line:156
    O00O0O00OO00000OO =np .array (O00O00OOOOO00O0O0 ,str )#line:159
    O00O0O00OO00000OO [O00O0O00OO00000OO =='0']='person'#line:160
    O00O0O00OO00000OO [O00O0O00OO00000OO =='24']='backpack'#line:161
    O00O0O00OO00000OO [O00O0O00OO00000OO =='26']='handbag'#line:162
    O00O0O00OO00000OO [O00O0O00OO00000OO =='27']='tie'#line:163
    print ('detected: {}'.format (O00O0O00OO00000OO ))#line:164
    OO0OOO000000O0OOO =min (args .top_k ,O00O00OOOOO00O0O0 .shape [0 ])#line:168
    for O0O00OOO0O0OO0OO0 in range (OO0OOO000000O0OOO ):#line:169
        if OOO00OOOO0O0O000O [O0O00OOO0O0OO0OO0 ]<args .score_threshold :#line:170
            OO0OOO000000O0OOO =O0O00OOO0O0OO0OO0 #line:171
            break #line:172
    if OO0OOO000000O0OOO ==0 :#line:179
        O000000OOOOO0OOOO =np .ones ((h_aim ,w_aim ),'uint8')*255 #line:180
        return O000000OOOOO0OOOO #line:181
    def OO0O000O0O0OO000O (OOOO0O0OOO000OO0O ,on_gpu =None ):#line:185
        global color_cache #line:186
        O000OO000OO0O00OO =(O00O00OOOOO00O0O0 [OOOO0O0OOO000OO0O ]*5 if class_color else OOOO0O0OOO000OO0O *5 )%len (COLORS )#line:187
        if on_gpu is not None and O000OO000OO0O00OO in color_cache [on_gpu ]:#line:189
            return color_cache [on_gpu ][O000OO000OO0O00OO ]#line:190
        else :#line:191
            OO0OO0O0OO0OOOO0O =COLORS [O000OO000OO0O00OO ]#line:192
            if not undo_transform :#line:193
                OO0OO0O0OO0OOOO0O =(OO0OO0O0OO0OOOO0O [2 ],OO0OO0O0OO0OOOO0O [1 ],OO0OO0O0OO0OOOO0O [0 ])#line:195
            if on_gpu is not None :#line:196
                OO0OO0O0OO0OOOO0O =torch .Tensor (OO0OO0O0OO0OOOO0O ).to (on_gpu ).float ()/255. #line:197
                color_cache [on_gpu ][O000OO000OO0O00OO ]=OO0OO0O0OO0OOOO0O #line:198
            return OO0OO0O0OO0OOOO0O #line:202
    if args .display_masks and cfg .eval_mask_branch :#line:205
        O0OOOOOO00O0OOOO0 =O0OOOOOO00O0OOOO0 [:OO0OOO000000O0OOO ,:,:,None ]#line:207
        O0OOOOOO00O0OOOO0 =np .array (O0OOOOOO00O0OOOO0 )#line:210
        O0OOOOOO00O0OOOO0 =O0OOOOOO00O0OOOO0 .reshape (O0OOOOOO00O0OOOO0 .shape [:-1 ])#line:212
        O0OO0OO000O00O0OO =[]#line:217
        O0000OO0O0OOO0O0O =len (OOOOOOO000O0O0O00 )*len (OOOOOOO000O0O0O00 [0 ])#line:219
        OO0OO0000O00OOOO0 ,OOOOO0OO0O0O0O000 =0 ,0 #line:221
        O00O000OO0O0O00OO =None #line:222
        for O0OO000OO0O0O00O0 in range (len (O00O00OOOOO00O0O0 )):#line:223
            if O00O00OOOOO00O0O0 [O0OO000OO0O0O00O0 ]==0 and np .sum (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ,:,:])>O0000OO0O0OOO0O0O *0.15 *0.5 :#line:224
                OO0OO0000O00OOOO0 =np .sum (np .array (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ]))#line:225
                if OO0OO0000O00OOOO0 >OOOOO0OO0O0O0O000 :#line:226
                    OOOOO0OO0O0O0O000 =OO0OO0000O00OOOO0 #line:227
                    O00O000OO0O0O00OO =O0OO000OO0O0O00O0 #line:228
        if O00O000OO0O0O00OO is not None :#line:229
            O0OO0OO000O00O0OO .append (O00O000OO0O0O00OO )#line:230
        OO0OO0000O00OOOO0 ,OOOOO0OO0O0O0O000 =0 ,0 #line:232
        O00O000OO0O0O00OO =None #line:233
        for O0OO000OO0O0O00O0 in range (len (O00O00OOOOO00O0O0 )):#line:234
            if O00O00OOOOO00O0O0 [O0OO000OO0O0O00O0 ]==24 and np .sum (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ,:,:])>O0000OO0O0OOO0O0O *0.009 *0.5 :#line:235
                OO0OO0000O00OOOO0 =np .sum (np .array (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ]))#line:236
                if OO0OO0000O00OOOO0 >OOOOO0OO0O0O0O000 :#line:237
                    OOOOO0OO0O0O0O000 =OO0OO0000O00OOOO0 #line:238
                    O00O000OO0O0O00OO =O0OO000OO0O0O00O0 #line:239
        if O00O000OO0O0O00OO is not None :#line:240
            O0OO0OO000O00O0OO .append (O00O000OO0O0O00OO )#line:241
        OO0OO0000O00OOOO0 ,OOOOO0OO0O0O0O000 =0 ,0 #line:243
        O00O000OO0O0O00OO =None #line:244
        for O0OO000OO0O0O00O0 in range (len (O00O00OOOOO00O0O0 )):#line:245
            if O00O00OOOOO00O0O0 [O0OO000OO0O0O00O0 ]==26 and np .sum (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ,:,:])>O0000OO0O0OOO0O0O *0.009 *0.5 :#line:246
                OO0OO0000O00OOOO0 =np .sum (np .array (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ]))#line:247
                if OO0OO0000O00OOOO0 >OOOOO0OO0O0O0O000 :#line:248
                    OOOOO0OO0O0O0O000 =OO0OO0000O00OOOO0 #line:249
                    O00O000OO0O0O00OO =O0OO000OO0O0O00O0 #line:250
        if O00O000OO0O0O00OO is not None :#line:251
            O0OO0OO000O00O0OO .append (O00O000OO0O0O00OO )#line:252
        OO0OO0000O00OOOO0 ,OOOOO0OO0O0O0O000 =0 ,0 #line:254
        O00O000OO0O0O00OO =None #line:255
        for O0OO000OO0O0O00O0 in range (len (O00O00OOOOO00O0O0 )):#line:256
            if O00O00OOOOO00O0O0 [O0OO000OO0O0O00O0 ]==27 and np .sum (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ,:,:])>O0000OO0O0OOO0O0O *0.0025 *0.5 :#line:257
                OO0OO0000O00OOOO0 =np .sum (np .array (O0OOOOOO00O0OOOO0 [O0OO000OO0O0O00O0 ]))#line:258
                if OO0OO0000O00OOOO0 >OOOOO0OO0O0O0O000 :#line:259
                    OOOOO0OO0O0O0O000 =OO0OO0000O00OOOO0 #line:260
                    O00O000OO0O0O00OO =O0OO000OO0O0O00O0 #line:261
        if O00O000OO0O0O00OO is not None :#line:262
            O0OO0OO000O00O0OO .append (O00O000OO0O0O00OO )#line:263
        print ('valid index: {}'.format (O0OO0OO000O00O0OO ))#line:268
        if len (O0OO0OO000O00O0OO )==0 :#line:271
            O000000OOOOO0OOOO =np .ones ((h_aim ,w_aim ,3 ),'uint8')*255 #line:272
            return O000000OOOOO0OOOO #line:273
        O0OOOOOO00O0OOOO0 =O0OOOOOO00O0OOOO0 [O0OO0OO000O00O0OO ]#line:279
        OO0O00O00O0OO00OO =np .max (O0OOOOOO00O0OOOO0 ,axis =0 )#line:283
        OO0OO000OO0000O0O =np .ones ((5 ,5 ),np .uint8 )#line:307
        O00O0OOOOOO0O0OOO =cv2 .morphologyEx (OO0O00O00O0OO00OO ,cv2 .MORPH_CLOSE ,OO0OO000OO0000O0O )#line:308
        O00O0OOOOOO0O0OOO =np .array (O00O0OOOOOO0O0OOO ,'uint8')#line:310
        try :#line:313
            _O0OOO00OO00OOO00O ,O0000000OO00OOO00 ,_O0OOO00OO00OOO00O =cv2 .findContours (O00O0OOOOOO0O0OOO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:314
        except :#line:315
            O0000000OO00OOO00 ,_O0OOO00OO00OOO00O =cv2 .findContours (O00O0OOOOOO0O0OOO ,cv2 .RETR_EXTERNAL ,cv2 .CHAIN_APPROX_SIMPLE )#line:316
        O0000O00OOOO00O00 =max (O0000000OO00OOO00 ,key =lambda OO00OO0O00OOO0O00 :cv2 .contourArea (OO00OO0O00OOO0O00 ))#line:319
        OOO0000O0OOOOOO00 =np .zeros_like (O00O0OOOOOO0O0OOO )#line:322
        OO0OOO0OOOO0000O0 =cv2 .drawContours (OOO0000O0OOOOOO00 ,[O0000O00OOOO00O00 ],-1 ,color =255 ,thickness =-1 )#line:323
        OOOO0OOO0O0O0000O =np .min (np .where (OO0OOO0OOOO0000O0 >0 )[0 ])#line:327
        O000OO0O000O00000 =np .max (np .where (OO0OOO0OOOO0000O0 >0 )[0 ])#line:328
        O0O0OOO0OOO0OO0OO =np .min (np .where (OO0OOO0OOOO0000O0 >0 )[1 ])#line:329
        OO0O00OO0000O0000 =np .max (np .where (OO0OOO0OOOO0000O0 >0 )[1 ])#line:330
        OOOOOOO000O0O0O00 [:,:,0 ][OO0OOO0OOOO0000O0 ==0 ]=255 #line:334
        OOOOOOO000O0O0O00 [:,:,1 ][OO0OOO0OOOO0000O0 ==0 ]=255 #line:335
        OOOOOOO000O0O0O00 [:,:,2 ][OO0OOO0OOOO0000O0 ==0 ]=255 #line:336
        OO00OO0OO000OO000 =cv2 .cvtColor (OOOOOOO000O0O0O00 ,cv2 .COLOR_BGR2RGB )#line:340
        OO00OO0OO000OO000 =Image .fromarray (OO00OO0OO000OO000 )#line:341
        OO00OO0OO000OO000 =OO00OO0OO000OO000 .crop ((O0O0OOO0OOO0OO0OO ,OOOO0OOO0O0O0000O ,OO0O00OO0000O0000 ,O000OO0O000O00000 ))#line:348
        O00O0O0OOOO0OO000 ,OO0OOOO0O000O0O00 =OO00OO0OO000OO000 .size #line:349
        OO00OO0O00OO0O0O0 =int (h_aim *0.95 )#line:352
        OO00OO0OO000OO000 =OO00OO0OO000OO000 .resize ((int (O00O0O0OOOO0OO000 *OO00OO0O00OO0O0O0 /OO0OOOO0O000O0O00 ),OO00OO0O00OO0O0O0 ),Image .BICUBIC )#line:353
        O00O0O0OOOO0OO000 ,OO0OOOO0O000O0O00 =OO00OO0OO000OO000 .size #line:354
        O0O00O0OO0O00O0OO =Image .new ('RGB',(w_aim ,h_aim ),(255 ,255 ,255 ))#line:358
        O0O00O0OO0O00O0OO .paste (OO00OO0OO000OO000 ,(w_aim //2 -O00O0O0OOOO0OO000 //2 ,int (h_aim *0.03 )))#line:359
        return O0O00O0OO0O00O0OO #line:365
    return OOOO00OO0O0OOOO0O #line:417
def evalimage (O0OOO0O000OOO0O00 ,O00O0000O00O0O0OO :Yolact ,OOOOOOO00OO0O00OO :str ,save_path :str =None ,w_aim =256 ,h_aim =512 ):#line:421
    O00O000OOO0000OOO =torch .from_numpy (O0OOO0O000OOO0O00 ).float ()#line:423
    OOOOO000000O0O00O =FastBaseTransform ()(O00O000OOO0000OOO .unsqueeze (0 ))#line:424
    O000OOOO0OO0OOO0O =O00O0000O00O0O0OO (OOOOO000000O0O00O )#line:425
    OO0O000O00O0O0O00 =prep_display (O0OOO0O000OOO0O00 ,O000OOOO0OO0OOO0O ,O00O000OOO0000OOO ,None ,None ,undo_transform =False ,w_aim =w_aim ,h_aim =h_aim )#line:428
    return OO0O000O00O0O0O00 #line:434
def evaluate (OO0O00000OO000000 :Yolact ,OO0000OOOOO0OO0OO ,O000O00O00OO000OO ,train_mode =False ,w_aim =256 ,h_aim =512 ):#line:439
    OO0O00000OO000000 .detect .use_fast_nms =args .fast_nms #line:440
    cfg .mask_proto_debug =args .mask_proto_debug #line:441
    O0000OO0OO0O00O0O ,OO000OOOOOO0000OO =args .image .split (':')#line:443
    OO0OO0OO0OOO00000 =evalimage (O000O00O00OO000OO ,OO0O00000OO000000 ,O0000OO0OO0O00O0O ,OO000OOOOOO0000OO ,w_aim =w_aim ,h_aim =h_aim )#line:444
    return OO0OO0OO0OOO00000 #line:445
class tool_mask :#line:481
    def __init__ (OO0OO00O00OO00O0O ,OO0OOO0OO00000O0O ):#line:482
        parse_args (model_path =OO0OOO0OO00000O0O )#line:485
        if args .config is None :#line:487
            OO0OOO0OO00000O0O =SavePath .from_str (args .trained_model )#line:488
            args .config =OO0OOO0OO00000O0O .model_name +'_config'#line:490
            set_cfg (args .config )#line:492
        with torch .no_grad ():#line:494
            print ('Loading mask model...',end ='')#line:498
            OO0OO00O00OO00O0O .net =Yolact ()#line:499
            OO0OO00O00OO00O0O .net .load_weights (args .trained_model )#line:500
            OO0OO00O00OO00O0O .net .eval ()#line:502
            print ('Done.')#line:503
            if args .cuda :#line:505
                OO0OO00O00OO00O0O .net =OO0OO00O00OO00O0O .net #line:507
    def __del__ (OOOOOO00O0OOOOOOO ):#line:511
        pass #line:512
    def do_mask (OOOOOOOOOOO0000O0 ,OO0O00OOO00O0O0OO ,w_aim =256 ,h_aim =512 ):#line:515
        parse_args ()#line:517
        OO0O00OOO00O0O0OO =cv2 .cvtColor (OO0O00OOO00O0O0OO ,cv2 .COLOR_RGB2BGR )#line:520
        with torch .no_grad ():#line:522
            O0O00O0000O00O0OO =None #line:524
            OO0000000OO0O0000 =evaluate (OOOOOOOOOOO0000O0 .net ,O0O00O0000O00O0OO ,OO0O00OOO00O0O0OO ,w_aim =w_aim ,h_aim =h_aim )#line:526
        print ('mask end.')#line:530
        return np .array (OO0000000OO0O0000 ,'uint8')#line:531
if __name__ =='__main__':#line:535
    pass #line:537
