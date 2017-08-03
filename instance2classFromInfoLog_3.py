from PIL import Image
from sys import platform
import re
import glob
import os
import ntpath
from datetime import datetime
import sys
import pickle

WNID_TO_NYU_CLASS = {
        '04593077':4, '03262932':4, '02933112':6, '03207941':7, '03063968':10, '04398044':7, '04515003':7,
        '00017222':7, '02964075':10, '03246933':10, '03904060':10, '03018349':6, '03786621':4, '04225987':7,
        '04284002':7, '03211117':11, '02920259':1, '03782190':11, '03761084':7, '03710193':7, '03367059':7,
        '02747177':7, '03063599':7, '04599124':7, '20000036':10, '03085219':7, '04255586':7, '03165096':1,
        '03938244':1, '14845743':7, '03609235':7, '03238586':10, '03797390':7, '04152829':11, '04553920':7,
        '04608329':10, '20000016':4, '02883344':7, '04590933':4, '04466871':7, '03168217':4, '03490884':7,
        '04569063':7, '03071021':7, '03221720':12, '03309808':7, '04380533':7, '02839910':7, '03179701':10,
        '02823510':7, '03376595':4, '03891251':4, '03438257':7, '02686379':7, '03488438':7, '04118021':5,
        '03513137':7, '04315948':7, '03092883':10, '15101854':6, '03982430':10, '02920083':1, '02990373':3,
        '03346455':12, '03452594':7, '03612814':7, '06415419':7, '03025755':7, '02777927':12, '04546855':12,
        '20000040':10, '20000041':10, '04533802':7, '04459362':7, '04177755':9, '03206908':7, '20000021':4,
        '03624134':7, '04186051':7, '04152593':11, '03643737':7, '02676566':7, '02789487':6, '03237340':6,
        '04502670':7, '04208936':7, '20000024':4, '04401088':7, '04372370':12, '20000025':4, '03956922':7,
        '04379243':10, '04447028':7, '03147509':7, '03640988':7, '03916031':7, '03906997':7, '04190052':6,
        '02828884':4, '03962852':1, '03665366':7, '02881193':7, '03920867':4, '03773035':12, '03046257':12,
        '04516116':7, '00266645':7, '03665924':7, '03261776':7, '03991062':7, '03908831':7, '03759954':7,
        '04164868':7, '04004475':7, '03642806':7, '04589593':13, '04522168':7, '04446276':7, '08647616':4,
        '02808440':7, '08266235':10, '03467517':7, '04256520':9, '04337974':7, '03990474':7, '03116530':6,
        '03649674':4, '04349401':7, '01091234':7, '15075141':7, '20000028':9, '02960903':7, '04254009':7,
        '20000018':4, '20000020':4, '03676759':11, '20000022':4, '20000023':4, '02946921':7, '03957315':7,
        '20000026':4, '20000027':4, '04381587':10, '04101232':7, '03691459':7, '03273913':7, '02843684':7,
        '04183516':7, '04587648':13, '02815950':3, '03653583':6, '03525454':7, '03405725':6, '03636248':7,
        '03211616':11, '04177820':4, '04099969':4, '04586225':7, '02738535':4, '20000039':10,
        '20000038':10, '04476259':7, '04009801':11, '03909406':12, '03002711':7, '03085602':11, '03233905':6,
        '20000037':10, '03899768':7, '04343346':7, '03603722':7, '03593526':7, '02954340':7,
        '02694662':7, '04209613':7, '02951358':7, '03115762':9, '04038727':6, '03005285':7, '04559451':7,
        '03775636':7, '03620967':10, '02773838':7, '20000008':6, '04526964':7, '06508816':7, '20000009':6,
        '03379051':7, '04062428':7, '04074963':7, '04047401':7, '03881893':13, '03959485':7, '03391301':7,
        '03151077':12, '04590263':13, '20000006':1, '03148324':6, '20000004':1, '04453156':7, '02840245':2,
        '04591713':7, '03050864':7, '03727837':5, '06277280':11, '03365592':5, '03876519':8, '03179910':7,
        '06709442':7, '03482252':7, '04223580':7,  '04554684':7, '20000030':9, '03085013':7,
        '03169390':7, '04192858':7, '20000029':9, '04331277':4, '03452741':7, '03485997':7, '20000007':1,
        '02942699':7, '03231368':10, '03337140':7, '03001627':4, '20000011':6, '20000010':6, '20000013':6,
        '04603729':10, '20000015':4, '04548280':12, '06410904':2, '04398951':10, '03693474':9, '04330267':7,
        '03015149':9, '04460038':7, '03128519':7, '04306847':7, '03677231':7, '02871439':6, '04550184':6,
        '14974264':7, '04344873':9, '03636649':7, '20000012':6, '02876657':7, '03325088':7, '04253437':7,
        '02992529':7, '03222722':12, '04373704':4, '02851099':13, '04061681':10, '04529681':7, 
        #small objects added to scene
        '02691156':14, '02801938':14, '04099429':14, '02924116':14, '04146614':14, '02690373':14, 
        '02693413':14, '02781338':14, '03284308':14, '03928116':14, '02880940':14,
        #additional WNID in suncg previously not in scenenet
        '08632096':0, '04070727':6, '04405907':11, '03290653':6, '04301000':6, 
        '03015254':6, '02732072':6, '02870526':2, '04314914':6, '03880531':7, '03082979':7, 
        '02766320':1, '03225988':1, '03210683':7, '03378174':7, '03063338':7, '04517823':7, 
        '03584829':7, '03320046':7, '04459773':7, '03508101':7, '03931765':8, '04053677':7, 
        '03025513':7, '03586090':7, '04330340':7, '07886849':7, '02818832':1, '03964744':7, 
        '05217688':7, '03894379':12, '04285146':7, '03014317':7, '03350204':7, '03455488':7, 
        '03064758':7, '03790512':7, '02958343':7, '03074380':6, '03327234':12, '02802215':7, 
        '04161981':4, '03459591':7, '03251766':7, '03528263':7, '03380724':4, '02948072':7, 
        '03621377':7, '03982060':0, #pool is mapped to floor
        '02977058':6, '03820318':7, '01318894':7, '04507155':7, '02733524':6, '04222210':1, 
        '04105068':3, '04482393':7, '03452267':7, '02834778':7, '04485082':7, '04199027':7, 
        '03094503':7, '03384167':7, '07679356':7, '02787435':7, '00021265':7, '03953743':7, 
        '03388043':6, '03632277':7, '04243941':7, '03020416':7, '03101156':7, '04442312':7, 
        '03249569':7, '02705944':7, '02672831':7, '04419642':7, '03484083':7, '04141975':7, 
        '03970156':7, '04254120':7, '04447443':7, '03483316':7, '02937469':7, '03649909':7, 
        '04125021':7 #humans, animals mapped to objects. partition mapped to wall
        } 

