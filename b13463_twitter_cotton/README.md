python3 -m textblob.download_corpora

删除无用数据
sed '1, 11850d' xinjang324_327.csv > new.csv
