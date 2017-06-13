# -*- coding: utf-8 -*
""" thesaurus.py
このスクリプトは, 日本語 WordNet のデータベースファイルから，
特定の語の類義語を検索します
"""
from os import path

class WordNet(object):
    """
    WordNet の DB ファイルに接続し,
    種々の検索を行うクラスです.
    """

    def __init__(self):
        from sqlite3 import connect
        thisdir = path.dirname(path.abspath(__file__))
        dbfile = path.abspath(path.join(THISDIR, '..', 'var', 'wnjpn.db'))
        self.con = connect(dbfile)

    def get_wordid(self, word):
        """
        特定の語のワードIDを取得します
        """
        sql = 'select * from word where lemma="{0}";'.format(
            word
        )
        return [row[0] for row in self.con.execute(sql)]

    def get_synset(self, wordid):
        """
        特定のワードID が属する類似語 ID を取得します
        """
        sql = 'select * from sense where wordid = {0};'.format(
            wordid
        )
        return [row[0] for row in self.con.execute(sql)]

    def get_synonym(self, synset, lang='eng'):
        """
        特定の synset から類義語を取得します
        """
        sql = ' '.join(
            [
                'select lemma from sense, word where synset="{0}"'.format(
                    synset
                ),
                'and word.lang="{0}"'.format(lang),
                'and sense.wordid = word.wordid;'
            ]
        )
        return [row[0] for row in self.con.execute(sql)]

    def get_synonym_by_link(self, synset, link):
        """
        入力で与えられた synset ID から,
        下位語や下位語を検索します

        ここで下位語を検索する場合には, link='hypo',
        上位語を検索する場合には, link='hype' を入力してください．
        その他の関連に関しては, 以下のページの第四項を参照してください.

        - http://compling.hss.ntu.edu.sg/wnja/jpn/detail.html
        """
        sql = ' '.join([
            'SELECT lemma FROM synlink, sense, word',
            'WHERE link ="{0}"'.format(link),
            'AND synset1 = "{0}"'.format(synset),
            'AND synset2 = synset',
            'AND sense.wordid = word.wordid',
            'AND word.lang="eng";'
        ])
        return [row[0] for row in self.con.execute(sql)]


def get_synonym(word):
    """
    引数 word で指定した語の類義語を検索します
    """
    synonyms = []
    wn = WordNet()
    wordids = wn.get_wordid(word)
    for i in wordids:
        synsetids = wn.get_synset(i)
        for synid in synsetids:
            synonyms.extend(wn.get_synonym(synid))
    synonyms = sorted(list(set(synonyms)))
    synonyms.pop(synonyms.index(word))
    return synonyms


def get_synonym_by_link(word, link):
    """
    引数 word で指定した語の link で指定された関係語を検索します.
    """
    synonyms = []
    wn = WordNet()
    wordids = wn.get_wordid(word)
    for i in wordids:
        synsetids = wn.get_synset(i)
        for synid in synsetids:
            synonyms.extend(wn.get_synonym_by_link(synid, link))
    synonyms = sorted(list(set(synonyms)))
    synonyms.pop(synonyms.index(word))
    return synonyms


# vim 呼出用関数
def thesaurus_get_synonym(word):
    synonyms = get_synonym(word)
    for synonym in synonyms:
        print("{0}".format(synonym))


if __name__ == "__main__":
    from argparse import ArgumentParser
    desc = "Shearch synonyms form args."
    PARSER = ArgumentParser(description=desc)
    PARSER.add_argument(
        "words",
        help="words you want to sherch.",
        nargs='*'
    )
    link_help = ' '.join([
        "type of word link, like hype or hypo.",
        "see cap.4 in http://compling.hss.ntu.edu.sg/wnja/jpn/detail.html"
    ])
    PARSER.add_argument(
        "--link", "-l", help=link_help
    )
    ARGS = PARSER.parse_args()
    ARGS = PARSER.parse_args()
    for word in ARGS.words:
        print("# {0} を検索します.".format(word))
        if ARGS.link:
            for synonym in get_synonym_by_link(word, ARGS.link):
                print("- {0}".format(synonym))
        else:
            for synonym in get_synonym(word):
                print("- {0}".format(synonym))
