import os
import json
import nuvpy.nuviot_srvc as nuviot_srvc
import nuvpy.nuviot_util as nuviot_util
import numpy as np
import random
import pandas as pd
from keras.utils import to_categorical
from array import array
import shutil
import subprocess
from scipy.io import wavfile
import librosa
import matplotlib.pyplot as plt

def get_labels(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/labels')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def print_labels(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/labels')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("ML Labels", nuviot_util.to_item_array(rj))

def get_samples(ctx, labelid, content_type):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/samples/label/' + labelid, content_type, 200)
    if responseJSON == None:
        return
 
    return json.loads(responseJSON)

def print_samples(ctx, labelid, content_type):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/samples/label/' + labelid, content_type)
    if responseJSON == None:
        return
     
    rj = json.loads(responseJSON)
    print("ML Samples")
    
    items = rj["model"]
    
    print('-----------------------------------------')
    
   # items = nuviot_util.to_item_array(rj)

    for item in items:
        print(item["sampleId"], item["creationDate"], item["contentType"], item["contentSize"])
        
    print('-----------------------------------------')
    print()
        
def print_model_categories(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/modelcategories')
    if responseJSON == None:
        return
    
    rj = json.loads(responseJSON)
    
    items = []
    for ret_item in rj:
        items.append(nuviot_util.NuvIoTItem(ret_item["id"], ret_item["name"]))
    
    nuviot_util.print_array("Model Categories", items)

def upload_model_revision(ctx, modelid, model_file_name):
    path = '/clientapi/ml/model/' + modelid
    
    response = nuviot_srvc.post_file(ctx, path, model_file_name)
    print(response)
    
def print_models(ctx, categoryId):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/models/category/' + categoryId)
    if responseJSON == None:
        return
    rj = json.loads(responseJSON)
    
    items = []
    for ret_item in rj:
        items.append(nuviot_util.NuvIoTItem(ret_item["id"], ret_item["name"]))
    
    nuviot_util.print_array("Models", items)

def get_sample_detail(ctx, id):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/sample/' + id + "/detail")
    if responseJSON == None:
        return
 
    return json.loads(responseJSON)
    
def download_sample(ctx, sampleId, dest):
    nuviot_srvc.download_file(ctx, "/clientapi/ml/sample/" + sampleId, dest)
    
def get_datasets(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/trainingdatasets')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    return nuviot_util.to_item_array(rj)

def print_datasets(ctx):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/trainingdatasets')
    if responseJSON == None:
        return
 
    rj = json.loads(responseJSON)
    nuviot_util.print_array("ML Training Datasets", nuviot_util.to_item_array(rj))
    
def get_dataset(ctx, id):
    responseJSON = nuviot_srvc.get(ctx, '/clientapi/ml/trainingdataset/' + id)
    if responseJSON == None:
        return
 
    return json.loads(responseJSON)

def load_sample(cfg, fullFileName, rows, stride):
    fileBytes = os.path.getsize(fullFileName)  
    fileData = []
    with open(fullFileName, 'rb') as f:
        for row in range(rows):
            strideData = array('d')
            bytesToRead = int(stride)
            strideData.fromfile(f, bytesToRead)
            fileData.append(strideData)    
    return fileData

def build_feature_set(cfg, lbls, rows, stride):
    files = []
    fileLabels = []
  
    _min, _max = float('inf'), -float('inf')
    
    labelIdx = 0
    for item in lbls:
        label = item["text"]
        print(label + str(labelIdx))
        path = cfg.working_dir + "\\mfcc\\" + label + "\\bin"
        if(os.path.isdir(path)):
            filesInDir = os.listdir(path)
            file_count = len(filesInDir)
            for file in filesInDir:
                fileData = []
                fullFileName = path + "\\" + file
                fileBytes = os.path.getsize(fullFileName)
                with open(fullFileName, 'rb') as f:
                    for row in range(rows):
                        strideData = array('d')
                        bytesToRead = int(stride)
                        strideData.fromfile(f, bytesToRead)
                        fileData.append(strideData)
                        
                _min = min(np.amin(fileData), _min)
                _max = max(np.amax(fileData), _max)
 
                files.append(fileData)
                fileLabels.append(labelIdx)
                
        labelIdx = labelIdx + 1
        
    outFiles = []
    outLabels = []
   
    randomizer = random.sample(range(0, len(files)), len(files))
    for idx in range(len(files)):
        rndIdx = randomizer[idx]
        outFiles.append(files[rndIdx])
        outLabels.append(fileLabels[rndIdx])
          
    
    files, fileLabels = np.array(outFiles,np.float32), np.array(outLabels)
    
    # any particular reason I'd want to make sure we only had positive values?
    #totalRange = _max - _min
    #files = (files - _min) / (totalRange)
    
    fileLabels = to_categorical(fileLabels, num_classes = cfg.number_classes)
   
    return files, fileLabels

def generate_mfccs(cfg, smpls):
    appPath = "d:\\mobileapps\\SignalEditor\\LagoVista.MFCCBuilder\\bin\\Release\\netcoreapp2.2\\publish\\LagoVista.MFCCBuilder.exe"
    mels = "-nmels={0}".format(cfg.nmels)
    nmcc = "-nmcc={0}".format(cfg.nmcc)
    fft = "-fft={0}".format(cfg.nfft)
    hop = "-hop={0}".format(cfg.nhop)
    box = "-box={0}".format(cfg.box)

    root_output_path = "{0}\\mfcc".format(cfg.working_dir)
    print("Writing out put to %s" % root_output_path)
    shutil.rmtree(root_output_path, ignore_errors=True)

    stride = -1
    rows = -1
    idx = 0

    print("Start processing on {0} audio files.".format(smpls.shape[0]))
    print("-----------------------------------------------")

    for index, row in smpls.iterrows():
        inputFile = "-inputFile=" + row.filename
        outputPath = "-outputPath={0}\\{1}".format(root_output_path, row.label)
        p = subprocess.run([appPath, inputFile, outputPath, mels, nmcc, fft, hop, box], stdout=subprocess.PIPE)
        outmsg = str(p.stdout)[2:-5]
        parts = outmsg.split(",")
        stride = int(parts[6])
        rows = int(parts[7])

        idx = idx + 1

        print("Sample {0} out of {1}".format(idx, smpls.shape[0]), outmsg, end='\r')
    
    print("\r\nProcessed all sammples.")
    
    return rows, stride

def identify_samples(ds, cfg, ctx):
    if(os.path.exists(cfg.working_dir) == False):
        os.mkdir(cfg.working_dir)

    if(os.path.exists(cfg.working_dir + "\\rawaudio") == False):
        os.mkdir(cfg.working_dir + "\\rawaudio")

    samples = pd.DataFrame({'sampleid':[], 'filename':[],'label':[], 'rate':[],'length':[]})
    for label in ds["labels"]:
        labelName = label["text"]
        labelId = label["id"]

        label_dir = cfg.working_dir + "\\rawaudio\\" + label["text"]

        result = get_samples(ctx, labelId, 'audio-wav')
        sampleList = result["model"]

        print("Found " + str(len(sampleList)) + " samples for " + label["text"] )

        if(os.path.exists(label_dir) == False):
            os.mkdir(label_dir)

        for sample in sampleList:
            audio_file = label_dir + "\\" + sample["sampleId"] + ".wav"
            row = {'sampleid': sample["sampleId"], 'filename':audio_file, 'labelId':labelId, "label":labelName }
            samples = samples.append(row, ignore_index=True)      
    return samples

def download_samples(ctx, samples):
    rowIdx = 0
    filesDownloaded = 0
    totalRows = samples.shape[0]

    print("Audio samples: {0} files (will only download new ones)".format(totalRows))
    print("----------------------------------------------------")
    for index, row in samples.iterrows():
        rowIdx = rowIdx + 1
        if(not os.path.isfile(row.filename)):
            download_sample(ctx, row.sampleid, row.filename)
            print("File {0}%  {1}/{2} - {3} - Downloaded".format(int(rowIdx * 100 / totalRows), rowIdx, totalRows, row.filename), end='\r')
            filesDownloaded = filesDownloaded + 1

    print("\r\nCompleted - Downloaded {0} new files".format(filesDownloaded))

def populate_sample_details(samples):
    out = pd.DataFrame({'sampleid':[], 'filename':[],'label':[], 'rate':[],'length':[]})

    for index, row in samples.iterrows():
        try:
            rate, signal = wavfile.read(row.filename)
            row.rate = rate
            row.length = signal.shape[0]/rate
            out = out.append(row)
        except:
            print("Error reading file: " + row.filename)
        
    return out

def render_sample_distribution(config, samples):
    class_dist = samples.groupby(['label'])['length'].sum()
    print(class_dist)

    fig, ax = plt.subplots()
    ax.set_title('Class Distribution', y=1.08)
    ax.pie(class_dist, labels=class_dist.index, autopct='%1.1f%%',
           shadow=False, startangle=90)
    ax.axis('equal')
    plt.show()

    # we get 20 samples per second, our sample size is
    # 100ms, however we overlap each sample by 50ms
    # Take a 0.05s step forward and then sample the next 0.1s from that point
    # It means that the second half of the last sample becomes the first half 
    # of the next sample. E.g; first sample time range: 0.1s to 0.2s, 
    # second sample time range: 0.15s to 0.25s
    # TODO: this assumed sample count does not match actual

    samples_generated_per_second = config.samples_generated_per_second * config.samples_generated_overlap 
    total_sample_count = int(samples['length'].sum() * samples_generated_per_second) 
    print("Total Samples Generated: %d" % total_sample_count)