NYU_14_CLASSES = [(0,'Unknown'),
                                    (1,'Bed'),
                                    (2,'Books'),
                                    (3,'Ceiling'),
                                    (4,'Chair'),
                                    (5,'Floor'),
                                    (6,'Furniture'),
                                    (7,'Objects'),
                                    (8,'Picture'),
                                    (9,'Sofa'),
                                    (10,'Table'),
                                    (11,'TV'),
                                    (12,'Wall'),
                                    (13,'Window'),
                                    (14,'SmallObjects')
]

NYU_14_CLASS_TO_TRAIN_CLASSES = {0:0, 1:2, 2:3, 3:2,  4:2,  5:1,  6:2, 
                                7:3, 8:3, 9:2, 10:2, 11:2, 12:2, 13:2, 14:3}

TRAIN_CLASSES = [(0,'Unknown'),
                                 (1,'Floor'),
                                 (2,'Background and Furnitures'),
                                 (3,'Objects'),
]

label_folder_name = 'labels_3'

def readInfoLog(infoLogFile):
    INSTANCE_TO_WNID = {}
    f = open(infoLogFile, 'r')
    f.readline() #ignore first line
    for line in f:
        instance, WNID = re.split(';|:', line)[1:3]
        WNID = WNID.split(',')[0]
        INSTANCE_TO_WNID [instance] = WNID
    return INSTANCE_TO_WNID

def main(output_dir):
    for house in os.scandir(output_dir):
        if house.name.startswith('.') or not house.is_dir():
            continue
        print ('Generating labels for house',house.name)
        for room in os.scandir(house.path):
            room_path = room.path
            infoLog_path = os.path.join(room_path, 'infoNew.log')
            INSTANCE_TO_WNID = readInfoLog(infoLog_path)
            label_path = os.path.join(room_path, label_folder_name)
            if not os.path.exists(label_path):
                os.makedirs(label_path)
            instance_dir = os.path.join(room_path, 'instance')
            for inst_png in os.scandir(instance_dir):
                inst_png_path = inst_png.path
                im = Image.open(inst_png_path)
                pix = im.load()
                width, height = im.size
                for x in range(width):
                    for y in range(height):
                        instance = pix[x,y]
                        WNID = INSTANCE_TO_WNID.get(str(instance), 0)
                        NYU = WNID_TO_NYU_CLASS.get(WNID, 0)
                        CLASS = NYU_14_CLASS_TO_TRAIN_CLASSES.get(NYU)
                        pix[x,y] = CLASS
                new_label_path = os.path.join(label_path, inst_png.name)
                # print('saving as',new_label_path)
                im.save(new_label_path)
        print ('All Labels generated for',house.name)

if __name__=='__main__':
    main(os.path.normpath(sys.argv[1]))
