# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence


class CharLSTM(nn.Module):

    def __init__(self, n_chars, n_word_embed, n_out, pad_index=0):
        super(CharLSTM, self).__init__()

        self.n_chars = n_chars
        self.n_word_embed = n_word_embed
        self.n_out = n_out
        self.pad_index = pad_index

        # the embedding layer
        self.embed = nn.Embedding(num_embeddings=n_chars,
                                  embedding_dim=n_word_embed)
        # the lstm layer
        self.lstm = nn.LSTM(input_size=n_word_embed,
                            hidden_size=n_out//2,
                            batch_first=True,
                            bidirectional=True)

    def __repr__(self):
        s = self.__class__.__name__ + '('
        s += f"{self.n_chars}, {self.n_word_embed}, "
        s += f"n_out={self.n_out}, "
        s += f"pad_index={self.pad_index}"
        s += ')'

        return s

    def forward(self, x):
        # [batch_size, seq_len, fix_len]
        mask = x.ne(self.pad_index)
        # [batch_size, seq_len]
        lens = mask.sum(-1)
        char_mask = lens.gt(0)

        # [n, fix_len, n_word_embed]
        x = self.embed(x[char_mask])
        x = pack_padded_sequence(x, lens[char_mask], True, False)
        x, (h, _) = self.lstm(x)
        # [n, fix_len, n_out]
        h = torch.cat(torch.unbind(h), dim=-1)
        # [batch_size, seq_len, n_out]
        embed = h.new_zeros(*lens.shape, self.n_out)
        embed = embed.masked_scatter_(char_mask.unsqueeze(-1), h)

        return embed
