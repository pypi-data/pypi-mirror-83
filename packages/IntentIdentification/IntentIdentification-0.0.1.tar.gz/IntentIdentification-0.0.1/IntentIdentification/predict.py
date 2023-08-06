from IntentIdentification.utils.module import ModelManager
from IntentIdentification.utils.loader import DatasetManager
from IntentIdentification.utils.predict_process import Processor

import torch

import os
import json
import random
import argparse
import numpy as np

class Arguments:
  def __init__(self):
    self.data_dir = "NULL"
    this_dir, this_filename = os.path.split(__file__)
    self.save_dir=this_dir
    self.random_state=0
    self.num_epoch=300
    self.batch_size=1
    self.l2_penalty=1e-6
    self.learning_rate=0.001
    self.dropout_rate=0.4
    self.intent_forcing_rate=0.9
    self.differentiable=False

    # model parameters.
    self.word_embedding_dim=64
    self.encoder_hidden_dim=256
    self.intent_embedding_dim=8
    self.intent_decoder_hidden_dim=64
    self.attention_hidden_dim=1024
    self.attention_output_dim=128
"""
parser = argparse.ArgumentParser()

class Arguments:

# Training parameters.
parser.add_argument('--data_dir', '-dd', type=str, default="NULL")
parser.add_argument('--save_dir', '-sd', type=str, default=this_dir)
parser.add_argument("--random_state", '-rs', type=int, default=0)
parser.add_argument('--num_epoch', '-ne', type=int, default=300)
parser.add_argument('--batch_size', '-bs', type=int, default=1)
parser.add_argument('--l2_penalty', '-lp', type=float, default=1e-6)
parser.add_argument("--learning_rate", '-lr', type=float, default=0.001)
parser.add_argument('--dropout_rate', '-dr', type=float, default=0.4)
parser.add_argument('--intent_forcing_rate', '-ifr', type=float, default=0.9)
parser.add_argument("--differentiable", "-d", action="store_true", default=False)

# model parameters.
parser.add_argument('--word_embedding_dim', '-wed', type=int, default=64)
parser.add_argument('--encoder_hidden_dim', '-ehd', type=int, default=256)
parser.add_argument('--intent_embedding_dim', '-ied', type=int, default=8)
parser.add_argument('--intent_decoder_hidden_dim', '-idhd', type=int, default=64)
parser.add_argument('--attention_hidden_dim', '-ahd', type=int, default=1024)
parser.add_argument('--attention_output_dim', '-aod', type=int, default=128)
"""
class Predictor:
  def __init__(self):
      #self.__args = parser.parse_args()
      self.__args = Arguments()
      # Fix the random seed of package random.
      random.seed(self.__args.random_state)
      np.random.seed(self.__args.random_state)

      # Fix the random seed of Pytorch when using GPU.
      if torch.cuda.is_available():
          torch.cuda.manual_seed_all(self.__args.random_state)
          torch.cuda.manual_seed(self.__args.random_state)

      # Fix the random seed of Pytorch when using CPU.
      torch.manual_seed(self.__args.random_state)
      torch.random.manual_seed(self.__args.random_state)

      # Instantiate a dataset object.
      self.__dataset = DatasetManager(self.__args)
      self.__dataset.quick_build(mode=1)

      # Instantiate a network model object.
      self.__model = ModelManager(
          self.__args, len(self.__dataset.word_alphabet),
          len(self.__dataset.intent_alphabet))
      
  def __call__(self, utterance):
      self.__args.data_dir = utterance.lower()
      self.__dataset = DatasetManager(self.__args)
      self.__dataset.quick_build(mode=1)
      # To train and evaluate the models.
      process = Processor(self.__dataset, self.__model, self.__args.batch_size)
      confidence, pred_intent = Processor.validate(self.__model, os.path.join(self.__args.save_dir, "model.pt"),self.__dataset,self.__args.batch_size) 
      return confidence, pred_intent
