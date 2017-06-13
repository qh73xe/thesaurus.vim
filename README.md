# thesaurus.vim
The vim script to shearch synonyms form word, using word net jp.

ローカル環境内のみで, 類義語検索を行う vim スクリプトです.
基本的な実装方針としては, 日本語 Word Net の sqlite3 版の DB を利用し,
これを python を使用し検索, 後は vim に表示をさせるだけの単純仕様です(調べてないから分からないけど類似のより良いものがあるかも...).
スクリプトを作成している時により良い英語表現をさがせないかなとか考えて作成しました.

筆者の趣味で, python スクリプト部分は python3 系を前提に制作しています．
