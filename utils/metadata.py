
import pandas as pd
import numpy as np

from os import listdir, makedirs

from os.path import isfile, join, exists

from maad.util import read_audacity_annot

def search_annotations(annotations_path, sites, verbose=False):

    # Search files files
    annotation_files = []
    for site in sites:
        path_annot = annotations_path+site
        annotation_site = [join(path_annot, f) for f in listdir(path_annot) if isfile(join(path_annot, f))]
        # To avoid xlsx!!
        annotation_site = [file for file in annotation_site if '.txt' in file]
        annotation_files.extend(annotation_site)
        if verbose:
            print(path_annot, '- cummulative sum:', len(annotation_files))
    
    return annotation_files

def load_annotations(annotation_files):
    
    """
    Load all audacity annotations on a folder
    
    Parameters
    ----------
    path_annot : str
        Path where annotations are located
    Returns
    -------
    df_all_annotations : pandas.core.frame.DataFrame
        Dataframe composed of the annotations from audacity
    """
    
    
    fnames_list = []
    df_all_annotations = pd.DataFrame()
    # TODO: avoid for loops, list comprenhension and multiprocessing
    for file in annotation_files:
        df_annotation_file = read_audacity_annot(file)
        if df_annotation_file.shape[0]>0:
            fnames_list.extend([file.split('.')[0]]*df_annotation_file.shape[0])
        else:
            fnames_list.extend([file.split('.')[0]])
            df_annotation_file = pd.DataFrame([np.nan, 0, np.nan, 60,  np.nan],
                                          index=list(df_all_annotations.columns)).T


        df_all_annotations = pd.concat([df_all_annotations, df_annotation_file],ignore_index=True)
    
    df_all_annotations.insert(loc=0, column='fname', value=fnames_list)
    
    return df_all_annotations

def transform_annotations_df(df_all_annotations):

    df = df_all_annotations.copy()

    df['min_t'] = np.floor(df['min_t'])
    df['max_t'] = np.ceil(df['max_t'])

    df[['dir','site','fname']] = df['fname'].str.rsplit('/',2, expand=True)
    df[['site','date']] = df['fname'].str.split('_',1,expand=True)

    df['date'] = df['date'].str.split('_').apply(lambda x: x[0]+x[1])
    df['date'] = pd.to_datetime(df['date'])

    df[['species','quality']] = df['label'].str.split('_',expand=True)
    df['label_duration'] = df['max_t'] - df['min_t']

    df = df.sort_values(by=['fname','min_t','max_t'],ignore_index=True)

    return df

def test_audio_annotations(df, audio_path):

    # Manual inspection
    # search INCT20955 in INCT.Anfibios/5_selection/INCT.selvino/regular
    # INCT20955, 475 audio files downloaded, 475 files in NAS
    # search INCT41 in INCT.Anfibios/5_selection/INCT.r.bastos/selection/regular_41
    # INCT41, 366 audio files downloaded, 366 in NAS
    # search INCT17 in INCT.Anfibios/5_selection/INCT.franco/selection/regular
    # INCT17, 285 audio files downloaded, 285 in NAS
    # search S4A09810 in INCT.Anfibios/5_selection/INCT.franco/selection/regular
    # S4A09810, 69 audio files downloaded, 69 in NAS
    # /volume1/INCT.ftoledo/selection/regular, 6.19 GB , 1257 files

    for i in df['site'].unique():
        print('Site:',i)
        annotation_files = list(df[df['site']==i]['fname'].unique())
        print('Annotations files:', len(annotation_files))
        mypath = audio_path + i #'data/raw/audio/'+i
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        onlyfiles = [i.split('.wav')[0] for i in onlyfiles if '.wav' in i]
        print('Audio files:', len(onlyfiles))
        if len(onlyfiles)!=len(annotation_files):
            print('Annotations intersection Audio =',len(set(annotation_files)&set(onlyfiles)))
            print('Annotations unin Audio =',len(set(annotation_files)|set(onlyfiles)))
            print('Annotations - Audio =',len(set(annotation_files)-set(onlyfiles)))
            print('Audio - Annotations =',len(set(onlyfiles)-set(annotation_files)))
        print()


df = df[df['quality']!='FALSE']


def assign_label(df, file_annotated, max_duration=60):
    
    file_annotation = []
    species_list = df['species'].dropna().unique()
    # select audio dor
    audio_dir = [dir_file for dir_file in all_audio_files if file_annotated in dir_file][0]
    # select annotations of one file of ~60s
    df_file = df[df['fname']==file_annotated]
    #display(df_file)
    for min_t in range(max_duration-window_size+1):
        try:
            y, sr = librosa.load(audio_dir, offset=min_t, duration=window_size)
            #[file_annotated,start_reading,start_reading+window_size]
            max_t = min_t+window_size
            
            # change name to co-occurence
            df_file_annotation = df_file.copy()
            #print(min_t, max_t)
            #df_overlap = df_overlap[(min_t>=df_overlap['min_t'])&(max_t<=df_overlap['max_t'])]
            df_file_annotation = df_file_annotation[(min_t<=df_file_annotation['max_t'])&(max_t>=df_file_annotation['min_t'])]
            #p_overlap = lambda x: ((min(x['max_t'], max_t)-max(x['min_t'], min_t))/min(window_size,x['label_duration']))
            #df_overlap['p_overlap_t'] = df_overlap.apply(p_overlap, axis=1)
            #df_overlap = df_overlap[df_overlap['p_overlap_t']>0]
            #print(min_t, max_t)
            #display(df_overlap)
            ### Return p overlap if species in annotation, else 0
            #t_0 = list(df_overlap['min_t'].apply(lambda x: x if x > min_t else min_t))
            #t_f = list(df_overlap['max_t'].apply(lambda x: x if max_t > x else max_t))
            #intervals = [(t_0[i],t_f[i]) for i in range(len(t_0))]
            
            #print('intervals',intervals)
            #print('intersection',find_intersection(intervals))
            
            species_overlap = [1
                                #df_overlap[df_overlap['species']==specie]['p_overlap_t'].values[0] 
                                        if specie in df_file_annotation['species'].unique() 
                                        else 0 
                                        for specie in species_list 
                                ]
            #print(species_overlap)
            
            file_annotation.append([file_annotated,min_t,max_t] + species_overlap)
        except:
            print('check:',file_annotated,min_t)
            file_annotation.append([file_annotated,min_t,0] + len(species_list)*[None])
            print([file_annotated,min_t,0] + len(species_list)*[None])

    return file_annotation


def build_meatadata_table(annotation_files):

    # Read annotations

def main():

    


