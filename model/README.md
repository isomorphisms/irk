# Meaning model

IRK uses `minishlab/potion-base-2M`, pinned at revision
`389b9f64be5aa4ae7a6bc6fe95ef20ce485ae5da`.

This is a 64-dimensional static embedding table: 29,528 token vectors, simple
pooling, and no transformer inference. The published weights are 7.56 MB and
MIT licensed. It is close to the intended "tiny modern GloVe" idea while its
subword tokenizer handles unfamiliar identifier pieces better than GloVe.

On the initial examples, the model scored:

```text
an image  ↔  image/pixels/width/height       0.685
an image  ↔  numeric table/rows/columns      0.068
downsize  ↔  reduce width and height         0.812
downsize  ↔  increase width and height       0.697
```

The last two numbers explain the design. Vectors are good enough to propose
`picture → Image`; they are not a proof that dimensions decreased.

`fetch.sh` downloads only the three files required for local inference and
checks every SHA-256 digest.

Source and model card:
https://huggingface.co/minishlab/potion-base-2M

