import torch


class Decoder:
    def __init__(
        self,
        d_model,
        num_heads,
        drop_prob,
        batch_size,
        max_sequence_length,
        ffn_hidden,
        num_layers,
    ) -> None:
        self.d_model = d_model
        self.num_heads = num_heads
        self.drop_prob = drop_prob
        self.batch_size = batch_size
        self.max_sequence_length = max_sequence_length
        self.ffn_fidden = ffn_hidden
        self.num_layers = num_layers

        x = torch.randn(
            (batch_size, max_sequence_length, d_model)
        )  # Enlish sentence positional encoded
        y = torch.randn(
            (batch_size, max_sequence_length, d_model)
        )  # Chinese setence postional encoded
        mask = torch.full([max_sequence_length, max_sequence_length], float("-inf"))
        mask = torch.triu(mask, diagonal=1)  # 每行向后mask掉多一位
