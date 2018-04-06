LLIM
===

A simple Pinyin input method for AI practice

## Dependence
`python3` on UNIX/Linux.

If it is running on `Windows`, you should manually redirect the IO of the python code if you do not have a `bash`

## Usage
Inference bash script which is required in the homework

```
cd bin
./llpy.sh <input_file> <output_file>
```

Python script

```
python3 src/infer/llpy.py < <input_file> > <output_file>
```

Evaulate script

```
python3 src/parsedata/check.py <input1> <input2>
```

## Evaulate figures
ROUGE-L, sentence-wise accuracy and character-wise accuracy are calculated.

## Necessary data files
The following files are loaded in the inference program

```
src/data/dict.pickle
src/data/map.pickle
```

If they are missing, you can generate them using code in `src/parsedata` and `src/train`.
