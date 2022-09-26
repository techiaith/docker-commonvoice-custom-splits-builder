# Common Voice Custom Splits Builder

[Click here to read this in English](#introduction)
## Cyflwyniad

Dyma'r sgriptiau a ddefnyddir gan Uned Technolegau Iaith ar gyfer creu setiau hyfforddi a phrofi amgen o gorpws Mozilla Common Voice. Mae'r sgriptiau wedi eu datblygu yn bennaf ar gyfer modelau Cymraeg (a Saesneg) ond dyle bod modd i'w haddasu ar gyfer ieithoedd eraill. 

## Sut i'w ddefnyddio

Mae angen cyfrifiadur Mac neu Linux gyda Docker wedi'i osod er mwyn defnyddio'r sgriptiau hyn. 

Byddwch angen llwytho i lawr setiau Cymraeg a Saesneg o wefan Common Voice a'i osod ar weinydd HTTP (yn delfrydol un lleol a phreifat) eich hunain. Mae angen rhoi'r cyfeiriadau a rhai manylion eraill o fewn ffeil `python/data_urls.py` - gellir copio ac addasu'r ffeil `python/data_urls.template.py`.

Wedi i chi osod yr uchod i gyd yn eu le, yna mae modd adeiladu'r amgylchedd drwy...

```shell
$ make

$ make run
```

O fewn yr amgylchedd docker, rhedwch y gorchymyn canlynol i llwytho i lawr setiau cyfan Common Voice. 

```shell
# python3 download_commonvoice.py --target_dir /data/download_commonvoice
```

Bydd data Common Voice i'w weld yn `/data/commonvoice` yn ogystal â ffeil `cv.db` sy'n cynnwys metadata'r oll ffeiliau. 



## Adeiladu setiau amgen

I adeiladu setiau modelau adnabod lleferydd Cymraeg, dylid defnyddio:

```shell
# python3 build.py
```

I adeiladu setiau hyfforddi modelau ddwyieithog, dylid defnyddio:

```shell
# python build_biling.py
```

Mae'r ddwy ffeil sgript uchod yn creu ffeiliau `.tsv` newydd o fewn eich ffolder Common voice o dan `/data` 

Mae modd creu ffeil `.tar.gz` eich hunain i gynnwys y ffeiliau `.tsv` ac mp3 . E.e. 

```shell
/data/commonvoice/CV11_CY# tar zcvf cv-corpus-11.0-2022-09-21-cy.tar.gz cv-corpus-11.0-2022-09-21/
```


## Introduction

A Mac or Linux computer with Docker installed is required to use these scripts.

You will need to download the Welsh and English sets from the Common Voice website and install it on your own (ideally local and private) HTTP server. The addresses and some other details need to be entered within a `python/data_urls.py` file - the `python/data_urls.template.py` file can be copied and modified.

Once you have all the above in place, then the environment can be built by...

```shell
$ make

$ make run
```

Within the docker environment, run the following command to download the entire Common Voice sets.

```shell
# python3 download_commonvoice.py --target_dir /data/download_commonvoice
```

Common Voice data will be found in `/data/commonvoice` as well as a `cv.db` file which contains the metadata of all the files.

## Build alternative sets

To build sets of Welsh speech recognition models, you should use:

```shell
# python3 build.py
```

To build training sets for bilingual models, use should be made of:

```shell
# python build_billing.py
```

The two script files above create new `.tsv` files within your Common voice folder under `/data`

It is possible to create your own `.tar.gz` file to contain the `.tsv` and mp3 files. E.g.

```shell
/data/commonvoice/CV11_CY# tar zcvf cv-corpus-11.0-2022-09-21-cy.tar.gz cv-corpus-11.0-2022-09-21/
```



