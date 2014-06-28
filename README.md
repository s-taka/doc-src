doc-src
=======
ドキュメントとソースコードをTF-IDFを用いて対応付けできるかどうかやってみたScriptです。
下記のsampleの通り、postgresql-9.3.4をターゲットにしています。（和訳版含む）

結果は  
http://staka.jp/wordpress/?p=72  
http://staka.jp/wordpress/?p=78  
に記載しています。

Example (use word2vec)
------
1. python to_word2vec_ja.py ../data/manual/ > ../out/to_word2vec.txt
2. python make_data_ja.py ../data/postgresql-9.3.4/ ../out/to_word2vec.txt > ../out/dataset.txt
3. python make_dic.py ../out/dataset.txt > ../out/dic.txt
4. python make_vec_idf.py ../out/dataset.txt ../out/dic.txt 4095 ../out/out.pickle
5. python out-distance-html2c.py ../out/out.pickle 5 > ../out/result.txt


* ../data/manual: 英語・日本語のマニュアルを保存したディレクトリ
* ../data/postgresql-9.3.4: PostgreSQLのソースコードと英語・日本語のマニュアルを入れたディレクトリ

Example
------
1. python make_data_ja.py ../data/postgresql-9.3.4/ > ../out/dataset.txt
2. python make_dic.py ../out/dataset.txt > ../out/dic.txt
3. python make_vec_idf.py ../out/dataset.txt ../out/dic.txt 4095 ../out/out.pickle
4. python out-distance-html2c.py ../out/out.pickle 5 > ../out/result.txt


* ../data/postgresql-9.3.4: PostgreSQLのソースコードと英語・日本語のマニュアルを入れたディレクトリ

