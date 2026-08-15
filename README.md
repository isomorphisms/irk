# IRK

Isomorphisms' R Kompiler.

The left side of this definition makes two claims:

```irk
downsize_image ← λ(image) {
    ...
}
```

`image` says what kind of value the function acts on. `downsize` says what
happens to that value. IRK checks the kind first because it is the more basic
claim.

Hungarian notation put type-like information in names but left its truth to
the programmer. IRK's difference is that the name creates an obligation which
the generated program checks.

The first experiment accepts one typed, R-shaped function:

```irk
downsize_image : Image → Image

downsize_image ← λ(image) {
    image$width  ← image$width  ÷ 2
    image$height ← image$height ÷ 2
    image
}
```

It does four small things:

1. Reads `image` from the binding name as a proposed semantic kind.
2. Rejects a declaration such as `Table → Table` because it contradicts the
   name.
3. Generates ordinary R with structural guards on both the argument and
   result, so the written `Image → Image` declaration cannot merely be
   decorative.
4. Says plainly that the `downsize` relation has not yet been proved.

Known words such as `image` resolve exactly. Unknown variants such as `photo`
are compared with a tiny local vector model. A vector match proposes a kind;
the generated guards check the nominal/structural domain and codomain at
runtime. They do not yet prove that the argument influenced the result.

```sh
python -m venv .venv
.venv/bin/pip install -r requirements.txt
sh model/fetch.sh
.venv/bin/python irk.py examples/downsize_image.irk
.venv/bin/python -m unittest discover -s tests
```

The current reader deliberately understands only one top-level function with
one argument. Reproducing all of R's grammar would hide the experiment.
