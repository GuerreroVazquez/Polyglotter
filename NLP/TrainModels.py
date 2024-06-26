import subprocess
import os
import uuid
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import sys
import random

# Fix RNG for reproducibility
RANDOM_SEED = "332021"
random.seed(RANDOM_SEED)

# Training parameters
NUM_LAYERS = 6
NUM_HEADS = 8
TRANSFORMER_FF = 2048
BATCH_SIZE = 256
RNN_SIZE = 512
WORD_VEC_SIZE = 512
VALID_BATCH_SIZE = 8
ACCUM_COUNT = 4
LEARNING_RATE = 2
DROPOUT_RATE = 0.1
ATTENTION_DROPOUT_RATE = 0.1
LABEL_SMOOTHING = 0.1
TRAIN_EPOCHS = 2000
WARMUP_STEPS = 500
DATABASE_NAME = 'MySQL'

if __name__ == "__main__":
    training_set_sizes = [1000, 5000, 10000, 25000, 50000, 100000, 1000000]
    training_set_sizes = [1000000]

    for training_set_size in training_set_sizes:
        print("### TRAINING MODEL - INFORMATION ###")
        print("Random seed: " + str(RANDOM_SEED))
        print("Training epochs: " + str(TRAIN_EPOCHS))
        print("Warmup steps: " + str(WARMUP_STEPS))
        print("RNN size: " + str(RNN_SIZE))
        print("WordVec size: " + str(WORD_VEC_SIZE))
        print("Dataset size: " + str(training_set_size))
        print("Number of layers: " + str(NUM_LAYERS))
        print("Number of heads: " + str(NUM_HEADS))
        print("Size of hidden transformer feed-forward layer: " + str(TRANSFORMER_FF))
        print("Batch size: " + str(BATCH_SIZE))
        print("Accum count: " + str(ACCUM_COUNT))
        print("Learning rate: " + str(LEARNING_RATE))
        print("Dropout rate: " + str(DROPOUT_RATE))
        print("Attention dropout rate: " + str(ATTENTION_DROPOUT_RATE))
        print("Label smoothing: " + str(LABEL_SMOOTHING))
        print("####################################")

        trainingDataSaveDir = f"../Data/TrainingData/{DATABASE_NAME}/" + str(training_set_size) + "/"

        # Using pre-trained word embeddings 
        OpenNMTcmd = 'onmt_train -data ' + str(trainingDataSaveDir) \
                     + f'dataset -save_model ./Models/model-{DATABASE_NAME}-' + str(training_set_size) \
                     + ' --layers ' + str(NUM_LAYERS) + ' -heads ' + str(NUM_HEADS) + ' -rnn_size ' + str(
            RNN_SIZE) + ' -word_vec_size ' + str(WORD_VEC_SIZE) + ' -transformer_ff ' + str(
            TRANSFORMER_FF) + ' -max_generator_batches 2 -seed ' + str(RANDOM_SEED) + ' -batch_size ' + str(
            BATCH_SIZE) + ' -valid_batch_size ' + str(VALID_BATCH_SIZE) + ' -accum_count ' + str(
            ACCUM_COUNT) + ' -optim adam -adam_beta2 0.998 -encoder_type transformer -max_grad_norm 0 -decoder_type transformer -position_encoding -param_init_glorot -param_init 0 -batch_type tokens -decay_method noam -learning_rate ' + str(
            LEARNING_RATE) + ' -normalization tokens -train_steps ' \
                     + str(TRAIN_EPOCHS) + ' -pre_word_vecs_enc ' + str(
            trainingDataSaveDir) + 'embeddings.enc.pt -pre_word_vecs_dec ' + str(
            trainingDataSaveDir) + 'embeddings.dec.pt -valid_steps 100 -save_checkpoint_steps 500 -report_every 50 -dropout ' + str(
            DROPOUT_RATE) + ' -attention_dropout ' + str(ATTENTION_DROPOUT_RATE) + ' -label_smoothing ' + str(
            LABEL_SMOOTHING) + f' -src_vocab {str(trainingDataSaveDir)}_src_vocab.pt -tgt_vocab {str(trainingDataSaveDir)}_tgt_vocab.pt' + ''
        OpenNMTcmd_d = {
            'onmt_train': True,
            'data': str(trainingDataSaveDir) + 'dataset',
            'save_model': f'./Models/model-{DATABASE_NAME}-{str(training_set_size)}',
            'layers': str(NUM_LAYERS),
            'heads': str(NUM_HEADS),
            'rnn_size': str(RNN_SIZE),
            'word_vec_size': str(WORD_VEC_SIZE),
            'transformer_ff': str(TRANSFORMER_FF),
            'max_generator_batches': '2',
            'seed': str(RANDOM_SEED),
            'batch_size': str(BATCH_SIZE),
            'valid_batch_size': str(VALID_BATCH_SIZE),
            'accum_count': str(ACCUM_COUNT),
            'optim': 'adam',
            'adam_beta2': '0.998',
            'encoder_type': 'transformer',
            'max_grad_norm': '0',
            'decoder_type': 'transformer',
            'position_encoding': True,
            'param_init_glorot': True,
            'param_init': '0',
            'batch_type': 'tokens',
            'decay_method': 'noam',
            'learning_rate': str(LEARNING_RATE),
            'normalization': 'tokens',
            'train_steps': str(TRAIN_EPOCHS),
            'pre_word_vecs_enc': str(trainingDataSaveDir) + 'embeddings.enc.pt',
            'pre_word_vecs_dec': str(trainingDataSaveDir) + 'embeddings.dec.pt',
            'valid_steps': '100',
            'save_checkpoint_steps': '500',
            'report_every': '50',
            'dropout': str(DROPOUT_RATE),
            'attention_dropout': str(ATTENTION_DROPOUT_RATE),
            'label_smoothing': str(LABEL_SMOOTHING),
            'src_vocab': str(trainingDataSaveDir) + 'src_vocab.pt',
            'tgt_vocab': str(trainingDataSaveDir) + 'tgt_vocab.pt'
        }
        print(OpenNMTcmd)

        process = subprocess.Popen(OpenNMTcmd, shell=True, stderr=subprocess.STDOUT)
        process.wait()
