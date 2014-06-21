doc-src
=======
ドキュメントとソースコードをTF-IDFを用いて対応付けできるかどうかやってみたScriptです。
下記のsampleの通り、postgresql-9.3.4をターゲットにしています。（和訳版含む）

結果は「http://staka.jp/wordpress/?p=72」に記載しています。

Sample
------
1. python make_data_ja.py ../data/postgresql-9.3.4/ > ../out/dataset.txt
2. python make_dic.py ../out/dataset.txt > ../out/dic.txt
3. python make_vec_idf.py ../out/dataset.txt ../out/dic.txt 4095 ../out/out.pickle
4. python out-distance-html2c.py ../out/out.pickle 5 > ../out/result.txt


